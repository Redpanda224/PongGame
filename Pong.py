import pygame
from pygame import mixer
from pygame.locals import *
import random

pygame.init()

# Screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Classic Pong')
icon = pygame.image.load('Pong.png')
pygame.display.set_icon(icon)

# Variables
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
GREY = (40, 40, 40)
Color = (4, 2, 115)
moving = False
run = True
game_start = False
game_menu = True
player_score = 0
enemy_score = 0
circleX = 390
circleY = 300
ball_dx = 1.5
ball_dy = 1.5
paddle_speed = 1

# Imports
font1 = pygame.font.Font('Pixeltype.ttf', 100)
font2 = pygame.font.Font('Pixeltype.ttf', 50)
hit = pygame.mixer.Sound('hit.wav')
hit.set_volume(0.5)
grunt = pygame.mixer.Sound('grunt.mp3')
hit.set_volume(0.5)

# Rectangles
enemy = pygame.Rect(20, 250, 20, 100)
player = pygame.Rect(750, 250, 20, 100)
ball = pygame.Rect(circleX, circleY, 20, 20)

# BG Music
mixer.music.load('music.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Game Loop
while run:
    if not game_menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

            # Player Movement
            if event.type == MOUSEBUTTONDOWN:
                if player.collidepoint(event.pos):
                    moving = True
                    game_start = True

            elif event.type == MOUSEBUTTONUP:
                moving = False

            elif event.type == MOUSEMOTION and moving:
                player.move_ip(event.rel)

            # Player and Enemy Boundaries
            if player.right > WIDTH - 5:
                player.right = WIDTH - 5

            if player.left < WIDTH - 150:
                player.left = WIDTH - 150

            if player.top <= 5:
                player.top = 5

            if player.bottom > HEIGHT - 5:
                player.bottom = HEIGHT - 5

            if enemy.right > 150:
                enemy.right = 150

            if enemy.left < 5:
                enemy.left = 5

            if enemy.top <= 5:
                enemy.top = 5

            if enemy.bottom > HEIGHT - 5:
                enemy.bottom = HEIGHT - 5

        # Ball Movement
        if game_start:
            circleY += ball_dy
            circleX += ball_dx
            ball.center = (circleX, circleY)

            # Ball Collision
            if ball.colliderect(player):
                grunt.play()
                hit.play()
                ball_dx = -1.5
            if ball.colliderect(enemy):
                hit.play()
                ball_dx = 1.5
            if ball.right > WIDTH:
                enemy_score += 1
                ball_dx = -1.5
            if ball.left < 0:
                player_score += 1
                ball_dx = 1.5
            if ball.top <= 5:
                ball_dy = 1.5
            if ball.bottom >= HEIGHT - 5:
                ball_dy = -1.5

            # Enemy A.I
            if ball.x < 300:
                if enemy.bottom > ball.y:
                    enemy.bottom -= paddle_speed
                if enemy.y < ball.y:
                    enemy.top += paddle_speed

        # Board
        screen.fill("Black")
        pygame.draw.rect(screen, 'blue', player)
        pygame.draw.rect(screen, 'blue', enemy)
        middle_of_board = pygame.draw.rect(screen, GREY, (396, 0, 5, 800), 10)
        pygame.draw.circle(screen, 'white', ball.center, 15)
        player_score_text = font2.render(str(player_score), True, "white")
        enemy_score_text = font2.render(str(enemy_score), True, "white")

        # Blit Paddles
        screen.blit(player_score_text, (525, 100))
        screen.blit(enemy_score_text, (250, 100))

    # Game Menu
    if game_menu:
        if game_menu:
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        game_menu = False

            screen.fill((4, 2, 115))
            menu_mes1 = font1.render("CLASSIC PONG", False, "white")
            menu_mes2 = font2.render('press SPACE BAR to play!', False, "white")
            img = pygame.image.load('Pong.png').convert_alpha()
            screen.blit(img, (500, 350))
            screen.blit(menu_mes1, (100, 200))
            screen.blit(menu_mes2, (100, 300))

    # Update/FPS/Quit
    pygame.display.flip()
    clock.tick(150)
pygame.quit()
