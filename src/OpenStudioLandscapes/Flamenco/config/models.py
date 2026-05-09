import enum
import pathlib
from typing import Dict, List

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel
from pydantic import (
    Field,
    PositiveInt,
)

from OpenStudioLandscapes.Flamenco import (
    ASSET_HEADER,
    LOGGER,
    dist,
)


class FlamencoArchives(enum.StrEnum):
    version_3_7 = (
        "https://flamenco.blender.org/downloads/flamenco-3.7-linux-amd64.tar.gz"
    )
    version_3_8 = (
        "https://flamenco.blender.org/downloads/flamenco-3.8-linux-amd64.tar.gz"
    )
    version_3_8_2 = (
        "https://flamenco.blender.org/downloads/flamenco-3.8.2-linux-amd64.tar.gz"
    )


FLAMENCO_DEFAULT_LISTEN_PORT: int = 8080


class ManagerConfigs(enum.Enum):

    # Todo:
    #  - [ ] Two-Way?
    #        https://flamenco.blender.org/usage/variables/#two-way-variables-for-mixed-platform-farms
    #        https://flamenco.blender.org/usage/variables/multi-platform/
    #        variables:
    #          my_storage:
    #            is_twoway: true
    #            values:
    #            - platform: linux
    #              value: /media/shared/flamenco
    #            - platform: windows
    #              value: F:\flamenco
    #            - platform: darwin
    #              value: /Volumes/shared/flamenco

    version_3_8_2 = {
        "_meta": {
            "version": 3,
        },
        # Core Settings
        "manager_name": "OpenStudioLandscapes-Flamenco",
        "database": pathlib.Path(
            "/app/flamenco-manager-storage/flamenco-manager.sqlite"
        ),
        "database_check_period": "10m0s",
        "listen": f":{FLAMENCO_DEFAULT_LISTEN_PORT}",
        "autodiscoverable": True,
        # Storage
        "local_manager_storage_path": pathlib.Path("/app/flamenco-manager-storage"),
        "shared_storage_path": pathlib.Path("/app/flamenco-manager-storage-shared"),
        "shaman": {
            "enabled": True,
            "garbageCollect": {
                "period": "24h0m0s",
                "maxAge": "744h0m0s",
                "extraCheckoutPaths": [],
            },
        },
        # Timeout & Failures
        "task_timeout": "10m0s",
        "worker_timeout": "1m0s",
        "blocklist_threshold": 3,
        "task_fail_after_softfail_count": 3,
        # MQTT Configuration
        "mqtt": {
            "client": {
                "broker": "",
                "clientID": "flamenco",
                "topic_prefix": "flamenco",
                "username": "",
                "password": "",
            },
        },
        # Variables
        "variables": {
            "blender": {
                "values": [
                    # {
                    #     "audience": "",
                    #     "platform": "",
                    #     "value": "",
                    # },
                    {
                        "audience": "all",
                        "platform": "linux",
                        "value": pathlib.Path("blender"),
                    },
                    {
                        "audience": "all",
                        "platform": "windows",
                        "value": pathlib.Path("blender.exe"),
                    },
                    {
                        "audience": "all",
                        "platform": "darwin",
                        "value": pathlib.Path("blender"),
                    },
                ],
            },
            "blenderArgs": {
                "values": [
                    # {
                    #     "audience": "",
                    #     "platform": "",
                    #     "value": "",
                    # },
                    {
                        "audience": "all",
                        "platform": "all",
                        "value": " ".join(
                            [
                                "--background",
                                "--debug",
                                "--enable-autoexec",
                            ]
                        ),
                    },
                ],
            },
        },
    }


class Config(FeatureBaseModel):

    flamenco_manager_yaml: Dict = Field(
        default=ManagerConfigs.version_3_8_2.value,
        description="The flamenco-manager.yaml. See "
        "https://flamenco.blender.org/usage/manager-configuration/ "
        "for more information.",
    )

    feature_name: str = dist.name

    group_name: str = ASSET_HEADER["group_name"]

    key_prefixes: List[str] = ASSET_HEADER["key_prefix"]

    flamenco_manager_port_host: PositiveInt = Field(
        default=8484,
    )

    flamenco_manager_port_container: PositiveInt = Field(
        default=FLAMENCO_DEFAULT_LISTEN_PORT,
    )

    # Todo
    # - [ ] Tuple?
    flamenco_version: FlamencoArchives = Field(
        default=FlamencoArchives.version_3_8_2,
        examples=[i.name for i in FlamencoArchives],
    )

    # Todo
    #  - [ ] Implement Postgres DB Backend?

    flamenco_storage: pathlib.Path = Field(
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/storage"),
    )

    flamenco_shared_storage: pathlib.Path = Field(
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/shared_storage"),
    )

    # EXPANDABLE PATHS
    @property
    def flamenco_storage_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")
        LOGGER.debug(f"Expanding {self.flamenco_storage}...")
        ret = pathlib.Path(
            self.flamenco_storage.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret

    @property
    def flamenco_shared_storage_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.flamenco_shared_storage}...")
        ret = pathlib.Path(
            self.flamenco_shared_storage.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret


if __name__ == "__main__":
    CONFIG_STR = Config.get_docs()
else:
    import yaml

    CONFIG_STR = yaml.dump(
        Config.model_json_schema(mode="serialization"),
    )
