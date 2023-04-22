import os
import sys
import pygame
import random
import subprocess
import numpy as np

eat_translations = {
    "Ting-Ting": "吃",
    "Kyoko": "食べる",
    "Yuna": "먹다",
    "Kanya": "กิน",
}

def get_available_voices():
    try:
        output = subprocess.check_output(["say", "-v", "?"])
        output = output.decode("utf-8")
        lines = output.strip().split("\n")
        voices = [line.split()[0] for line in lines]
        return voices
    except subprocess.CalledProcessError as e:
        print("Error getting available voices:", e)
        return []

voices = list(eat_translations.keys()) + np.random.choice(list(set(get_available_voices()) - set(eat_translations.keys())), size=5, replace=False).tolist()
print(voices)

def check_collision(pos_a, pos_b):
    return pos_a[0] == pos_b[0] and pos_a[1] == pos_b[1]

def valid_direction(new_direction, current_direction):
    if new_direction == "UP" and current_direction != "DOWN":
        return True
    if new_direction == "DOWN" and current_direction != "UP":
        return True
    if new_direction == "LEFT" and current_direction != "RIGHT":
        return True
    if new_direction == "RIGHT" and current_direction != "LEFT":
        return True
    return False

def draw_score(screen, score):
    font = pygame.font.SysFont("arial", 20)
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (WIDTH - 100, 10))

pygame.init()

WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

SNAKE_SIZE = 20
SNAKE_SPEED = 10
BASE_SPEED = 10
snake_pos = [[100, 50], [90, 50], [80, 50]]

FOOD_SIZE = 20
food_pos = [random.randrange(1, (WIDTH//20)) * 20, random.randrange(1, (HEIGHT//20)) * 20]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
running = True
direction = "RIGHT"
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            new_direction = None
            if event.key == pygame.K_UP:
                new_direction = "UP"
            if event.key == pygame.K_DOWN:
                new_direction = "DOWN"
            if event.key == pygame.K_LEFT:
                new_direction = "LEFT"
            if event.key == pygame.K_RIGHT:
                new_direction = "RIGHT"
            
            if new_direction and valid_direction(new_direction, direction):
                direction = new_direction

    if direction == "UP":
        new_pos = [snake_pos[0][0], snake_pos[0][1] - SNAKE_SPEED]
    if direction == "DOWN":
        new_pos = [snake_pos[0][0], snake_pos[0][1] + SNAKE_SPEED]
    if direction == "LEFT":
        new_pos = [snake_pos[0][0] - SNAKE_SPEED, snake_pos[0][1]]
    if direction == "RIGHT":
        new_pos = [snake_pos[0][0] + SNAKE_SPEED, snake_pos[0][1]]
    #os.system("say -v Alex move &")
    
    snake_pos.insert(0, new_pos)

    snake_head_rect = pygame.Rect(snake_pos[0][0], snake_pos[0][1], SNAKE_SIZE, SNAKE_SIZE)
    food_rect = pygame.Rect(food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE)

    if snake_head_rect.colliderect(food_rect):
        food_pos = [random.randrange(1, (WIDTH//20)) * 20, random.randrange(1, (HEIGHT//20)) * 20]
        score += 1
        random_voice = random.choice(voices)
        translation = eat_translations.get(random_voice, "eat")  # Default to "eat" if the voice is not in the dictionary
        os.system(f"say -v {random_voice} {translation} &")
    else:
        snake_pos.pop()

    screen.fill(WHITE)

    for pos in snake_pos:
        snake_rect = pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE)
        pygame.draw.rect(screen, GREEN, snake_rect)

    food_rect = pygame.Rect(food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE)
    pygame.draw.rect(screen, RED, food_rect)

    if snake_pos[0][0] < 0 or snake_pos[0][0] > WIDTH - SNAKE_SIZE or snake_pos[0][1] < 0 or snake_pos[0][1] > HEIGHT - SNAKE_SIZE:
        running = False
        os.system("say -v Alex dead &")

    if snake_pos[0] in snake_pos[1:]:
        running = False
        os.system("say -v Alex dead &")

    draw_score(screen, score)

    pygame.display.flip()
    speed = BASE_SPEED + int(score / 5)
    clock.tick(speed)

pygame.quit()
sys.exit()


