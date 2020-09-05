import pygame
import sys
from pygame.locals import *


pygame.init()
pygame.font.init()

game_list = []
fpsClock = pygame.time.Clock()
DISPLAY = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption(" Breakout Boom")
font = pygame.font.SysFont(None, 30)
font1 = pygame.font.SysFont(None, 20)
programIcon = pygame.image.load('Icon.ico')
pygame.display.set_icon(programIcon)


def block(pos_x, pos_y, width, height, color):
    global game_list
    pygame.draw.rect(DISPLAY, color, (pos_x, pos_y, width, height))
    game_list.append([pos_x, pos_y, width, height])


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    DISPLAY.blit(screen_text, [x, y])


def score_screen(text, color, x, y):
    screen_text = font1.render(text, True, color)
    DISPLAY.blit(screen_text, [x, y])


def game_loop():
    fps = 20
    WHITE = (255, 255, 255)
    lead_x = 260
    v_x = 0
    circle_x = lead_x+60
    circle_y = 456
    v_c_x = 0
    v_c_y = 0
    game_run = True
    game_over = False
    win = False
    global game_list
    score = 0

    blocks = [[True for i in range(5)] for j in range(10)]

    while game_run:
        if game_over == True or win == True:
            k = ""
            if (game_over == True):
                k = "Game Over! Press Enter To Play Again"
            elif (win == True):
                k = "You Won! Press Enter To Play Again"
            DISPLAY.fill((47, 47, 47))
            text_screen(k, WHITE, 130, 230)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        fps = 20
                        WHITE = (255, 255, 255)
                        lead_x = 260
                        v_x = 0
                        circle_x = lead_x+60
                        circle_y = 456
                        v_c_x = 0
                        v_c_y = 0
                        game_run = True
                        game_over = False
                        blocks = [[True for i in range(5)] for j in range(10)]
                        score = 0

        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_run = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        v_c_x = -10
                        v_c_y = -10

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                lead_x = max(0, lead_x-10)
            if keys[pygame.K_RIGHT]:
                lead_x = min(DISPLAY.get_width()-120, lead_x+10)

            circle_x += v_c_x
            circle_y += v_c_y
            lead_x += v_x

            ball_rect = pygame.Rect(circle_x-4, circle_y-4, 8, 8)
            lead_rect = pygame.Rect(lead_x, 460, 120, 10)
            display_rect = DISPLAY.get_rect()

            if ball_rect.colliderect(lead_rect):
                v_c_y = -abs(v_c_y)

            if ball_rect.left < display_rect.left or ball_rect.right > display_rect.right:
                v_c_x *= -1
            if ball_rect.top < display_rect.top:
                v_c_y *= -1
            if ball_rect.bottom > display_rect.bottom:
                game_over = True

            for i in range(5):
                for j in range(10):
                    if blocks[j][i]:
                        x_val, y_val = j * 64, 22 + i * 30
                        block_rect = pygame.Rect(x_val, y_val, 62, 20)
                        if block_rect.colliderect(ball_rect):
                            blocks[j][i] = False
                            v_c_y *= -1
                            score += 1
            cnt = 0
            for i in range(5):
                for j in range(10):
                    if (j == False):
                        cnt += 1
            if (cnt == 50):
                win = True

            DISPLAY.fill((47, 47, 47))
            pygame.draw.rect(DISPLAY, WHITE, (lead_x, 460, 120, 10))
            pygame.draw.circle(DISPLAY, WHITE, (circle_x, circle_y), 4)
            for i in range(5):
                for j in range(10):
                    if blocks[j][i]:
                        x_val, y_val = j * 64, 22 + i * 30
                        block(x_val, y_val, 62, 20, (255, 255, 255))
            st = "Score: {}".format(score)
            score_screen(st, WHITE, 5, 5)

        pygame.display.update()
        fpsClock.tick(fps)


game_loop()
