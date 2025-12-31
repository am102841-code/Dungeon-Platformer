selected_character = "wizard"

player = Player()

if selected_character == "wizard":
    player.player_now = wizard
    player.player_flipped_image = pygame.transform.flip(wizard, True, False)
elif selected_character == "knight":
    player.player_now = knight
    player.player_flipped_image = pygame.transform.flip(knight, True, False)


if hitbox.collidepoint((mouse_x, mouse_y)) and mouseClicked:
    selected_character = "knight"
    start_time = time.time()
    player.player_now = knight
    player.player_flipped_image = pygame.transform.flip(knight, True, False)
    show_message = True
    text = "Knight was selected!"

if hitbox2.collidepoint((mouse_x, mouse_y)) and mouseClicked:
    selected_character = "wizard"
    start_time2 = time.time()
    player.player_now = wizard
    player.player_flipped_image = pygame.transform.flip(wizard, True, False)
    show_message2 = True
    text2 = "Wizard was selected!"
