from pathlib import Path
from pygame import Color, Font, Vector2
from justkeepswimming.components.font import TextComponent
from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.components.ui import ButtonComponent
from justkeepswimming.debug.processors.button import ButtonDebuggerProcessor
from justkeepswimming.prefabs.renderable import RenderablePrefab
from justkeepswimming.processors.font import TextProcessor
from justkeepswimming.processors.render import RendererProcessor
from justkeepswimming.processors.button import ButtonProcessor
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
        ButtonDebuggerProcessor,
    ]


PLAY_BUTTON_FONT = Font(Path("assets/fonts/GameOver.otf"), 20)


class PlayButtonPrefab(Prefab):
    extends = RenderablePrefab()
    components = [
        TransformComponent(
            position=Vector2((1920 / 3) / 2, ((1080 / 4) / 2) + 50),
            anchor=Vector2(0, 0),
            size=Vector2(150, 30),
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
            background_color_hover=Color(0, 0, 0),
            background_color=Color(255, 255, 255),
        ),
        RendererComponent(layer=100),
    ]
    processors = [
        ButtonDebuggerProcessor,
        ButtonProcessor,
        RendererProcessor,
        TextProcessor,
    ]


class SettingsButtonPrefab(Prefab):
    extends = RenderablePrefab()
    components = [
        TransformComponent(
            position=Vector2((1920 / 3) / 2, ((1080 / 4) / 2) + 100),
            anchor=Vector2(0, 0),
            size=Vector2(150, 30),
        ),
        TextComponent(
            color=Color(255, 255, 255),
            background_color=Color(0, 0, 0, 0),
            font=PLAY_BUTTON_FONT,
            antialias=True,
            content="Settings",
        ),
        ButtonComponent(
            label_color_hover=Color(255, 255, 255),
            label_color=Color(0, 0, 0),
            background_color_hover=Color(0, 0, 0),
            background_color=Color(255, 255, 255),
        ),
        RendererComponent(layer=100),
    ]
    processors = [
        ButtonDebuggerProcessor,
        ButtonProcessor,
        RendererProcessor,
        TextProcessor,
    ]


class QuitButtonPrefab(Prefab):
    extends = RenderablePrefab()
    components = [
        TransformComponent(
            position=Vector2((1920 / 3) / 2, ((1080 / 4) / 2) + 150),
            anchor=Vector2(0, 0),
            size=Vector2(150, 30),
        ),
        TextComponent(
            color=Color(255, 255, 255),
            background_color=Color(0, 0, 0, 0),
            font=PLAY_BUTTON_FONT,
            antialias=True,
            content="Quit",
        ),
        ButtonComponent(
            label_color_hover=Color(255, 255, 255),
            label_color=Color(0, 0, 0),
            background_color_hover=Color(0, 0, 0),
            background_color=Color(255, 255, 255),
        ),
        RendererComponent(layer=100),
    ]
    processors = [
        ButtonDebuggerProcessor,
        ButtonProcessor,
        RendererProcessor,
        TextProcessor,
    ]
