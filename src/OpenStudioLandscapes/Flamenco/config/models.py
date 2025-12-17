import pathlib

from dagster import get_dagster_logger
from pydantic import (
    Field,
    PositiveInt,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel

from OpenStudioLandscapes.Flamenco import dist

config_default = pathlib.Path(__file__).parent.joinpath("config_default.yml")
CONFIG_STR = config_default.read_text()


class Config(FeatureBaseModel):

    feature_name: str = dist.name

    definitions: str = "OpenStudioLandscapes.Ayon.definitions"

    flamenco_manager_port_host: PositiveInt = Field(
        default=8484,
    )

    flamenco_manager_port_container: PositiveInt = Field(
        default=8080,
    )

    # Todo
    # - [ ] Tuple?
    flamenco_version: str = Field(
        default="3.7",
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
            self.flamenco_storage.expanduser()
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
            self.flamenco_shared_storage.expanduser()
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret
