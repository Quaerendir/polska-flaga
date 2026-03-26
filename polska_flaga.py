#!/usr/bin/env python3
"""
polska_flaga.py — animowana flaga Polski
Quaerendir

Sterowanie:
  +  /  =     — przyspiesz
  -           — zwolnij
  F  / F11    — przełącz pełny ekran
  ESC / Q     — wyjście
"""

import sys
import pygame

# ── kolory ──────────────────────────────────────────────────────────────────
WHITE  = (255, 255, 255)
RED    = (220,  20,  60)   # Crimson — bliżej oryginału niż pure red
BG     = ( 20,  20,  30)   # ciemne tło żeby flaga "wisiała w powietrzu"

# ── rozmiar flagi (proporcja 5:8 jak oficjalna) ──────────────────────────────
FLAG_W = 640
FLAG_H = 400

# ── prędkość startowa i jej granice ─────────────────────────────────────────
SPEED_DEFAULT = 4.0
SPEED_MIN     = 0.5
SPEED_MAX     = 30.0
SPEED_STEP    = 0.5

# ── delikatny cień pod flagą ─────────────────────────────────────────────────
SHADOW_COLOR  = (0, 0, 0, 120)   # RGBA — użyjemy surface z alpha


def draw_flag(surface: pygame.Surface) -> None:
    """Rysuj flagę PL na podanej surface (FLAG_W x FLAG_H)."""
    half = FLAG_H // 2
    # górny pas — biały
    pygame.draw.rect(surface, WHITE, (0, 0,    FLAG_W, half))
    # dolny pas — czerwony
    pygame.draw.rect(surface, RED,   (0, half, FLAG_W, FLAG_H - half))


def make_flag_surface() -> pygame.Surface:
    surf = pygame.Surface((FLAG_W, FLAG_H))
    draw_flag(surf)
    return surf


def make_shadow_surface() -> pygame.Surface:
    surf = pygame.Surface((FLAG_W + 20, FLAG_H + 20), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    pygame.draw.rect(surf, SHADOW_COLOR, (10, 14, FLAG_W, FLAG_H), border_radius=2)
    return surf


def speed_label(speed: float) -> str:
    return f"prędkość: {speed:.1f}x"


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Flaga Polski")

    info   = pygame.display.Info()
    sw, sh = info.current_w, info.current_h

    fullscreen = True
    screen = pygame.display.set_mode((sw, sh), pygame.FULLSCREEN)

    clock      = pygame.time.Clock()
    flag_surf  = make_flag_surface()
    shadow_surf = make_shadow_surface()

    # pozycja startowa — wyśrodkowana
    fx = float((sw - FLAG_W) // 2)
    fy = float((sh - FLAG_H) // 2)

    speed  = SPEED_DEFAULT
    dx     = speed
    dy     = speed * 0.6   # lekko ukośny ruch jak w starych dem

    font_big   = pygame.font.SysFont("monospace", 22, bold=True)
    font_small = pygame.font.SysFont("monospace", 15)

    show_hint  = True
    hint_timer = 300   # klatek

    running = True
    while running:
        # ── eventy ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False

                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS,
                                   pygame.K_KP_PLUS):
                    speed = min(speed + SPEED_STEP, SPEED_MAX)
                    _rescale_velocity()

                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    speed = max(speed - SPEED_STEP, SPEED_MIN)
                    _rescale_velocity()

                elif event.key in (pygame.K_f, pygame.K_F11):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(
                            (sw, sh), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((sw, sh))

        # lokalna funkcja żeby nie przekazywać zmiennych przez stos
        def _rescale_velocity():
            nonlocal dx, dy
            mag = (dx*dx + dy*dy) ** 0.5
            if mag > 0:
                dx = dx / mag * speed
                dy = dy / mag * speed * 0.6

        _rescale_velocity()

        # ── fizyka odbicia ───────────────────────────────────────────────────
        fx += dx
        fy += dy

        if fx <= 0:
            fx = 0.0
            dx = abs(dx)
        elif fx + FLAG_W >= sw:
            fx = float(sw - FLAG_W)
            dx = -abs(dx)

        if fy <= 0:
            fy = 0.0
            dy = abs(dy)
        elif fy + FLAG_H >= sh:
            fy = float(sh - FLAG_H)
            dy = -abs(dy)

        ix, iy = int(fx), int(fy)

        # ── rysowanie ────────────────────────────────────────────────────────
        screen.fill(BG)

        # cień
        screen.blit(shadow_surf, (ix - 5, iy - 4))

        # flaga
        screen.blit(flag_surf, (ix, iy))

        # ramka
        pygame.draw.rect(screen, (180, 180, 180),
                         (ix, iy, FLAG_W, FLAG_H), 1)

        # HUD — prędkość
        spd_surf = font_big.render(speed_label(speed), True, (200, 200, 200))
        screen.blit(spd_surf, (12, 10))

        # podpowiedź klawiszy (zanika po chwili)
        if hint_timer > 0:
            hint_timer -= 1
            alpha = min(255, hint_timer * 4)
            hint_lines = [
                "+/=  przyspiesz",
                "-    zwolnij",
                "F    pełny ekran",
                "ESC  wyjście",
            ]
            yoff = sh - len(hint_lines) * 22 - 15
            for line in hint_lines:
                ts = font_small.render(line, True, (160, 160, 160))
                ts.set_alpha(alpha)
                screen.blit(ts, (12, yoff))
                yoff += 22

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
