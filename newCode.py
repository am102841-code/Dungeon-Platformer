elif game_state == 'tutorial_level':
    WINDOW.fill('lightblue')
    
    # Reset player for tutorial
    player.x = 100
    player.y = 500
    player.vel_y = 0
    
    # Tutorial obstacles
    ob1 = pygame.Rect(100, 450, 200, 50)   # ground platform
    ob2 = pygame.Rect(400, 350, 100, 20)   # middle platform
    ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
    obstacle_list = [ob1, ob2, ground]

    # Tutorial spike
    tutorial_spike = spike(50, 50)
    tutorial_spike.hitbox.topleft = (550, 500)
    spike_position_list = [tutorial_spike.hitbox]

    # Coin example
    coin1 = Coin(ob2.left + ob2.width // 2, ob2.top - 25)
    coin1.anim = coin_anim
    coin_list = [coin1]

    # Get input
    keys = pygame.key.get_pressed()
    player.vel_x = 0
    if keys[pygame.K_LEFT]:
        player.vel_x = -player.move_speed
        player.player_now = player.player_image
        player.facing_left = True
    if keys[pygame.K_RIGHT]:
        player.vel_x = player.move_speed
        player.player_now = player.player_flipped_image
        player.facing_left = False
    if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and player.on_ground:
        player.vel_y = player.jump_strength
        player.on_ground = False

    # Horizontal collision
    horizontal_collision(player, obstacle_list)

    # Gravity
    player.vel_y += player.gravity
    player.y += int(player.vel_y)
    player.x += player.vel_x
    player.hitbox.topleft = (player.x, player.y)

    # Vertical collision
    player.on_ground = False
    for ob in obstacle_list:
        if player.hitbox.colliderect(ob):
            if player.vel_y > 0 and player.hitbox.bottom - player.vel_y <= ob.top:
                player.y = ob.top - player.hitbox.height
                player.vel_y = 0
                player.on_ground = True
            elif player.vel_y < 0 and player.hitbox.top - player.vel_y >= ob.bottom:
                player.y = ob.bottom
                player.vel_y = 0

    # Spike collisions
    for sp in [tutorial_spike]:
        sp.collisions(player, spike_position_list)

    # Coin collisions
    for coin in coin_list:
        coin.collide(player.hitbox)

    # Render
    WINDOW.blit(background, (0, 0))
    for ob in obstacle_list:
        platform_img = pygame.transform.scale(platform, (ob.width, ob.height))
        WINDOW.blit(platform_img, ob.topleft)

    for sp in [tutorial_spike]:
        WINDOW.blit(sp.image, sp.hitbox.topleft)

    for coin in coin_list:
        coin.render_coin()

    WINDOW.blit(player.player_now, (player.x, player.y))
