import pygame
import json
import os

pygame.init()

# Window setup
WIDTH, HEIGHT = 500, 400
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JSON Save Practice")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player setup
player = {"x": 50, "y": 50, "coins": 0}
player_size = 50

# Coin setup
coin = {"x": 300, "y": 200, "collected": False, "size": 30}

# Save file
SAVE_FILE = "player_save.json"

# Load saved data if it exists
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        saved_data = json.load(f)
        player.update(saved_data)

running = True
while running:
    clock.tick(FPS)
    WINDOW.fill(WHITE)

    # Draw coin if not collected
    if not coin["collected"]:
        pygame.draw.rect(WINDOW, YELLOW, (coin["x"], coin["y"], coin["size"], coin["size"]))

    # Draw player
    pygame.draw.rect(WINDOW, BLUE, (player["x"], player["y"], player_size, player_size))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save progress before quitting
            with open(SAVE_FILE, "w") as f:
                json.dump({"x": player["x"], "y": player["y"], "coins": player["coins"]}, f)
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player["x"] -= 5
    if keys[pygame.K_RIGHT]:
        player["x"] += 5
    if keys[pygame.K_UP]:
        player["y"] -= 5
    if keys[pygame.K_DOWN]:
        player["y"] += 5

    # Coin collision
    player_rect = pygame.Rect(player["x"], player["y"], player_size, player_size)
    coin_rect = pygame.Rect(coin["x"], coin["y"], coin["size"], coin["size"])
    if player_rect.colliderect(coin_rect) and not coin["collected"]:
        coin["collected"] = True
        player["coins"] += 1
        print(f"Coins collected: {player['coins']}")

    pygame.display.update()

pygame.quit()
