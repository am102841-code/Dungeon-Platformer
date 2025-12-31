import pygame
import json
import sys
import random

pygame.init()

# Window
WIDTH, HEIGHT = 500, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JSON Save/Load Practice")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Player
player = pygame.Rect(50, 300, 50, 50)
player_speed = 5

# Coin
coin = pygame.Rect(random.randint(0, WIDTH-30), random.randint(0, HEIGHT-30), 30, 30)
coins_collected = 0

# JSON save/load functions
def save_game():
    data = {
        "player_x": player.x,
        "player_y": player.y,
        "coins_collected": coins_collected
    }
    with open("mock_save.json", "w") as f:
        json.dump(data, f)

def load_game():
    global coins_collected
    try:
        with open("mock_save.json", "r") as f:
            data = json.load(f)
            player.x = data["player_x"]
            player.y = data["player_y"]
            coins_collected = data["coins_collected"]
    except FileNotFoundError:
        pass

load_game()

# Main loop
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    WIN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed
    if keys[pygame.K_s]:
        save_game()
    if keys[pygame.K_l]:
        load_game()

    # Coin collision
    if player.colliderect(coin):
        coins_collected += 1
        coin.x = random.randint(0, WIDTH-30)
        coin.y = random.randint(0, HEIGHT-30)

    # Draw
    pygame.draw.rect(WIN, RED, player)
    pygame.draw.rect(WIN, YELLOW, coin)
    font = pygame.font.Font(None, 32)
    text = font.render(f"Coins: {coins_collected}", True, (0,0,0))
    WIN.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()
sys.exit()
