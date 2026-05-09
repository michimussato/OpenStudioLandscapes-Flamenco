from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Flamenco.assets
from OpenStudioLandscapes.Flamenco import (
    LOGGER,
    dist,
)

LOGGER.info(f"Loading {dist.name} assets...")

assets_base = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Flamenco.assets],
)

defs = Definitions(
    assets=[
        *assets_base,
    ],
)
