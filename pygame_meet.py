import random

import pygame

fps = 30

# запуск
pygame.init()
clock = pygame.time.Clock()


screen = pygame.display.set_mode((500, 500)) # размер экрана
pygame.display.set_caption("?") # название окна


screen.fill((255, 255, 255)) # заливка

pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, 100)) # квадрат
pygame.draw.circle(screen, (0, 0, 0), (150, 150), 50, 50) # круг
pygame.draw.polygon(screen, (0, 0, 0), ((200, 200), (300, 200), (300, 300))) # другое

pygame.display.flip() # отобразить изменения


# нужные циклы

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    #pygame.display.flip()

pygame.quit() # выход