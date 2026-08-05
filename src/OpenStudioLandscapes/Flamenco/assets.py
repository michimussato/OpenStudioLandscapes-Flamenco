# pylint: disable=line-too-long,invalid-name
import copy
import json
import pathlib
import textwrap
import urllib.parse
from typing import Any, Dict, Generator, List, Union

import ruamel.yaml

# import yaml
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    AssetOut,
    AssetsDefinition,
    AssetSpec,
    MetadataValue,
    Output,
    asset,
    multi_asset,
)
from OpenStudioLandscapes.engine.common_assets import (
    cmd,
    compose,
    docker_compose_graph,
    feature,
    feature_out,
    group_in,
    group_out,
)
from OpenStudioLandscapes.engine.config.models import ConfigEngine
from OpenStudioLandscapes.engine.base.configurable_resources.docker_registry_resource import DockerRegistryConfigurableResource
from OpenStudioLandscapes.engine.base.configurable_resources.docker_resource import DockerConfigurableResource
from OpenStudioLandscapes.engine.constants import (
    ASSET_HEADER_BASE,
    ConfigParent,
)
from OpenStudioLandscapes.engine.enums import (
    DockerComposePolicies,
)
from OpenStudioLandscapes.engine.link.models import OpenStudioLandscapesFeatureIn
from OpenStudioLandscapes.engine.policies.retry import build_docker_image_retry_policy
from OpenStudioLandscapes.engine.utils import (
    create_image,
    get_docker_compose_names,
    get_docker_run_cmd,
    get_image_metadata,
    get_relative_path_via_common_root,
)
from OpenStudioLandscapes.engine.utils.docker.compose_dicts import (
    get_network_dicts,
)

from OpenStudioLandscapes.Flamenco import (
    ASSET_HEADER,
    config,
    dist,
)

# https://github.com/yaml/pyyaml/issues/722#issuecomment-1969292770
# yaml.SafeDumper.add_multi_representer(
#     data_type=enum.Enum,
#     representer=yaml.representer.SafeRepresenter.represent_str,
# )


cmd: AssetsDefinition = cmd.get_feature__cmd(
    ASSET_HEADER=ASSET_HEADER,
)

CONFIG: AssetsDefinition = feature.get_feature__CONFIG(
    ASSET_HEADER=ASSET_HEADER,
    CONFIG_STR=config.models.CONFIG_STR,
    search_model_of_type=config.models.Config,
)

feature_in: AssetsDefinition = group_in.get_feature_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_BASE=ASSET_HEADER_BASE,
    ASSET_HEADER_FEATURE_IN={},
)

group_out: AssetsDefinition = group_out.get_group_out(
    ASSET_HEADER=ASSET_HEADER,
)


docker_compose_graph: AssetsDefinition = docker_compose_graph.get_docker_compose_graph(
    ASSET_HEADER=ASSET_HEADER,
)


compose: AssetsDefinition = compose.get_compose(
    ASSET_HEADER=ASSET_HEADER,
)


feature_out_v2: AssetsDefinition = feature_out.get_feature_out_v2(
    ASSET_HEADER=ASSET_HEADER,
)


# Produces
# - feature_in_parent
# - CONFIG_PARENT
# if ConfigParent is or type FeatureBaseModel
feature_in_parent: Union[AssetsDefinition, None] = group_in.get_feature_in_parent(
    ASSET_HEADER=ASSET_HEADER,
    config_parent=ConfigParent,
)


@asset(
    **ASSET_HEADER,
    ins={
        "feature_in": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "feature_in"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
)
def write_dockerfile(
    context: AssetExecutionContext,
    config_DockerRegistryConfigurableResource: DockerRegistryConfigurableResource,
    config_DockerConfigurableResource: DockerConfigurableResource,
    feature_in: OpenStudioLandscapesFeatureIn,  # pylint: disable=redefined-outer-name
    CONFIG: config.models.Config,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    config_engine: ConfigEngine = CONFIG.config_engine

    docker_config: DockerConfigurableResource = config_DockerConfigurableResource

    docker_image: Dict = feature_in.openstudiolandscapes_base.docker_image_base

    docker_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{dist.name}",
        "__".join(context.asset_key.path),
        "Dockerfiles",
        "Dockerfile",
    )

    docker_file.parent.mkdir(parents=True, exist_ok=True)

    #################################################

    (
        image_name,
        image_prefixes,
        tags,
        build_base_parent_image_prefix,
        build_base_parent_image_name,
        build_base_parent_image_tags,
    ) = get_image_metadata(
        context=context,
        docker_image=docker_image,
        docker_config=docker_config,
        config_DockerRegistryConfigurableResource=config_DockerRegistryConfigurableResource,
        env=env,
    )

    #################################################

    # @formatter:off
    docker_file_str = textwrap.dedent("""\
        # {auto_generated}
        # {dagster_url}
        # Credits: https://io.t-k-f.ch/Flamenco/Flamenco-Manager
        
        ################################################################################
        # Multi Stage: Stage 1
        # FROM alpine:latest AS builder  # Results in inaccessible shell session
        FROM {parent_image} AS builder
        LABEL authors="{AUTHOR}"

        ENV FLAMENCO_URL={flamenco_version}
        
        WORKDIR /app
        
        RUN wget "$FLAMENCO_URL" -O flamenco.tar.gz \\
            && tar -xf flamenco.tar.gz --strip-components=1 \\
            && rm flamenco.tar.gz \\
            && chmod +x /app/tools/ffmpeg-linux-amd64 \\
            && chmod +x /app/flamenco-manager \\
            && chmod +x /app/flamenco-worker
        
        ################################################################################
        # Multi Stage: Stage 2
        FROM {parent_image} AS {image_name}
        LABEL authors="{AUTHOR}"
        
        RUN apt-get update \\
            && apt-get -y \\
                install --no-install-recommends \\
                gpg \\
            && apt-get -y autoremove --purge \\
            && apt-get -y clean \\
            && apt-get -y autoclean
        
        # Install nvidia-container-toolkit
        RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \\
            && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \\
                sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \\
                tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
                
        RUN apt-get update \\
            && apt-get -y install \\
                --no-install-recommends \\
                nvidia-container-toolkit={nvidia_container_toolkit_version} \\
                nvidia-container-toolkit-base={nvidia_container_toolkit_version} \\
                libnvidia-container-tools={nvidia_container_toolkit_version} \\
                libnvidia-container1={nvidia_container_toolkit_version} \\
            && apt-get -y autoremove \\
                --purge \\
            && apt-get -y clean \\
            && apt-get -y autoclean
        
        WORKDIR /app
        
        COPY --from=builder /app/tools/ffmpeg-linux-amd64 /app/tools/ffmpeg-linux-amd64
        COPY --from=builder /app/flamenco-manager /app/flamenco-manager
        COPY --from=builder /app/flamenco-worker /app/flamenco-worker

        ENTRYPOINT []
        """).format(
        auto_generated=f"AUTO-GENERATED by Dagster Asset {'__'.join(context.asset_key.path)}",
        dagster_url=urllib.parse.quote(
            f"http://localhost:3000/asset-groups/{'%2F'.join(context.asset_key.path)}",
            safe=":/%",
        ),
        image_name=image_name,
        # Todo: this won't work as expected if len(tags) > 1
        parent_image=f"{build_base_parent_image_prefix}{build_base_parent_image_name}:{build_base_parent_image_tags[0]}",
        flamenco_version=CONFIG.flamenco_version,
        nvidia_container_toolkit_version=CONFIG.nvidia_container_toolkit_version,
        **env,
    )
    # @formatter:on

    with open(docker_file, "w") as fw:
        fw.write(docker_file_str)

    with open(docker_file, "r") as fr:
        docker_file_content = fr.read()

    #################################################

    yield Output(docker_file)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(docker_file),
            docker_file.name: MetadataValue.md(f"```shell\n{docker_file_content}\n```"),
            "env": MetadataValue.json(env),
        },
    )


build_docker_image_spec = AssetSpec(
    key=AssetKey(
        [
            *ASSET_HEADER["key_prefix"],
            "build_docker_image",
        ]
    ),
    group_name=ASSET_HEADER["group_name"],
    description=textwrap.dedent("""
        Todo
        """),
)


@multi_asset(
    outs={
        "build_docker_image": AssetOut.from_spec(build_docker_image_spec),
    },
    ins={
        "feature_in": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "feature_in"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
        "write_dockerfile": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "write_dockerfile"])
        ),
    },
    retry_policy=build_docker_image_retry_policy,
)
def build_docker_image(
    context: AssetExecutionContext,
    config_DockerRegistryConfigurableResource: DockerRegistryConfigurableResource,
    config_DockerConfigurableResource: DockerConfigurableResource,
    feature_in: OpenStudioLandscapesFeatureIn,  # pylint: disable=redefined-outer-name
    CONFIG: config.models.Config,  # pylint: disable=redefined-outer-name
    write_dockerfile: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Dict] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    docker_config_json: pathlib.Path = (
        feature_in.openstudiolandscapes_base.docker_config_json
    )

    config_engine: ConfigEngine = CONFIG.config_engine

    docker_config: DockerConfigurableResource = config_DockerConfigurableResource

    docker_image: Dict = feature_in.openstudiolandscapes_base.docker_image_base

    #################################################

    (
        image_name,
        image_prefixes,
        tags,
        build_base_parent_image_prefix,
        build_base_parent_image_name,
        build_base_parent_image_tags,
    ) = get_image_metadata(
        context=context,
        docker_image=docker_image,
        docker_config=docker_config,
        config_DockerRegistryConfigurableResource=config_DockerRegistryConfigurableResource,
        env=env,
    )

    #################################################

    image_data, logs = create_image(
        context=context,
        image_name=image_name,
        image_prefixes=image_prefixes,
        tags=tags,
        docker_image=docker_image,
        docker_config=docker_config,
        config_DockerRegistryConfigurableResource=config_DockerRegistryConfigurableResource,
        docker_config_json=docker_config_json,
        docker_file=write_dockerfile,
    )

    output_name = "build_docker_image"

    yield Output(
        output_name=output_name,
        value=image_data,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ): MetadataValue.json(image_data),
            "env": MetadataValue.json(env),
            "docker_image": MetadataValue.path(
                f"{image_data['image_prefixes']}{image_data['image_name']}:{image_data['image_tags'][0]}"
            ),
            "docker_cmd": MetadataValue.path(
                get_docker_run_cmd(
                    context=context,
                    image_data=image_data,
                )
            ),
            "logs": MetadataValue.json(logs),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
)
def compose_networks(
    context: AssetExecutionContext,
    CONFIG: config.models.Config,  # pylint: disable=redefined-outer-name
) -> Generator[
    Output[Dict[str, Dict[str, Dict[str, str]]]] | AssetMaterialization, None, None
]:

    env: Dict = CONFIG.env

    compose_network_mode = DockerComposePolicies.NETWORK_MODE.BRIDGE

    docker_dict = get_network_dicts(
        context=context,
        compose_network_mode=compose_network_mode,
        env=env,
    )

    docker_json = json.dumps(
        docker_dict,
        indent=2,
        default=str,
    )

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_json": MetadataValue.md(f"```json\n{docker_json}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
    description=textwrap.dedent("""
        Help on `flamenco-manager.yaml`:
        - [Shared Storage](https://flamenco.blender.org/usage/shared-storage/)
        - [Variables](https://flamenco.blender.org/usage/variables/)
        - [Manager Configuration](https://flamenco.blender.org/usage/manager-configuration/)
        """),
)
def flamenco_manager_yaml(
    context: AssetExecutionContext,
    CONFIG: config.models.Config,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, None, None]:

    env: Dict = CONFIG.env

    flamenco_manager_yaml_path = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{dist.name}",
        "config",
        "flamenco-manager.yaml",
    ).expanduser()

    flamenco_manager_yaml_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    flamenco_manager_yaml_dict: Dict = copy.deepcopy(CONFIG.flamenco_manager_yaml)

    context.log.debug(f"{flamenco_manager_yaml_dict = }")

    yaml_ = ruamel.yaml.YAML(typ="rt")
    yaml_.indent(
        mapping=2,
        sequence=2,
        offset=0,
    )
    with open(flamenco_manager_yaml_path, "w") as fw:
        yaml_.dump(flamenco_manager_yaml_dict, fw)

    yield Output(flamenco_manager_yaml_path)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(
                flamenco_manager_yaml_path
            ),
            "flamenco_manager_yaml": MetadataValue.md(
                f"```yaml\n{flamenco_manager_yaml_path.read_text(encoding='utf-8')}\n```"
            ),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
        "build": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "build_docker_image"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_networks"]),
        ),
        "flamenco_manager_yaml": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "flamenco_manager_yaml"]),
        ),
    },
)
def compose_flamenco(
    context: AssetExecutionContext,
    CONFIG: config.models.Config,  # pylint: disable=redefined-outer-name
    build: Dict,  # pylint: disable=redefined-outer-name
    compose_networks: Dict,  # pylint: disable=redefined-outer-name
    flamenco_manager_yaml: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Dict] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    config_engine: ConfigEngine = CONFIG.config_engine

    network_dict = {}
    ports_dict = {}

    if "networks" in compose_networks:
        network_dict = {"networks": list(compose_networks.get("networks", {}).keys())}
        ports_dict = {
            "ports": [
                f"{CONFIG.flamenco_manager_port_host}:{CONFIG.flamenco_manager_port_container}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {"network_mode": compose_networks["network_mode"]}

    storage = CONFIG.flamenco_storage_expanded
    storage.mkdir(parents=True, exist_ok=True)

    shared_storage = CONFIG.flamenco_shared_storage_expanded
    shared_storage.mkdir(parents=True, exist_ok=True)

    volumes_dict = {
        "volumes": [
            f"{flamenco_manager_yaml.as_posix()}:/app/flamenco-manager.yaml:ro",
            f"{storage.as_posix()}:/app/flamenco-manager-storage:rw",
            f"{shared_storage.as_posix()}:/app/flamenco-manager-storage-shared:rw",
        ],
    }

    # For portability, convert absolute volume paths to relative paths

    _volume_relative = []

    for v in volumes_dict["volumes"]:

        host, container = v.split(":", maxsplit=1)

        volume_dir_host_rel_path = get_relative_path_via_common_root(
            context=context,
            path_src=CONFIG.docker_compose_expanded,
            path_dst=pathlib.Path(host),
            path_common_root=pathlib.Path(env["DOT_LANDSCAPES"]),
        )

        _volume_relative.append(
            f"{volume_dir_host_rel_path.as_posix()}:{container}",
        )

    volumes_dict = {
        "volumes": list(
            {
                *_volume_relative,
                *config_engine.global_bind_volumes,
                *CONFIG.local_bind_volumes,
            }
        ),
    }

    command = [
        "/app/flamenco-manager",
        "-trace",
    ]

    service_name = "flamenco-manager"
    container_name, host_name = get_docker_compose_names(
        context=context,
        service_name=service_name,
        landscape_id=env.get("LANDSCAPE", "default"),
        domain_lan=config_engine.openstudiolandscapes__domain_lan,
    )
    # container_name = "--".join([service_name, env.get("LANDSCAPE", "default")])
    # host_name = ".".join(
    #     [service_name, env["OPENSTUDIOLANDSCAPES__DOMAIN_LAN"]]
    # )

    docker_dict = {
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname": host_name,
                "domainname": config_engine.openstudiolandscapes__domain_lan,
                # "mac_address": ":".join(re.findall(r"..", env["HOST_ID"])),
                "restart": DockerComposePolicies.RESTART_POLICY.ALWAYS.value,
                # "image": "${DOT_OVERRIDES_REGISTRY_NAMESPACE:-docker.io/openstudiolandscapes}/%s:%s"
                # % (build["image_name"], build["image_tags"][0]),
                "image": "%s%s:%s"
                % (
                    build["image_prefixes"],
                    build["image_name"],
                    build["image_tags"][0],
                ),
                **copy.deepcopy(volumes_dict),
                **copy.deepcopy(network_dict),
                **copy.deepcopy(ports_dict),
                "environment": {
                    "TZ": config_engine.tz,
                    **config_engine.global_environment_variables,
                    **CONFIG.local_environment_variables,
                },
                # "environment": {
                # },
                # "healthcheck": {
                # },
                "command": command,
            },
        },
    }

    docker_json = json.dumps(
        docker_dict,
        indent=2,
        default=str,
    )

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "docker_json": MetadataValue.md(f"```json\n{docker_json}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "compose_flamenco": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_flamenco"]),
        ),
    },
)
def compose_maps(
    context: AssetExecutionContext,
    **kwargs,  # pylint: disable=redefined-outer-name
) -> Generator[Output[List[Dict]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    context.log.info(ret)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )
