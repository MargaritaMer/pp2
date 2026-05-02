import pygame
import math
import datetime
from tools import flood_fill
import os

def main():
    pygame.init()

    WIDTH, HEIGHT = 700, 600
    TOOLBAR_HEIGHT = 80

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS2 Paint")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    THICKNESS = 5
    color = (0, 0, 255)
    mode = 'pencil'

    drawing = False
    start_pos = None
    last_pos = None
    temp_surface = None

    text_mode = False
    input_text = ""
    text_pos = (0, 0)

    screen.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    text_mode = False
                    input_text = ""

                if event.key == pygame.K_b:
                    mode = 'pencil'
                elif event.key == pygame.K_l:
                    mode = 'line'
                elif event.key == pygame.K_r:
                    mode = 'rect'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_u:
                    mode = 'square'
                elif event.key == pygame.K_t:
                    mode = 'triangle'
                elif event.key == pygame.K_y:
                    mode = 'eq_triangle'
                elif event.key == pygame.K_h:
                    mode = 'rhombus'
                elif event.key == pygame.K_f:
                    mode = 'fill'
                elif event.key == pygame.K_x:
                    mode = 'text'

                elif event.key == pygame.K_4:
                    color = (255, 0, 0)
                elif event.key == pygame.K_5:
                    color = (0, 255, 0)
                elif event.key == pygame.K_6:
                    color = (0, 0, 255)

                elif event.key == pygame.K_1:
                    THICKNESS = 2
                elif event.key == pygame.K_2:
                    THICKNESS = 5
                elif event.key == pygame.K_3:
                    THICKNESS = 10

                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if not os.path.exists("assets"):
                        os.makedirs("assets")
                    filename = datetime.datetime.now().strftime("assets/drawing_%Y%m%d_%H%M%S.png")
                    pygame.image.save(screen, filename)
                    print("Saved to:", filename)

                if text_mode:
                    if event.key == pygame.K_RETURN:
                        text_surface = font.render(input_text, True, color)
                        screen.blit(text_surface, text_pos)
                        text_mode = False
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key != pygame.K_ESCAPE:
                        input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > TOOLBAR_HEIGHT:
                    if mode == 'fill':
                        flood_fill(screen, event.pos[0], event.pos[1], color)
                    elif mode == 'text':
                        text_mode = True
                        input_text = ""
                        text_pos = event.pos
                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos
                        temp_surface = screen.copy()

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                end_pos = event.pos

                if start_pos is None:
                    continue

                if mode == 'line':
                    pygame.draw.line(screen, color, start_pos, end_pos, THICKNESS)

                elif mode == 'rect':
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(end_pos[0] - start_pos[0])
                    h = abs(end_pos[1] - start_pos[1])
                    pygame.draw.rect(screen, color, (x, y, w, h), THICKNESS)

                elif mode == 'circle':
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    r = int((dx**2 + dy**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, r, THICKNESS)

                elif mode == 'square':
                    size = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(screen, color, (start_pos[0], start_pos[1], size, size), THICKNESS)

                elif mode == 'triangle':
                    points = [start_pos, (end_pos[0], start_pos[1]), end_pos]
                    pygame.draw.polygon(screen, color, points, THICKNESS)

                elif mode == 'eq_triangle':
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    side = abs(x2 - x1)
                    if side < 1:
                        side = 1
                    height = int(side * 0.866)
                    if x2 >= x1:
                        points = [
                            (x1, y1),
                            (x1 + side, y1),
                            (x1 + side // 2, y1 - height)
                        ]
                    else:
                        points = [
                            (x2, y2),
                            (x2 + side, y2),
                            (x2 + side // 2, y2 - height)
                        ]
                    pygame.draw.polygon(screen, color, points, THICKNESS)

                elif mode == 'rhombus':
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                    pygame.draw.polygon(screen, color, points, THICKNESS)

            if event.type == pygame.MOUSEMOTION and drawing:
                if event.pos[1] > TOOLBAR_HEIGHT:
                    if mode == 'pencil':
                        pygame.draw.line(screen, color, last_pos, event.pos, THICKNESS)
                        last_pos = event.pos
                    elif mode == 'eraser':
                        pygame.draw.circle(screen, (0, 0, 0), event.pos, THICKNESS)
                    elif mode == 'line':
                        screen.blit(temp_surface, (0, 0))
                        pygame.draw.line(screen, color, start_pos, event.pos, THICKNESS)
                    elif mode == 'rect':
                        screen.blit(temp_surface, (0, 0))
                        x = min(start_pos[0], event.pos[0])
                        y = min(start_pos[1], event.pos[1])
                        w = abs(event.pos[0] - start_pos[0])
                        h = abs(event.pos[1] - start_pos[1])
                        pygame.draw.rect(screen, color, (x, y, w, h), THICKNESS)
                    elif mode == 'circle':
                        screen.blit(temp_surface, (0, 0))
                        dx = event.pos[0] - start_pos[0]
                        dy = event.pos[1] - start_pos[1]
                        r = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.circle(screen, color, start_pos, r, THICKNESS)
                    elif mode == 'square':
                        screen.blit(temp_surface, (0, 0))
                        size = max(abs(event.pos[0] - start_pos[0]), abs(event.pos[1] - start_pos[1]))
                        pygame.draw.rect(screen, color, (start_pos[0], start_pos[1], size, size), THICKNESS)
                    elif mode == 'triangle':
                        screen.blit(temp_surface, (0, 0))
                        points = [start_pos, (event.pos[0], start_pos[1]), event.pos]
                        pygame.draw.polygon(screen, color, points, THICKNESS)
                    elif mode == 'eq_triangle':
                        screen.blit(temp_surface, (0, 0))
                        x1, y1 = start_pos
                        x2, y2 = event.pos
                        side = abs(x2 - x1)
                        if side < 1:
                            side = 1
                        height = int(side * 0.866)
                        if x2 >= x1:
                            points = [
                                (x1, y1),
                                (x1 + side, y1),
                                (x1 + side // 2, y1 - height)
                            ]
                        else:
                            points = [
                                (x2, y2),
                                (x2 + side, y2),
                                (x2 + side // 2, y2 - height)
                            ]
                        pygame.draw.polygon(screen, color, points, THICKNESS)
                    elif mode == 'rhombus':
                        screen.blit(temp_surface, (0, 0))
                        x1, y1 = start_pos
                        x2, y2 = event.pos
                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2
                        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                        pygame.draw.polygon(screen, color, points, THICKNESS)

        pygame.draw.rect(screen, (50, 50, 50), (0, 0, WIDTH, TOOLBAR_HEIGHT))

        screen.blit(font.render("B-pencil L-line R-rect C-circle Y-eq_tri", True, (255,255,255)), (10, 5))
        screen.blit(font.render("F-fill X-text U-square T-tri H-rhombus E-eraser", True, (255,255,255)), (10, 25))
        screen.blit(font.render("1/2/3-size 4/5/6-red/green/blue Ctrl+S-save", True, (255,255,255)), (10, 45))

        screen.blit(font.render(f"Mode: {mode}", True, (255,255,0)), (450, 10))
        screen.blit(font.render(f"Size: {THICKNESS}", True, (255,255,0)), (450, 30))

        if text_mode:
            preview = font.render(input_text, True, color)
            screen.blit(preview, text_pos)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()