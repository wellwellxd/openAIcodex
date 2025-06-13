"""roguelike.input

Translate pygame events to Engine actions.
"""

from __future__ import annotations

import pygame


class InputHandler:
    """Handles keyboard input via pygame."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1, 1))

    def get_action(self) -> str | None:
        """Return action string from pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
                if event.key in (pygame.K_UP, pygame.K_k):
                    return "UP"
                if event.key in (pygame.K_DOWN, pygame.K_j):
                    return "DOWN"
                if event.key in (pygame.K_LEFT, pygame.K_h):
                    return "LEFT"
                if event.key in (pygame.K_RIGHT, pygame.K_l):
                    return "RIGHT"
        return None
