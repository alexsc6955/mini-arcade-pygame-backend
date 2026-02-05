from __future__ import annotations

import os
import sys
import pygame

this_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(this_dir, "..", "src"))
sys.path.insert(0, src_dir)

from mini_arcade_pygame_backend import Scene, GameConfig, run_game


class ExampleScene(Scene):
    def on_enter(self):
        print("ExampleScene: on_enter")

    def on_exit(self):
        print("ExampleScene: on_exit")

    def handle_event(self, event: object):
        # Narrow type for pygame
        if not isinstance(event, pygame.event.EventType):
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Ask the game to stop
                # (PygameGame defines stop(), even though the core base doesn’t)
                self.game.stop()

    def update(self, dt: float):
        # Just a no-op demo
        pass

    def draw(self, surface: object):
        if not isinstance(surface, pygame.Surface):
            return

        surface.fill((30, 30, 30))
        # Super minimal “hello world” text
        font = pygame.font.SysFont(None, 32)
        text = font.render("Mini Arcade Pygame Backend", True, (200, 200, 200))
        surface.blit(text, (40, 40))


if __name__ == "__main__":
    cfg = GameConfig(width=800, height=600, title="Mini Arcade · Pygame Backend")
    run_game(ExampleScene, config=cfg)
