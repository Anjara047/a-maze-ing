#!/usr/bin/env

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

x = 100
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        x += 5

    screen.fill((0, 150, 200))

    pygame.draw.rect(screen, (255, 40, 0), (x, 30, 100, 50))

    pygame.display.update()
