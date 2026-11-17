import pygame
import random

pygame.init()

WIDTH, HEIGHT = 700, 500
FPS = 60
BALL_SPEED_X, BALL_SPEED_Y = 5, 4
PADDLE_SPEED = 7
PADDLE_W, PADDLE_H = 20, 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Пинг-понг')
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 35, bold=True)

'''Ракетки'''
p1 = pygame.Rect(30, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)   # левая
p2 = pygame.Rect(WIDTH - 30 - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)  # правая

'''Мяч'''
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
ball_dx = BALL_SPEED_X * random.choice((1, -1))
ball_dy = BALL_SPEED_Y * random.choice((1, -1))

score1, score2 = 0, 0

def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_dx = BALL_SPEED_X * random.choice((1, -1))
    ball_dy = BALL_SPEED_Y * random.choice((1, -1))

def draw_lose_message():
    text = font.render('Вы пропустили мяч', True, (200, 0, 0))
    hint = font.render('Чтобы начать нажмите SPACE', True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

def pause_after_lose():
    draw_lose_message()
    pygame.display.flip()
    pygame.time.delay(300)
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                waiting = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and p1.top > 0:
        p1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and p1.bottom < HEIGHT:
        p1.y += PADDLE_SPEED
    if keys[pygame.K_UP] and p2.top > 0:
        p2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and p2.bottom < HEIGHT:
        p2.y += PADDLE_SPEED

    ball.x += ball_dx
    ball.y += ball_dy

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    if ball.colliderect(p1) and ball_dx < 0:
        ball_dx *= -1
    if ball.colliderect(p2) and ball_dx > 0:
        ball_dx *= -1

    if ball.right > WIDTH:
        score2 += 1
        pause_after_lose()
        reset_ball()
    if ball.left < 0:
        score1 += 1
        pause_after_lose()
        reset_ball()

    screen.fill((173, 216, 230))
    pygame.draw.rect(screen, (0, 0, 0), p1)
    pygame.draw.rect(screen, (0, 0, 0), p2)
    pygame.draw.circle(screen, (154, 205, 50), ball.center, 10)
    pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    s1 = font.render(str(score1), True, (0, 0, 0))
    s2 = font.render(str(score2), True, (0, 0, 0))
    screen.blit(s1, s1.get_rect(center=(WIDTH // 2 - 60, 40)))
    screen.blit(s2, s2.get_rect(center=(WIDTH // 2 + 60, 40)))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()