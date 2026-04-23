import pygame

def main():
    pygame.init()


    WIDTH, HEIGHT = 640, 480
    TOOLBAR_HEIGHT = 60  # высота верхней панели

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Paint")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    
    radius = 5  # толщина кисти
    mode = 'brush'  # текущий режим 
    color = (0, 0, 255)  # текущий цвет по умолчанию 

    drawing = False  #рисуем ли сейчас
    start_pos = None  #начальная точка для фигур

    
    screen.fill((0, 0, 0))

    
    while True:

        
        for event in pygame.event.get():

            
            if event.type == pygame.QUIT:
                return

            
            if event.type == pygame.KEYDOWN:

                # Режимы рисования
                if event.key == pygame.K_b:
                    mode = 'brush'   #кисть
                elif event.key == pygame.K_r:
                    mode = 'rect'    # прямоугол
                elif event.key == pygame.K_c:
                    mode = 'circle'  #круг
                elif event.key == pygame.K_e:
                    mode = 'eraser'  #ластик

                
                if event.key == pygame.K_1:
                    color = (255, 0, 0)  
                elif event.key == pygame.K_2:
                    color = (0, 255, 0)  
                elif event.key == pygame.K_3:
                    color = (0, 0, 255)  

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем чтобы не рисовать на панели
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

                    rect = pygame.Rect(x, y, w, h)
                    pygame.draw.rect(screen, color, rect, 2)

                #
                elif mode == 'circle':
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    radius_circle = int((dx**2 + dy**2) ** 0.5)

                    pygame.draw.circle(screen, color, start_pos, radius_circle, 2)

            
            if event.type == pygame.MOUSEMOTION and drawing:
                #рисуем только ниже панели
                if event.pos[1] > TOOLBAR_HEIGHT:

                    
                    if mode == 'brush':
                        pygame.draw.circle(screen, color, event.pos, radius)

                    # ластик рисует чёрным
                    elif mode == 'eraser':
                        pygame.draw.circle(screen, (0, 0, 0), event.pos, radius * 2)

        
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, WIDTH, TOOLBAR_HEIGHT))

        # Подсказки
        text1 = font.render("Modes: B-Brush  R-Rect  C-Circle  E-Eraser", True, (255, 255, 255))
        text2 = font.render("Colors: 1-Red  2-Green  3-Blue", True, (255, 255, 255))

        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 30))

        #текущий режим
        mode_text = font.render(f"Mode: {mode}", True, (255, 255, 0))
        screen.blit(mode_text, (400, 10))

        #текущий цвет
        color_text = font.render(f"Color: {color}", True, (255, 255, 0))
        screen.blit(color_text, (400, 30))

     
        pygame.display.flip()

       
        clock.tick(60)



main()