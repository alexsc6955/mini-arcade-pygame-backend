"""
Render port implementation for the pygame backend.
Provides functionality to draw shapes and manage rendering state.
"""

from __future__ import annotations

import pygame
from mini_arcade_core.backend.utils import (  # pyright: ignore[reportMissingImports]
    rgba,
)
from mini_arcade_core.backend.viewport import ViewportTransform

from mini_arcade_pygame_backend.ports.window import WindowPort  # type: ignore


class RenderPort:
    """
    Render port for the Mini Arcade native backend.

    :param native_backend: The native backend instance.
    :type native_backend: native.Backend
    :param vp: The viewport transform.
    :type vp: ViewportTransform
    """

    def __init__(
        self,
        window: WindowPort,
        vp: ViewportTransform,
        background_color=(0, 0, 0),
    ):
        self._w = window
        self._vp = vp
        self._clear = rgba(background_color)

    def set_clear_color(self, r: int, g: int, b: int):
        """
        Set the clear color for the renderer.

        :param r: Red component (0-255).
        :type r: int
        :param g: Green component (0-255).
        :type g: int
        :param b: Blue component (0-255).
        :type b: int
        """
        self._clear = (int(r), int(g), int(b), 255)

    def begin_frame(self):
        """Begin a new rendering frame."""
        r, g, b, _ = self._clear
        self._w.screen.fill((r, g, b))

    def end_frame(self):
        """End the current rendering frame."""
        pygame.display.flip()

    def set_clip_rect(self, x: int, y: int, w: int, h: int):
        """
        Set the clipping rectangle.

        :param x: The x-coordinate of the clipping rectangle.
        :type x: int
        :param y: The y-coordinate of the clipping rectangle.
        :type y: int
        :param w: The width of the clipping rectangle.
        :type w: int
        :param h: The height of the clipping rectangle.
        :type h: int
        """
        # IMPORTANT: the pipeline passes viewport_w/h and assumes viewport
        # transform has been applied.
        self._w.screen.set_clip(pygame.Rect(int(x), int(y), int(w), int(h)))

    def clear_clip_rect(self):
        """Clear the clipping rectangle."""
        self._w.screen.set_clip(None)

    # Justification: Many arguments needed for drawing
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def draw_rect(self, x: int, y: int, w: int, h: int, color=(255, 255, 255)):
        """
        Draw a filled rectangle.

        :param x: The x-coordinate of the rectangle.
        :type x: int
        :param y: The y-coordinate of the rectangle.
        :type y: int
        :param w: The width of the rectangle.
        :type w: int
        :param h: The height of the rectangle.
        :type h: int
        :param color: The color of the rectangle as an (R, G, B) or (R, G, B, A) tuple.
        :type color: tuple[int, int, int] | tuple[int, int, int, int]
        """
        r, g, b, _ = rgba(color)
        sx, sy = self._vp.map_xy(int(x), int(y))
        sw, sh = self._vp.map_wh(int(w), int(h))
        # alpha: pygame.draw supports alpha only if surface has per-pixel alpha;
        # simplest: ignore alpha for now, or use a temp surface if you really need it.
        pygame.draw.rect(
            self._w.screen, (r, g, b), pygame.Rect(sx, sy, sw, sh)
        )

    def draw_line(
        self, x1: int, y1: int, x2: int, y2: int, color=(255, 255, 255)
    ):
        """
        Draw a line between two points.

        :param x1: The x-coordinate of the start point.
        :type x1: int
        :param y1: The y-coordinate of the start point.
        :type y1: int
        :param x2: The x-coordinate of the end point.
        :type x2: int
        :param y2: The y-coordinate of the end point.
        :type y2: int
        :param color: The color of the line as an (R, G, B) or (R, G, B, A) tuple.
        :type color: tuple[int, int, int] | tuple[int, int, int, int]
        """
        r, g, b, _ = rgba(color)
        sx1, sy1 = self._vp.map_xy(int(x1), int(y1))
        sx2, sy2 = self._vp.map_xy(int(x2), int(y2))
        pygame.draw.line(self._w.screen, (r, g, b), (sx1, sy1), (sx2, sy2))
