from justkeepswimming.components.font import (
    TextComponent
)
from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.prefabs.renderable import RenderablePrefab
from justkeepswimming.processors.font import (
    TextProcessor
)
from justkeepswimming.utilities.prefab import Prefab
from pygame import Color, Font, Vector2
from pathlib import Path


class TextPrefab(Prefab):
    extends = RenderablePrefab()
    components = [
        TextComponent(),
    ]
    processors = [
        TextProcessor,
    ]


TITLE_SPLASH_LOGO_FONT = Font(Path("assets/fonts/GameOver.otf"), 48)
TITLE_SPLASH_LOGO_FONT.set_bold(True)


class TitleScreenTextPrefab(Prefab):
    extends = TextPrefab()
    components = [
        TextComponent(
            color=Color(255, 255, 255),
            background_color=Color(0, 0, 0, 0),
            font=TITLE_SPLASH_LOGO_FONT,
            antialias=True,
            content="JustKeepSwimming!"
        ),
        TransformComponent(
            position=Vector2((1920 / 3) / 2, (1080 / 3) / 4),
            anchor=Vector2(0.5, 0.5)
        ),
        RendererComponent(
            layer=100
        )
    ]
    processors = [
        TextProcessor,
    ]
