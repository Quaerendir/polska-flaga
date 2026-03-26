#!/usr/bin/env python3
"""
polska_flaga.py — animowana flaga Polski
Quaerendir

Sterowanie:
  +  /  =     — przyspiesz
  -           — zwolnij
  F  / F11    — przełącz pełny ekran / okno
  ESC / Q     — wyjście
"""

import sys

# ── Windows DPI awareness — MUSI być przed pygame.init() ────────────────────
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)   # Per-monitor V2
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()    # fallback WinXP+
        except Exception:
            pass

import pygame

# ── kolory ───────────────────────────────────────────────────────────────────
WHITE  = (255, 255, 255)
RED    = (220,  20,  60)
BG     = ( 20,  20,  30)
SHADOW = (  0,   0,   0, 110)

# ── rozmiar flagi (proporcja 5:8) ────────────────────────────────────────────
FLAG_W = 640
FLAG_H = 400

# ── prędkość ─────────────────────────────────────────────────────────────────
SPEED_DEFAULT = 4.0
SPEED_MIN     = 0.5
SPEED_MAX     = 30.0
SPEED_STEP    = 0.5


def make_flag_surface() -> pygame.Surface:
    surf = pygame.Surface((FLAG_W, FLAG_H))
    half = FLAG_H // 2
    pygame.draw.rect(surf, WHITE, (0, 0,    FLAG_W, half))
    pygame.draw.rect(surf, RED,   (0, half, FLAG_W, FLAG_H - half))
    return surf


def make_shadow_surface() -> pygame.Surface:
    surf = pygame.Surface((FLAG_W + 20, FLAG_H + 20), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    pygame.draw.rect(surf, SHADOW, (10, 14, FLAG_W, FLAG_H), border_radius=2)
    return surf


def rescale_velocity(dx: float, dy: float, speed: float):
    mag = (dx * dx + dy * dy) ** 0.5
    if mag > 0:
        return dx / mag * speed, dy / mag * speed * 0.6
    return dx, dy


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Flaga Polski")

    # (0, 0) + FULLSCREEN — pygame pobiera rozdzielczość pulpitu samodzielnie,
    # bez wcześniejszego display.Info() które na Windowsie z DPI scaling
    # zwraca błędne wartości przed pierwszym set_mode()
    screen     = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    sw, sh     = screen.get_size()
    fullscreen = True

    clock       = pygame.time.Clock()
    flag_surf   = make_flag_surface()
    shadow_surf = make_shadow_surface()

    fx    = float((sw - FLAG_W) // 2)
    fy    = float((sh - FLAG_H) // 2)
    speed = SPEED_DEFAULT
    dx    = speed
    dy    = speed * 0.6

    font_big   = pygame.font.SysFont("monospace", 22, bold=True)
    font_small = pygame.font.SysFont("monospace", 15)
    hint_timer = 300

    WIN_W, WIN_H = 1280, 720

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False

                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS,
                                   pygame.K_KP_PLUS):
                    speed = min(speed + SPEED_STEP, SPEED_MAX)
                    dx, dy = rescale_velocity(dx, dy, speed)

                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    speed = max(speed - SPEED_STEP, SPEED_MIN)
                    dx, dy = rescale_velocity(dx, dy, speed)

                elif event.key in (pygame.K_f, pygame.K_F11):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(
                            (0, 0), pygame.FULLSCREEN)
                        sw, sh = screen.get_size()
                    else:
                        screen = pygame.display.set_mode(
                            (WIN_W, WIN_H), pygame.RESIZABLE)
                        sw, sh = WIN_W, WIN_H
                    flag_surf   = make_flag_surface()
                    shadow_surf = make_shadow_surface()

        # ── fizyka ───────────────────────────────────────────────────────────
        fx += dx
        fy += dy

        if fx <= 0:
            fx, dx = 0.0, abs(dx)
        elif fx + FLAG_W >= sw:
            fx, dx = float(sw - FLAG_W), -abs(dx)

        if fy <= 0:
            fy, dy = 0.0, abs(dy)
        elif fy + FLAG_H >= sh:
            fy, dy = float(sh - FLAG_H), -abs(dy)

        ix, iy = int(fx), int(fy)

        # ── rysowanie ────────────────────────────────────────────────────────
        screen.fill(BG)
        screen.blit(shadow_surf, (ix - 5, iy - 4))
        screen.blit(flag_surf,   (ix, iy))
        pygame.draw.rect(screen, (180, 180, 180), (ix, iy, FLAG_W, FLAG_H), 1)

        spd_surf = font_big.render(f"prędkość: {speed:.1f}x", True, (200, 200, 200))
        screen.blit(spd_surf, (12, 10))

        if hint_timer > 0:
            hint_timer -= 1
            alpha = min(255, hint_timer * 4)
            hints = ["+/=  przyspiesz", "-    zwolnij",
                     "F    pełny ekran", "ESC  wyjście"]
            yoff  = sh - len(hints) * 22 - 15
            for line in hints:
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
