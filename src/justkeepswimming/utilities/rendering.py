import pygame
from pygame import Color, Surface, Vector2


def render_arrow(
    surface: Surface,
    start: Vector2,
    target: Vector2,
    color: Color = Color(255, 0, 0),
    thickness: int = 1,
) -> None:
    pygame.draw.line(surface, color, start, target, thickness)
    direction = (target - start).normalize()
    perpendicular = Vector2(-direction.y, direction.x)
    arrow_size = 5 + thickness
    left_wing = target - direction * arrow_size + perpendicular * (arrow_size / 2)
    right_wing = target - direction * arrow_size - perpendicular * (arrow_size / 2)
    pygame.draw.polygon(surface, color, [target, left_wing, right_wing])


def render_vector(
    surface: Surface,
    origin: Vector2,
    vector: Vector2,
    color: Color = Color(0, 255, 0),
    thickness: int = 1,
) -> None:
    end_point = origin + vector
    pygame.draw.line(surface, color, origin, end_point, thickness)
    pygame.draw.circle(surface, color, end_point, thickness * 2)


def render_label(
    surface: Surface,
    position: Vector2,
    text: str,
    font: pygame.font.Font,
    color: Color = Color(255, 255, 255),
    offset: Vector2 = Vector2(0, 0),
) -> None:
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position + offset)


def render_bounding_box(
    surface: Surface,
    rect: pygame.Rect,
    color: Color = Color(0, 0, 255),
    thickness: int = 1,
) -> None:
    pygame.draw.rect(surface, color, rect, thickness)
