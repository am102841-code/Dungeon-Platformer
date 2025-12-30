# Inside 'elif game_state == "skins":' block

# Load character images 
knight_img = pygame.image.load('KNIGHT.png').convert_alpha()
knight_img = pygame.transform.scale(knight_img, (120, 120))
wizard_img = pygame.image.load("WIZARD.png").convert_alpha()
wizard_img = pygame.transform.scale(wizard_img, (200, 200))

# Define hitboxes 
knight_hitbox = knight_img.get_rect(topleft=(125, 200))
wizard_hitbox = wizard_img.get_rect(topleft=(225, 200))

# Draw images
WINDOW.blit(knight_img, knight_hitbox.topleft)
WINDOW.blit(wizard_img, wizard_hitbox.topleft)

# Draw  labels
font = pygame.font.Font(None, 32)
knight_text = font.render("Knight", True, (0,0,0))
wizard_text = font.render("Wizard", True, (0,0,0))
WINDOW.blit(knight_text, (knight_hitbox.x + 15, knight_hitbox.y + 125))
WINDOW.blit(wizard_text, (wizard_hitbox.x + 15, wizard_hitbox.y + 125))

# Detect events 
mouse_x, mouse_y = pygame.mouse.get_pos()
mouse_clicked = False
for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_clicked = True

if mouse_clicked:
    if knight_hitbox.collidepoint(mouse_x, mouse_y):
        selected_character = 'knight'
        # Save choice, e.g., to a variable
    elif wizard_hitbox.collidepoint(mouse_x, mouse_y):
        selected_character = 'wizard'

# When starting gameplay, load the sprite based on selection
if selected_character == 'knight':
    player.player_image = pygame.image.load('KNIGHT.png').convert_alpha()
elif selected_character == 'wizard':
    player.player_image = pygame.image.load('WIZARD.png').convert_alpha()

# Make sure to draw the selected sprite during gameplay
