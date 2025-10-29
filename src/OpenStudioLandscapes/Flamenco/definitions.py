from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Flamenco.assets
import OpenStudioLandscapes.Flamenco.constants

assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Flamenco.assets],
)

constants = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Flamenco.constants],
)


defs = Definitions(
    assets=[
        *assets,
        *constants,
    ],
)
