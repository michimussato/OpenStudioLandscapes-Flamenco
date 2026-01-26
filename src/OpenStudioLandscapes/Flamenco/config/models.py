import enum
import pathlib
from typing import List

from dagster import get_dagster_logger
from pydantic import (
    Field,
    PositiveInt,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel

from OpenStudioLandscapes.Flamenco import constants, dist


class FlamencoArchives(enum.StrEnum):
    version_3_7 = (
        "https://flamenco.blender.org/downloads/flamenco-3.7-linux-amd64.tar.gz"
    )
    version_3_8 = (
        "https://flamenco.blender.org/downloads/flamenco-3.8-linux-amd64.tar.gz"
    )


class Config(FeatureBaseModel):

    feature_name: str = dist.name

    group_name: str = constants.ASSET_HEADER["group_name"]

    key_prefixes: List[str] = constants.ASSET_HEADER["key_prefix"]

    flamenco_manager_port_host: PositiveInt = Field(
        default=8484,
    )

    flamenco_manager_port_container: PositiveInt = Field(
        default=8080,
    )

    # Todo
    # - [ ] Tuple?
    flamenco_version: FlamencoArchives = Field(
        default=FlamencoArchives.version_3_7,
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


CONFIG_STR = Config.get_docs()

