import pygame
import math  

def main():
    pygame.init()

    WIDTH, HEIGHT = 700, 600
    TOOLBAR_HEIGHT = 80
    THICKNESS = 5

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Paint")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    radius = THICKNESS
    mode = 'brush'
    color = (0, 0, 255)

    drawing = False
    start_pos = None

    screen.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                
                if event.key == pygame.K_b:
                    mode = 'brush'
                elif event.key == pygame.K_r:
                    mode = 'rect'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_s:
                    mode = 'square'     
                elif event.key == pygame.K_t:
                    mode = 'r_triangle' # прямоугольный треугольник
                elif event.key == pygame.K_y:
                    mode = 'e_triangle' 
                elif event.key == pygame.K_h:
                    mode = 'rhombus'    

                
                if event.key == pygame.K_1:
                    color = (255, 0, 0)
                elif event.key == pygame.K_2:
                    color = (0, 255, 0)
                elif event.key == pygame.K_3:
                    color = (0, 0, 255)

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > TOOLBAR_HEIGHT:
                    drawing = True
                    start_pos = event.pos

            
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                end_pos = event.pos

                
                if mode == 'rect':
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
                    size = max(abs(end_pos[0] - start_pos[0]),
                               abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(screen, color,
                                     (start_pos[0], start_pos[1], size, size), THICKNESS)

                
                elif mode == 'r_triangle':
                    points = [
                        start_pos,
                        (end_pos[0], start_pos[1]),
                        end_pos
                    ]
                    pygame.draw.polygon(screen, color, points, THICKNESS)

                
                elif mode == 'e_triangle':
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    side = abs(x2 - x1)

                    height = int((math.sqrt(3) / 2) * side)

                    points = [
                        (x1, y1),
                        (x1 + side, y1),
                        (x1 + side // 2, y1 - height)
                    ]

                    pygame.draw.polygon(screen, color, points, THICKNESS)

                
                elif mode == 'rhombus':
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    points = [
                        (cx, y1),  
                        (x2, cy),  
                        (cx, y2),  
                        (x1, cy)   #
                    ]

                    pygame.draw.polygon(screen, color, points, THICKNESS)

            
            if event.type == pygame.MOUSEMOTION and drawing:
                if event.pos[1] > TOOLBAR_HEIGHT:

                    if mode == 'brush':
                        pygame.draw.circle(screen, color, event.pos, radius)

                    elif mode == 'eraser':
                        pygame.draw.circle(screen, (0, 0, 0), event.pos, radius * THICKNESS)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS:  
                    THICKNESS += 1
                    radius = THICKNESS
                elif event.key == pygame.K_MINUS:  
                    THICKNESS = max(1, THICKNESS - 1)  
                    radius = THICKNESS
                

        
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, WIDTH, TOOLBAR_HEIGHT))

        text1 = font.render("B-Brush \ R-Rect \ C-Circle \ E-Eraser", True, (255, 255, 255))
        text2 = font.render("S-Square \ T-RTri \ Y-ETri \ H-Rhombus", True, (255, 255, 255))
        text3 = font.render("1-Red 2-Green 3-Blue", True, (255, 255, 255))

        screen.blit(text1, (10, 5))
        screen.blit(text2, (10, 25))
        screen.blit(text3, (10, 45))

        mode_text = font.render(f"Mode: {mode}", True, (255, 255, 0))
        screen.blit(mode_text, (400, 10))

        color_text = font.render(f"Color: {color}", True, (255, 255, 0))
        screen.blit(color_text, (400, 30))

        

        pygame.display.flip()
        clock.tick(60)


main()