from pathlib import Path
from pygame import Color, Font, Vector2
from justkeepswimming.components.font import TextComponent
from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.components.ui import ButtonComponent
from justkeepswimming.prefabs.renderable import RenderablePrefab
from justkeepswimming.processors.font import TextProcessor
from justkeepswimming.processors.ui import ButtonProcessor
from justkeepswimming.utilities.prefab import Prefab


class ButtonPrefab(Prefab):
    extends = RenderablePrefab()
    components = [
        TextComponent(),
        ButtonComponent(),
    ]
    processors = [
        ButtonProcessor,
        TextProcessor,
    ]


PLAY_BUTTON_FONT = Font(Path("assets/fonts/GameOver.otf"), 12)


class PlayButtonPrefab(Prefab):
    extends = RenderablePrefab()
    components = [
        TransformComponent(
            position=Vector2(1920 / 2, 1080 / 2),
            anchor=Vector2(0.5, 0.5),
            size=Vector2(600, 50),
        ),
        TextComponent(
            color=Color(255, 255, 255),
            background_color=Color(0, 0, 0, 0),
            font=PLAY_BUTTON_FONT,
            antialias=True,
            content="Play",
        ),
        ButtonComponent(
            label_color_hover=Color(255, 255, 255),
            label_color=Color(0, 0, 0),
            hover_background_color=Color(0, 0, 0),
            background_color=Color(255, 255, 255),
        ),
        RendererComponent(
            layer=100
        )
    ]
    processors = [
        ButtonProcessor,
        TextProcessor,
    ]
