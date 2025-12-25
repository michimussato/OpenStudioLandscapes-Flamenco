[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-Flamenco](#feature-openstudiolandscapes-flamenco)
   1. [Brief](#brief)
   2. [Configuration](#configuration)
2. [External Resources](#external-resources)
   1. [Quickstart](#quickstart)
   2. [Help](#help)
      1. [Manager](#manager)
      2. [Worker](#worker)
3. [Community](#community)
4. [Technical Reference](#technical-reference)
   1. [Requirements](#requirements)
   2. [Install](#install)
      1. [This Feature](#this-feature)
   3. [Testing](#testing)
      1. [pre-commit](#pre-commit)
      2. [nox](#nox)

***

This `README.md` was dynamically created with [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator).

***

# Feature: OpenStudioLandscapes-Flamenco

## Brief

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

> [!NOTE]
> 
> You feel like writing your own Feature? Go and check out the 
> [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template).

## Configuration

OpenStudioLandscapes will search for a local config store. The default location is `~/.config/OpenStudioLandscapes/config-store/` but you can specify a different location if you need to.

A local config store location will be created if it doesn't exist, together with the `config.yml` files for each individual Feature.

> [!TIP]
> 
> The config store root will be initialized as a local Git
> controlled repository. This makes it easy to track changes
> you made to the `config.yml`.

> [!TIP]
> 
> To specify a config store location different than
> the default, you can do so be setting the environment variable
> `OPENSTUDIOLANDSCAPES__CONFIGSTORE_ROOT`:
> 
> ```shell
> OPENSTUDIOLANDSCAPES__CONFIGSTORE_ROOT="~/.config/OpenStudioLandscapes/my-custom-config-store"
> ```

The following settings are available in `OpenStudioLandscapes-Flamenco` and are based on [`OpenStudioLandscapes-Flamenco/tree/main/OpenStudioLandscapes/Flamenco/config/models.py`](https://github.com/michimussato/OpenStudioLandscapes-Flamenco/tree/main/OpenStudioLandscapes/Flamenco/config/models.py).

```yaml
# ===
# env
# ---
#
# Type: typing.Dict
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# =============
# config_engine
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.ConfigEngine'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# =============
# config_parent
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.FeatureBaseModel'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ============
# distribution
# ------------
#
# Type: <class 'importlib.metadata.Distribution'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ==========
# group_name
# ----------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         Dagster Group name. This will represent the group node name. See https://docs.dagster.io/api/dagster/assets for more information
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
group_name: OpenStudioLandscapes_Flamenco


# ============
# key_prefixes
# ------------
#
# Type: typing.List[str]
# Base Class Info:
#     Required:
#         True
#     Description:
#         Dagster Asset key prefixes. This will be reflected in the nesting (directory structure) of the Asset. See https://docs.dagster.io/api/dagster/assets for more information
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
key_prefixes:
- OpenStudioLandscapes_Flamenco


# =======
# enabled
# -------
#
# Type: <class 'bool'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         Whether the Feature is enabled or not.
#     Default value:
#         True
# Description:
#     Whether the Feature is enabled or not.
# Required:
#     False
# Examples:
#     None


# =============
# compose_scope
# -------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         default
# Description:
#     None
# Required:
#     False
# Examples:
#     ['default', 'license_server', 'worker']


# ============
# feature_name
# ------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         The name of the feature. It is derived from the `OpenStudioLandscapes.<Feature>.dist` attribute.
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
feature_name: OpenStudioLandscapes-Flamenco


# ==============
# docker_compose
# --------------
#
# Type: <class 'pathlib.Path'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         The path to the `docker-compose.yml` file.
#     Default value:
#         {DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/docker_compose/docker-compose.yml
# Description:
#     The path to the `docker-compose.yml` file.
# Required:
#     False
# Examples:
#     None


# ==========================
# flamenco_manager_port_host
# --------------------------
#
# Type: <class 'int'>
# Description:
#     None
# Required:
#     False
# Examples:
#     None
flamenco_manager_port_host: 8484


# ===============================
# flamenco_manager_port_container
# -------------------------------
#
# Type: <class 'int'>
# Description:
#     None
# Required:
#     False
# Examples:
#     None
flamenco_manager_port_container: 8080


# ================
# flamenco_version
# ----------------
#
# Type: <enum 'FlamencoArchives'>
# Description:
#     None
# Required:
#     False
# Examples:
#     ['version_3_7', 'version_3_8']
flamenco_version: https://flamenco.blender.org/downloads/flamenco-3.7-linux-amd64.tar.gz


# ================
# flamenco_storage
# ----------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     None
# Required:
#     False
# Examples:
#     None
flamenco_storage: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/storage'


# =======================
# flamenco_shared_storage
# -----------------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     None
# Required:
#     False
# Examples:
#     None
flamenco_shared_storage: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/shared_storage'
```

***

# External Resources

[![Logo Flamenco ](https://flamenco.blender.org/brand.svg)](https://flamenco.blender.org/)

Official Flamenco information.

## Quickstart

- [Quickstart](https://flamenco.blender.org/usage/quickstart/)

## Help

Remember to add flamenco-manager FQDN to your local DNS server for the worker to be able to find it by.

### Manager

```generic
./flamenco-manager --help                                                                                                                                                                                                              ✔ 
2025-10-29T13:04:02+01:00 INF starting Flamenco arch=amd64 git=72c1bad4 os=linux osDetail="Manjaro Linux (6.16.8-1-MANJARO)" releaseCycle=release version=3.7
Usage of ./flamenco-manager:
  -debug
        Enable debug-level logging.
  -delay
        Add a random delay to any HTTP responses. This aids in development of Flamenco Manager's web frontend.
  -pprof
        Expose profiler endpoints on /debug/pprof/.
  -quiet
        Only log warning-level and worse.
  -setup-assistant
        Open a webbrowser with the setup assistant.
  -trace
        Enable trace-level logging.
  -version
        Shows the application version, then exits.
  -write-config
        Writes configuration to flamenco-manager.yaml, then exits.
```

- [Manager Configuration](https://flamenco.blender.org/usage/manager-configuration/)

### Worker

```generic
./flamenco-worker --help                                                                                                                                                                                                               ✔ 
Usage of ./flamenco-worker:
  -debug
        Enable debug-level logging.
  -find-manager
        Autodiscover a Manager, then quit.
  -flush
        Flush any buffered task updates to the Manager, then exits.
  -manager string
        URL of the Flamenco Manager.
  -quiet
        Only log warning-level and worse.
  -register
        (Re-)register at the Manager.
  -restart-exit-code int
        Mark this Worker as restartable. It will exit with this code to signify it needs to be restarted.
  -trace
        Enable trace-level logging.
  -version
        Shows the application version, then exits.
```

- [Worker Configuration](https://flamenco.blender.org/usage/worker-configuration/)

```generic
./flamenco-worker -manager flamenco-manager.openstudiolandscapes.lan:8484                                                                                                                                                              ✔ 
2025-10-29T15:30:42+01:00 INF starting Flamenco Worker arch=amd64 git=72c1bad4 os=linux osDetail="Manjaro Linux (6.16.8-1-MANJARO)" pid=625742 releaseCycle=release version=3.7
2025-10-29T15:30:42+01:00 INF will load configuration from these paths credentials=/home/michael/.local/share/flamenco/flamenco-worker-credentials.yaml main=/home/michael/Downloads/flamenco-3.7-linux-amd64/flamenco-worker.yaml
2025-10-29T15:30:42+01:00 INF using Manager URL from commandline manager=http://flamenco-manager.openstudiolandscapes.lan:8484
2025-10-29T15:30:42+01:00 INF Blender could not be found. Flamenco Manager will have to supply the full path to Blender when tasks are sent to this Worker. For more info see https://flamenco.blender.org/usage/variables/blender/
2025-10-29T15:30:42+01:00 INF FFmpeg found on this system path=/home/michael/Downloads/flamenco-3.7-linux-amd64/tools/ffmpeg-linux-amd64 version=7.0.2-static
2025-10-29T15:30:42+01:00 INF loaded configuration config={"ConfiguredManager":"","LinuxOOMScoreAdjust":null,"ManagerURL":"http://flamenco-manager.openstudiolandscapes.lan:8484","RestartExitCode":0,"TaskTypes":["blender","ffmpeg","file-management","misc"],"WorkerName":""}
2025-10-29T15:30:42+01:00 INF loaded credentials filename=/home/michael/.local/share/flamenco/flamenco-worker-credentials.yaml
2025-10-29T15:30:42+01:00 INF signing on at Manager manager=http://flamenco-manager.openstudiolandscapes.lan:8484 name=lenovo softwareVersion=3.7 taskTypes=["blender","ffmpeg","file-management","misc"]
2025-10-29T15:30:42+01:00 WRN unable to sign on at Manager code=403 resp={"code":0,"message":"Security requirements failed"}
2025-10-29T15:30:42+01:00 INF registered at Manager code=200 resp={"address":"192.168.178.195","name":"lenovo","platform":"linux","software":"","status":"","supported_task_types":["blender","ffmpeg","file-management","misc"],"uuid":"73f5de82-a3aa-4f93-ab88-b3adf0be35d6"}
2025-10-29T15:30:42+01:00 INF Saved configuration file filename=/home/michael/.local/share/flamenco/flamenco-worker-credentials.yaml
2025-10-29T15:30:42+01:00 INF signing on at Manager manager=http://flamenco-manager.openstudiolandscapes.lan:8484 name=lenovo softwareVersion=3.7 taskTypes=["blender","ffmpeg","file-management","misc"]
2025-10-29T15:30:42+01:00 INF manager accepted sign-on startup_state=awake
2025-10-29T15:30:42+01:00 INF opening database dsn=/home/michael/.local/share/flamenco/flamenco-worker.sqlite
2025-10-29T15:30:42+01:00 INF state change curState=starting newState=awake
^C2025-10-29T15:30:49+01:00 INF signal received, shutting down. signal=interrupt
2025-10-29T15:30:49+01:00 INF signing off at Manager state=offline
2025-10-29T15:30:49+01:00 WRN shutdown complete, stopping process.
```

***

# Community

| Feature                              | GitHub                                                                                                                                       | Discord                                                                 |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| OpenStudioLandscapes                 | [https://github.com/michimussato/OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                                 | [# openstudiolandscapes-general](https://discord.gg/F6bDRWsHac)         |
| OpenStudioLandscapes-Ayon            | [https://github.com/michimussato/OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)                       | [# openstudiolandscapes-ayon](https://discord.gg/gd6etWAF3v)            |
| OpenStudioLandscapes-Dagster         | [https://github.com/michimussato/OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster)                 | [# openstudiolandscapes-dagster](https://discord.gg/jwB3DwmKvs)         |
| OpenStudioLandscapes-Flamenco        | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco](https://github.com/michimussato/OpenStudioLandscapes-Flamenco)               | [# openstudiolandscapes-flamenco](https://discord.gg/EPrX5fzBCf)        |
| OpenStudioLandscapes-Flamenco-Worker | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker](https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker) | [# openstudiolandscapes-flamenco-worker](https://discord.gg/Sa2zFqSc4p) |
| OpenStudioLandscapes-Kitsu           | [https://github.com/michimussato/OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)                     | [# openstudiolandscapes-kitsu](https://discord.gg/6cc6mkReJ7)           |
| OpenStudioLandscapes-RustDeskServer  | [https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer](https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer)   | [# openstudiolandscapes-rustdeskserver](https://discord.gg/nJ8Ffd2xY3)  |
| OpenStudioLandscapes-Template        | [https://github.com/michimussato/OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template)               | [# openstudiolandscapes-template](https://discord.gg/J59GYp3Wpy)        |
| OpenStudioLandscapes-VERT            | [https://github.com/michimussato/OpenStudioLandscapes-VERT](https://github.com/michimussato/OpenStudioLandscapes-VERT)                       | [# openstudiolandscapes-twingate](https://discord.gg/FYaFRUwbYr)        |

To follow up on the previous LinkedIn publications, visit:

- [OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).
- [Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).

***

# Technical Reference

## Requirements

- `python-3.11`
- `OpenStudioLandscapes`

## Install

### This Feature

Clone this repository into `OpenStudioLandscapes/.features` (assuming the current working directory to be the Git repository root `./OpenStudioLandscapes`):

```shell
git -C ./.features clone https://github.com/michimussato/OpenStudioLandscapes-Flamenco.git
```

Install into OpenStudioLandscapes `venv` (`./OpenStudioLandscapes/.venv`):

```shell
source .venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -e "./.features/OpenStudioLandscapes-Flamenco[dev]"
pip install -e ".[dev]"
```

For more info see [VCS Support of pip](https://pip.pypa.io/en/stable/topics/vcs-support/).

## Testing

### pre-commit

- https://pre-commit.com
- https://pre-commit.com/hooks.html

```shell
pre-commit install
```

### nox

#### Generate Report

```shell
nox --no-error-on-missing-interpreters --report .nox/nox-report.json
```

#### Re-Generate this README

```shell
nox -v --add-timestamp --session readme
```

#### pylint

```shell
nox -v --add-timestamp --session lint
```

##### pylint: disable=redefined-outer-name

- [`W0621`](https://pylint.pycqa.org/en/latest/user_guide/messages/warning/redefined-outer-name.html): Due to Dagsters way of piping arguments into assets.

#### SBOM

Acronym for Software Bill of Materials

```shell
nox -v --add-timestamp --session sbom
```

We create the following SBOMs:

- [`cyclonedx-bom`](https://pypi.org/project/cyclonedx-bom/)
- [`pipdeptree`](https://pypi.org/project/pipdeptree/) (Dot)
- [`pipdeptree`](https://pypi.org/project/pipdeptree/) (Mermaid)

SBOMs for the different Python interpreters defined in [`.noxfile.VERSIONS`](https://github.com/michimussato/OpenStudioLandscapes-Flamenco/tree/main/noxfile.py) will be created in the [`.sbom`](https://github.com/michimussato/OpenStudioLandscapes-Flamenco/tree/main/.sbom) directory of this repository.

- `cyclone-dx`
- `pipdeptree` (Dot)
- `pipdeptree` (Mermaid)

Currently, the following Python interpreters are enabled for testing:

- `python3.11`

***

Last changed: **2025-12-25 14:28:32 UTC**