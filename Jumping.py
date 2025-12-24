import pygame, sys, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()
# IDEAS: powerups ; text ; levels ; make horizontal collisions ; borders ; portal ;

# Score counter

# LOG
# finished level counter 9/17
# made coins w/ random coins 9/17
# score counter 10/1
# health bar 11/28
# tutorial level completed 11/28

# Make levels and fix attack animation
# First Level --> random generated position of obstacles
# Next Levels --> same layout, but each level gets harder

# Add Spike Collisions and finish player class


# Colours
BACKGROUND = (255, 255, 255)
OBSTACLE_COLOR = (0, 0, 0)
PLAYER_COLOR = (0, 199, 255)
TEXT_COLOR = (200, 100, 0)
CREATOR_COLOR = (153, 204, 255)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
level = 1

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Platformer')

clock = pygame.time.Clock()

background = pygame.image.load('background.png').convert_alpha()
background = pygame.transform.scale(background, (800, 600))
platform = pygame.image.load('PLATFORM.png').convert_alpha()

# music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

tutorial_initialized = False


class Player():
    def __init__(self):
        self.x = 250
        self.y = 450
        self.player_image = pygame.image.load('KNIGHT.png').convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (65, 65))
        self.player_flipped_image = pygame.transform.flip(self.player_image, True, False)
        self.vel_y = 0
        self.vel_x = 0
        self.player_now = self.player_image
        # self.jump_strength = -21.5
        self.jump_strength = -20.67676767
        self.gravity = 1
        self.jump_speed = 0
        self.move_speed = 4
        self.on_ground = False
        self.player_reset = False
        # self.player_hitbox = pygame.Rect(150, 450, 65, 65)
        self.hitbox = self.player_image.get_rect()
        self.player_color = (245, 0, 0)
        self.facing_left = True
        self.health = 10
        self.max_health = 10
        self.width = 50
        self.height = 50
        # add collision, gravity, and other code to the player class


class spike():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.image = pygame.image.load("SPIKE.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.hitbox.topleft = (self.x, self.y)

    def collisions(self, player):
        if self.hitbox.colliderect(player.hitbox):
            player.health -= 1
            player.x = 100
            player.y = 500
            player.hitbox.topleft = (player.x, player.y)


class Enemy():
    def __init__(self):
        self.x = 200
        self.y = 200
        self.move_speed = 4
        self.on_ground = False
        self.health = 5
        self.player_rect = pygame.Rect(self.x, self.y, 65 / 2, 65 / 2)
        self.facing_left = True

"""
class spike():
    def __init__(self, width, height, x, y):
        self.image = pygame.image.load('SPIKE.png').convert_alpha()
        # self.color = color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # self.hitbox = pygame.Rect(300,300, 10, 25).inflate(50,50)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        # moving hitbox to middle, making it thin and keeping same height

    def collisions(self, player):
        if player.hitbox.collderect(self.hitbox): 
            if player.facing_left:
                player.x += 10 
            else: 
                player.x -= 10 
            player.health -= 1 
            player.x = 250 
            player.y = 450 
"""

class level_counter():
    def __init__(self, number):
        self.number = number

    def text(self):
        fontObj = pygame.font.Font(None, 32)
        textSufaceObj = fontObj.render("Level " + str(self.number), True, TEXT_COLOR, None)
        return textSufaceObj

    def set_number(self, newNumber):
        self.number = newNumber


class score_counter():
    def __init__(self):
        pass

    def text(self, coin_list):
        score = 0
        for coin in coin_list:
            if coin.collected:  # Checks if coin is collected
                score += 1
        fontObj = pygame.font.Font(None, 32)
        textSufaceObj = fontObj.render("Points: " + str(score), True, TEXT_COLOR, None)
        return textSufaceObj


# pygame.draw.circle(surface, color, center_coordinates, radius, width=0)

# sprite sheet?
# spinning coin
# spilt sprite sheet
# fix sheet

class coin_animation():
    def __init__(self, path, fw, fh, fps=10):
        self.sprite_sheet = pygame.image.load(path).convert_alpha()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (25, 25))
        self.frames = []
        self.frame_index = 0
        self.last_time = pygame.time.get_ticks()
        self.frame_duration = 1000 / fps
        self.fw = fw
        self.fh = fh

        width, height = self.sprite_sheet.get_size()

        # Loop through sprite sheet to slice into frames
        for y in range(0, height, fh):
            for x in range(0, width, fw):
                # Check if rectangle is within sprite sheet
                if x + fw <= width and y + fh <= height:
                    rect = pygame.Rect(x, y, fw, fh)
                    self.frames.append(self.sprite_sheet.subsurface(rect))
                else:
                    # Skip if rectangle exceeds bounds
                    pass

    def get_frame(self):
        if not self.frames:
            return None  # or a default surface
        now = pygame.time.get_ticks()
        if now - self.last_time > self.frame_duration:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_time = now
        return self.frames[self.frame_index]


# Score counter
# When player collides --> coin dissapears and score goes up by 1


class TitleAnimation():
    def __init__(self, text, x, y, color, color_change, starting_color, speed, reverse):
        self.text = 'Platformer'
        self.x = x
        self.y = y
        self.color = color
        self.color_change = color_change
        self.starting_color = starting_color
        self.speed = speed
        self.reverse = False


class Coin():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.anim = None  # Will be assigned externally
        self.RECT = pygame.Rect(0, 0, 15, 15)

    def get_hitbox(self):
        return self.RECT.move(self.x, self.y)

    def render_coin(self):
        if not self.collected and self.anim:
            current_frame = self.anim.get_frame()
            if current_frame:
                self._blit_frame(current_frame)

    def collide(self, playerHitbox):
        if self.get_hitbox().colliderect(playerHitbox) and self.collected == False:
            self.collected = True

    def randomize_pos(self):
        self.x = self.x + random.randint(-30, 30)


# starting,
class button():
    def __init__(self, x, y, width, height, color, text, state):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.state = 'Normal'
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def render_button(self):
        pygame.draw.rect(WINDOW, self.color, self.hitbox, 0, 5)




# Horizontal Collisions
def horizontal_collision(player, Obstacle_list):
    for x in Obstacle_list:
        if player.hitbox.colliderect(x):
            if player.vel_x > 0:
                player.hitbox.right = x.left
            elif player.vel_x < 0:
                player.hitbox.left = x.right


"""
def secret_horizontal_collision(player, secret_obstacle_list):
    for x in secret_obstacle_list:
        if player.hitbox.colliderect(x):
            if player.vel_x > 0:
                player.hitbox.right = x.left
            elif player.vel_x < 0:
                player.hitbox.left = x.right
"""

coin_anim = coin_animation('Coin.png', 32, 32, 10)
tutorial_initialized = False
exit_button_rect = pygame.Rect(WINDOW_WIDTH - 125, 50, 100, 100)
spikes = []

# The main function that controls the game
def main():
    looping = True

    global level
    global WINDOW
    global background
    global secret_obstacle_list

    tutorial_initialized = False

    ### Player Setup ###
    '''
    player = pygame.Rect(150, 450, 65, 65)
    player_image = pygame.image.load('image (3).png').convert_alpha()
    player_image = pygame.transform.scale(player_image, (65, 65))
    player_flipped = pygame.transform.flip(player_image, True, False)
    player_now = player_image

    player_vel_y = 0
    player_vel_x = 0
    jump_strength = -21.5
    gravity = 1
    jump_speed = 0
    move_speed = 4
    on_ground = False
    player_color = (245, 0, 0)
    '''

    player = Player()
    ### Obstacle Setup ###
    enemy = Enemy()
    ob2X = random.randint(550, 575)
    ob2Y = random.randint(250, 275)
    obstacle_list = []
    # level 1 obstacles
    ob1 = pygame.Rect(290, 395 + 15, 100, 50)
    ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
    obstacle_list = [ob1, ground]


    ### Portal ###

    portal = pygame.image.load('image (4).png').convert_alpha()
    portal = pygame.transform.scale(portal, (125, 125))
    portal_hitbox = pygame.Rect(680 + 10, 100 - 50, 125 - 80, 125)
    # portal.rect = portal.image.get_rect()

    portal_surface = pygame.image.load('image (2).png').convert_alpha()
    portal_surface = pygame.transform.scale(portal_surface, (125, 125))

    coin_list = []

    coin1 = Coin(ob1.left + ob1.width / 2, ob1.top - 25)
    coin1.randomize_pos()
    coin_list.append(coin1)

    '''
    coin1 = Coin(ob1.left + ob1.width / 2, ob1.top - 25)
    coin1.anim = coin_anim
    coin1.randomize_pos()
    coin_list.append(coin1)


    coin2 = Coin(ob2.left + ob2.width / 2, ob2.top - 25)
    coin2.anim = coin_anim
    coin2.randomize_pos()
    coin_list.append(coin2)


    coin3 = Coin(ground.left + ground.width / 2, ground.top - 25)
    coin3.anim = coin_anim
    coin3.randomize_pos()
    coin_list.append(coin3)

    coin4 = Coin(ground.left + ground.width / 2, ground.top - 25)
    coin4.anim = coin_anim
    coin4.randomize_pos()
    coin_list.append(coin4)
    '''

    # spike = pygame.image.load('SPIKE.png').convert_alpha()
    # spike = pygame.transform.scale(spike, (50,50))

    # testing
    level_counter1 = level_counter(1)
    coin_counter = score_counter()
    game_state = 'gameplay'
    # The main game loop
    game_state = 'gameMenu'



    while looping:

        if game_state == 'gameMenu':
            mouseClicked = False
            '''
            background_img = pygame.image.load("BlueBackground.png").convert_alpha()
            background_img = pygame.transform.scale(background_img, (800, 600))
            WINDOW.blit(background_img, (0, 0))
            '''
            WINDOW.fill('light blue')
            fontObj = pygame.font.Font(None, 64)
            PlatformerText = fontObj.render("Platformer", True, TEXT_COLOR, None)
            WINDOW.blit(PlatformerText, (WINDOW.get_width() / 2 - PlatformerText.get_width() / 2,
                                         WINDOW.get_height() / 2 - 45 - PlatformerText.get_height() / 2))

            # Test Button
            test_button = button(0, 0, 100, 100, 'orange', 'hello', None)
            # test_button.render_button()

            # Start Button
            start_button = button(WINDOW.get_width() / 2 - 50 - 100, WINDOW.get_height() / 2, 100, 100, 'orange',
                                  'start', None)
            start_button.render_button()
            startfontobj = pygame.font.Font(None, 32)

            # Start Button text
            StartText = startfontobj.render("Start", True, TEXT_COLOR, None)
            x = WINDOW.get_width() / 2 - PlatformerText.get_width() / 2 + 80 - 150 + 50
            y = WINDOW.get_height() / 2 - 45 - PlatformerText.get_height() / 2 + 100

            WINDOW.blit(StartText, (x, y))

            # About the creator button
            atc_button = button(WINDOW.get_width() / 2 - 50 + 78, WINDOW.get_height() / 2, 100, 100, 'orange',
                                'Creator', None)
            atc_button.render_button()
            atcfontobj = pygame.font.Font(None, 32)

            # atc button text
            atcText = atcfontobj.render("Creator", True, TEXT_COLOR, None)
            x = WINDOW.get_width() / 2 - atcText.get_width() / 2 + 80
            y = WINDOW.get_height() / 2 - 45 - atcText.get_height() / 2 + 100 - 10
            WINDOW.blit(atcText, (x, y))

            # Tutorial Button
            x = 50
            y = 20
            tb = button(x, y, 200, 100 / 2, 'dodgerblue', 'tutorial', None)
            tb.render_button()
            tbfontobj = pygame.font.Font(None, 32)

            # Tutorial Button text
            txt = tbfontobj.render("Tutorial", True, TEXT_COLOR, None)
            x = 100
            y = 45 - 10

            WINDOW.blit(txt, (x, y))


            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    mouseClicked = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseClicked = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button.hitbox.collidepoint((mouse_x, mouse_y)) and mouseClicked == True:
                    level = 1
                    level_counter1.set_number(1)
                    player.health = player.max_health
                    player.x = 100
                    player.y = 500
                    tutorial_initialized = False
                    game_state = 'gameplay'
                if atc_button.hitbox.collidepoint((mouse_x, mouse_y)) and mouseClicked == True:
                    game_state = 'creator'
                if tb.hitbox.collidepoint((mouse_x, mouse_y)) and mouseClicked == True:
                    game_state = 'tutorial_level'
                if event.type == pygame.QUIT:
                    exit()

        elif game_state == 'tutorial_level':
            global spikes

            # Exit Button
            exit_button = button(exit_button_rect.x, exit_button_rect.y, exit_button_rect.width, exit_button_rect.height, 'orange', 'exit', None)
            exitfontobj = pygame.font.Font(None, 32)

            # Exit Button text
            ExitText = exitfontobj.render("Exit", True, TEXT_COLOR, None)
            x = 700
            y = 75 + 15

            mouseClicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if exit_button_rect.collidepoint(mouse_pos):
                        game_state = 'gameMenu'
                        level = 1


            WINDOW.fill('lightblue')

            font2 = pygame.font.SysFont(None, 36)
            text_surface = font2.render("Use arrow keys to move and jump!", True, (155, 155, 155))


            if tutorial_initialized == False:
                player.x = 100
                player.y = 500
                player.vel_x = 0
                player.vel_y = 0
                player.on_ground = False
                player.hitbox.topleft = (player.x, player.y)

                ob1 = pygame.Rect(100, 450-50, 200, 50)
                ob2 = pygame.Rect(400, 350, 100, 50)
                spikes.clear() 
                spikes.append(spike(450, 300))
                print("Tutorial Spikes", len(spikes))
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
                obstacle_list = [ob1, ob2, ground]


                tutorial_initialized = True



            # --- Input ---
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

            # --- Horizontal movement and collision ---
            player.x += player.vel_x
            player.hitbox.topleft = (player.x, player.y)
            horizontal_collision(player, obstacle_list)

            # --- Vertical movement and collision ---
            player.vel_y += player.gravity
            player.y += int(player.vel_y)
            player.hitbox.topleft = (player.x, player.y)

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

            for spike in spikes:
                spike.update()
                spike.collisions(player)


            player.hitbox.topleft = (player.x, player.y)

            WINDOW.blit(text_surface, (200, 150))
            #pygame.draw.rect((255, 0, 0), spike.hitbox)
            for ob in obstacle_list:
                WINDOW.blit(pygame.transform.scale(platform, (ob.width, ob.height)), ob.topleft)

            WINDOW.blit(background, (0, 0))

            for spike in spikes:
                WINDOW.blit(spike.image, (spike.x, spike.y))

            #WINDOW.blit(Spike.image, Spike.hitbox.topleft)
            exit_button.render_button()
            WINDOW.blit(ExitText, (x, y))
            WINDOW.blit(player.player_now, (player.x, player.y))







        elif game_state == 'tutorial':
            WINDOW.fill('lightblue')
            Titlefontobj = pygame.font.Font(None, 64)
            # WINDOW.fill('lightblue')
            # text
            Title = Titlefontobj.render("Game Features", True, TEXT_COLOR, None)
            # perfect placement and text size
            x = WINDOW.get_width() / 2 - Title.get_width() / 2 + 80 - 75
            y = 25
            WINDOW.blit(Title, (x, y))

            para_text = "Use arrow keys to move"
            font = pygame.font.Font(None, 32)
            para = font.render(para_text, True, TEXT_COLOR, None)
            x = WINDOW.get_width() / 2 - Title.get_width() / 2 + 80 - 75
            y = 25 + 100 - 50 + 10
            WINDOW.blit(para, (x, y))

            para_text = "Jump into portal to enter the next level"
            font = pygame.font.Font(None, 32)
            para = font.render(para_text, True, TEXT_COLOR, None)
            x = WINDOW.get_width() / 2 - Title.get_width() / 2 + 80 - 75
            y = 25 + 100 - 50 + 50
            WINDOW.blit(para, (x, y))

            para_text = "Collect coins to earn points"
            font = pygame.font.Font(None, 32)
            para = font.render(para_text, True, TEXT_COLOR, None)
            x = WINDOW.get_width() / 2 - Title.get_width() / 2 + 80 - 75
            y = 25 + 100 - 50 + 90
            WINDOW.blit(para, (x, y))

            # Exit Button
            exit_button = button(600, 500 - 75, 100, 100, 'orange', 'exit', None)
            exit_button.render_button()
            exitfontobj = pygame.font.Font(None, 32)

            # Exit Button text
            ExitText = exitfontobj.render("Exit", True, TEXT_COLOR, None)
            x = 600 + 50 - 25
            y = 500 - 75 + 50 - 25 + 15

            WINDOW.blit(ExitText, (x, y))

            mouseClicked = False

            for event in pygame.event.get():
                # if clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseClicked = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check EXIT button click
            if exit_button.hitbox.collidepoint((mouse_x, mouse_y)) and mouseClicked:
                game_state = 'gameMenu'



        # Creator Page
        elif game_state == 'creator':
            # mouseClicked = False
            WINDOW.fill('lightblue')

            Titlefontobj = pygame.font.Font(None, 64)

            # text
            Title = Titlefontobj.render("About the Creator: Ankitha Mukund", True, TEXT_COLOR, None)
            # perfect placement and text size
            x = WINDOW.get_width() / 2 - Title.get_width() / 2 + 80 - 75
            y = 25
            WINDOW.blit(Title, (x, y))

            # loading computer img
            img = pygame.image.load("computah.jpeg").convert_alpha()
            img = pygame.transform.scale(img, (200, 200))
            WINDOW.blit(img, (550 + 50, 100))

            para_text = "Hi, I am the creator of this platformer, Ankitha."
            font = pygame.font.Font(None, 32)
            para = font.render(para_text, True, TEXT_COLOR, None)
            x = WINDOW.get_width() / 2 - Title.get_width() / 2 + 80 - 75
            y = 25 + 100
            WINDOW.blit(para, (x, y))

            para_text = "First off, I would like to thank my playtester, Architha."
            font = pygame.font.Font(None, 32)
            para = font.render(para_text, True, TEXT_COLOR, None)
            x = WINDOW.get_width() / 2 - Title.get_width() / 2 + 80 - 75
            y = 25 + 100 + 50
            WINDOW.blit(para, (x, y))

            para_text = "I have worked on this game for about 1.5 years."
            font = pygame.font.Font(None, 32)
            para = font.render(para_text, True, TEXT_COLOR, None)
            x = WINDOW.get_width() / 2 - Title.get_width() / 2 + 80 - 75
            y = 25 + 100 + 50 + 50
            WINDOW.blit(para, (x, y))

            para_text = "Over time, I have made many additions, and some"
            font = pygame.font.Font(None, 32)
            para = font.render(para_text, True, TEXT_COLOR, None)
            x = WINDOW.get_width() / 2 - Title.get_width() / 2 + 80 - 75
            y = 25 + 100 + 50 + 50 + 50
            WINDOW.blit(para, (x, y))

            para_text = "include gravity, collisions, classes, and a score counter."
            font = pygame.font.Font(None, 32)
            para = font.render(para_text, True, TEXT_COLOR, None)
            x = WINDOW.get_width() / 2 - Title.get_width() / 2 + 80 - 75
            y = 25 + 100 + 50 + 200 - 50
            WINDOW.blit(para, (x, y))

            # Exit Button
            exit_button = button(600, 500 - 75, 100, 100, 'orange', 'exit', None)
            exit_button.render_button()
            exitfontobj = pygame.font.Font(None, 32)

            # Exit Button text
            ExitText = exitfontobj.render("Exit", True, TEXT_COLOR, None)
            x = 600 + 50 - 25
            y = 500 - 75 + 50 - 25 + 15

            WINDOW.blit(ExitText, (x, y))

            mouseClicked = False

            for event in pygame.event.get():
                # if clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseClicked = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check EXIT button click
            if exit_button.hitbox.collidepoint((mouse_x, mouse_y)) and mouseClicked:
                game_state = 'gameMenu'


        elif game_state == 'gameplay':
            # for testing
            # level = 2
            # level_changing = True
            level_changing = False
            # Get inputs
            key = pygame.key.get_pressed()

            # Movement
            player.vel_x = 0

            if key[pygame.K_LEFT]:
                player.vel_x = -player.move_speed
                player.player_now = player.player_image
                player.facing_left = True
            if key[pygame.K_RIGHT]:
                player.vel_x = player.move_speed
                player.player_now = player.player_flipped_image
                player.facing_left = False
            if (key[pygame.K_UP] or key[pygame.K_SPACE]) and player.on_ground == True:
                player.vel_y = player.jump_strength
                player.on_ground = False
            if key[pygame.K_SLASH]:
                colorImage = pygame.Surface(player.player_image.get_size()).convert_alpha()
                colorImage.fill(player.player_color)
                player.player_image.blit(colorImage, (player.x, player.y), special_flags=pygame.BLEND_RGBA_MULT)

            if player.hitbox.colliderect(portal_hitbox) and level == 1:
                player.player_reset = True
                level = 2
                level_changing = True
                level_counter1.set_number(int(level))
            elif player.hitbox.colliderect(portal_hitbox) and (level == 2 or level == 'secret'):
                player.player_reset = True
                level = 3
                level_changing = True
                level_counter1.set_number(int(level))
            elif player.hitbox.colliderect(portal_hitbox) and level == 3:
                player.player_reset = True
                level = 4
                level_changing = True
                level_counter1.set_number(int(level))
            elif player.hitbox.colliderect(portal_hitbox) and level == 4:
                player.player_reset = True
                level = 5
                level_changing = True
                level_counter1.set_number(int(level))
            elif player.hitbox.colliderect(portal_hitbox) and level == 5:
                player.player_reset = True
                level = 6
                level_changing = True
                level_counter1.set_number(int(level))


            # Level 2
            if level == 2 and level_changing:
                level_changing = False
                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False
                # ob1 = pygame.Rect(290, 395, 125, 50)
                ob2 = pygame.Rect(random.randint(550, 575), random.randint(260, 275), 125, 50)
                ob3 = pygame.Rect(450, 450, 175, 50)
                # ob4 = pygame.Rect(650/2, 650/2 - 50, 50, 50)
                ob5 = pygame.Rect(650 / 2 - 250 - 75 + 345, 650 / 2 - 70, 50, 50)  # secret level block
                # ob6 = pygame.Rect(400, 200, 200, 50)

                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
                obstacle_list = [ob2, ob3, ground]
                # spike1 = (400, 150, 50, 50)
                # spike2 = (550, 150, 50, 50)

                coin_list = []
                '''
                new_coin = Coin(ob1.left + ob1.width / 2, ob1.top - 25)
                new_coin.anim = coin_anim
                new_coin.randomize_pos()
                coin_list.append(new_coin)

                new_coin2 = Coin(ob1.left + ob3.width / 2, ob3.top - 25)
                new_coin2.anim = coin_anim
                new_coin2.randomize_pos()
                coin_list.append(new_coin2)

                new_coin3 = Coin(ground.left + ground.width / 2, ob1.top - 25)
                new_coin3.anim = coin_anim
                new_coin3.randomize_pos()
                coin_list.append(new_coin3)

                new_coin4 = Coin(ob6.left + ob6.width / 2, ob6.top - 25)
                new_coin4.anim = coin_anim
                new_coin4.randomize_pos()
                coin_list.append(new_coin4)

                new_coin5 = Coin(ob1.left + ob7.width / 2, ob7.top - 25)
                new_coin5.anim = coin_anim
                new_coin5.randomize_pos()
                coin_list.append(new_coin5)
                '''

                # touched secret level portal

                # spike_position_list = [spike1, spike2]

                pygame.draw.rect(WINDOW, (255, 0, 0), enemy.player_rect)
            if level == 2 and not level_changing:
                if player.hitbox.colliderect(ob5):
                    player.player_reset = True
                    level_counter1.set_number(str('secret level'))
                    level_changing = True
                    print("touched secret level")
                    level = 'secret'
                    WINDOW = pygame.display.set_mode((WINDOW_WIDTH + 400, WINDOW_HEIGHT))
                    background = pygame.transform.scale(background, (800 + 400, 600))

            # secret level
            if level == "secret" and level_changing:
                level_changing = False

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                # ob1 = pygame.Rect(200, 450, 100, 50)
                ob2 = pygame.Rect(500 - 25, 350, 150, 50)  # long platform on bottom
                ob3 = pygame.Rect(600 + 75, 250 - 50 - 15, 50, 50)
                ob4 = pygame.Rect(700, 200, 50, 50)
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)

                coin_list = []

                obstacle_list = [ob2, ob3, ob4, ground]

                # replace ALL  coins with this implimentation

                coin1 = Coin(ob1.left + ob1.width / 2, ob1.top - 25)
                coin1.anim = coin_anim
                coin1.randomize_pos()
                coin_list.append(coin1)

                '''
                new_coin1 = Coin(ob1.left + ob1.width / 2, ob1.top - 25)
                new_coin1.randomize_pos()
                coin_list.append(new_coin1)

                new_coin2 = Coin(ob1.left + ob1.width / 2 + 10, ob1.top - 25)
                new_coin2.randomize_pos()
                coin_list.append(new_coin2)

                new_coin3 = Coin(ob2.left + ob2.width / 2, ob2.top - 25)
                new_coin3.randomize_pos()
                coin_list.append(new_coin3)

                new_coin4 = Coin(ground.left + ground.width / 2 + 400, ground.top - 25)
                new_coin4.randomize_pos()
                coin_list.append(new_coin4)

                new_coin5 = Coin(ground.left + ground.width / 2 - 500, ground.top - 25)
                new_coin5.randomize_pos()
                coin_list.append(new_coin5)

                new_coin6 = Coin(ground.left + ground.width / 2 + 300, ground.top - 25)
                new_coin6.randomize_pos()
                coin_list.append(new_coin6)

                new_coin7 = Coin(ground.left + ground.width / 2 - 399, ground.top - 25)
                new_coin7.randomize_pos()
                coin_list.append(new_coin7)

                new_coin4 = Coin(ob3.left + ob3.width / 2, ob3.top - 25)
                new_coin4.randomize_pos()
                coin_list.append(new_coin4)

                new_coin5 = Coin(ground.left + ground.width / 2, ground.top - 25)
                new_coin5.randomize_pos()
                coin_list.append(new_coin5)

                new_coin6 = Coin(ob6.left + ob6.width / 2, ob6.top - 25)
                new_coin6.randomize_pos()
                coin_list.append(new_coin6)

                new_coin8 = Coin(ground.left + ground.width / 2, ground.top - 25)
                new_coin8.randomize_pos()
                coin_list.append(new_coin8)
                '''

            if level == "secret" and not level_changing:
                horizontal_collision(player, obstacle_list)

            # level 3
            if level == 3 and level_changing == True:
                level_changing = False

                # setting screen and background sizes less from the secret level
                WINDOW = pygame.display.set_mode((800, 600))
                background = pygame.transform.scale(background, (800, 600))

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                # ob1 = pygame.Rect(x, y, width, height)
                ob1 = pygame.Rect(200, 400, 200, 50)  # long platform with spike1
                ob2 = pygame.Rect(450, 290, 50, 50)  # make grey
                # ob3 = pygame.Rect(330, 175, 50, 50) # make grey
                ob4 = pygame.Rect(550, 175, 160, 50)
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)

                coin_list = []
                obstacle_list = [ob1, ob2, ob4, ground]

                coin1 = Coin(ob3.left + ob3.width / 2, ob3.top - 25)
                coin1.anim = coin_anim
                coin1.randomize_pos()
                coin_list.append(coin1)

                coin2 = Coin(ob1.left + ob1.width / 2, ob1.top - 25)
                coin2.anim = coin_anim
                coin2.randomize_pos()
                coin_list.append(coin2)

            # level 4
            if level == 4 and level_changing == True:
                level_changing = False

                # setting screen and background sizes less from the secret level
                WINDOW = pygame.display.set_mode((800, 600))
                background = pygame.transform.scale(background, (800, 600))

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                ob1 = pygame.Rect(200, 350, 100, 50)
                ob2 = pygame.Rect(500 - 25, 350, 100, 50)
                ob3 = pygame.Rect(375, 545 - 50, 50, 50)  # fill with grey
                # ob4 = pygame.Rect(375, 350, 50, 50) # fill with grey
                ob5 = pygame.Rect(475 + 45 + 75, 200 + 12 + 10, 50, 50)  # fill with grey
                ob6 = pygame.Rect(ob5.x - 25 - 75 - 25, ob5.y - 35 - 50, 50, 50)  # fill with grey
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)

                coin_list = []
                obstacle_list = [ob1, ob2, ob3, ob5, ob6, ground]

                coin1 = Coin(ground.left + ground.width / 2, ground.top - 25)
                coin1.anim = coin_anim
                coin1.randomize_pos()
                coin_list.append(coin1)

                coin2 = Coin(ground.left + ground.width / 2, ground.top - 25)
                coin1.anim = coin_anim
                coin1.randomize_pos()
                coin_list.append(coin2)

            # level 5
            if level == 5 and level_changing == True:
                level_changing = False

                # setting screen and background sizes less from the secret level
                WINDOW = pygame.display.set_mode((800, 600))
                background = pygame.transform.scale(background, (800, 600))

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                ob1 = pygame.Rect(200, 425, 100, 50)
                ob2 = pygame.Rect(250 + 25, 225 + 50 + 30, 50, 50) # filled with grey
                ob3 = pygame.Rect(ob2.x + 40 + 75, ob2.y - 75 + 35, 125, 50)
                ob4 = pygame.Rect(ob3.x + 100 + 50, ob3.y - 75, 50, 50) # filled with grey
                ob5 = pygame.Rect(ob4.x + 75 + 75, ob4.y, 50, 50) # filled with grey
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)



                obstacle_list = [ob1, ob2, ob3, ob4, ob5, ground]
                coin_list = []

            # level 6
            if level == 6 and level_changing == True:
                level_changing = False

                # setting screen and background sizes less from the secret level
                WINDOW = pygame.display.set_mode((800, 600))
                background = pygame.transform.scale(background, (800, 600))

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                ob1 = pygame.Rect(150, 500 - 50, 150, 50)
                ob2 = pygame.Rect(ob1.x + 100, ob1.y - 50, 60, 50) # fill with grey
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)

                obstacle_list = [ob1, ob2, ground]
                coin_list = []

            horizontal_collision(player, obstacle_list)
            player.vel_y += player.gravity
            player.hitbox.top = player.y
            player.hitbox.left = player.x

            # Vertical Collision
            player.on_ground = False
            for x in obstacle_list:
                if player.hitbox.colliderect(x):
                    # Landing on top of a obstacle
                    if player.vel_y > 0 and player.hitbox.bottom - player.vel_y <= x.top:
                        player.y = x.top - player.hitbox.height
                        player.vel_y = 0
                        player.on_ground = True
                    # Hitting a Obstacle
                    elif player.vel_y < 0 and player.hitbox.top - player.vel_y >= x.bottom:
                        player.y = x.bottom
                        player.vel_y = 0

            player.y += int(player.vel_y)
            player.x += player.vel_x

            player.hitbox.top = player.y
            player.hitbox.left = player.x

            for coin in coin_list:
                coin.collide(player.hitbox)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Processing
            # Left boundary
            if player.hitbox.left < 0:
                player.x = 0
                player.hitbox.left = 0

            # Right boundary
            if player.hitbox.right > WINDOW_WIDTH:
                player.x = WINDOW_WIDTH - player.hitbox.width
                player.hitbox.right = WINDOW_WIDTH

            # This section will be built out later

            # Render elements of the game
            portal_x = 680 - 300
            portal_y = 100 + 100
            portal_hitbox.topleft = (portal_x, portal_y)

            # if 640 <  player

            WINDOW.blit(background, (0, 0))
            # health bar
            pygame.draw.rect(WINDOW, (100, 100, 100), (50, 50, 200, 20))
            health_ratio = max(player.health / player.max_health, 0)
            pygame.draw.rect(WINDOW, (255, 0, 0), (50, 50, 200 * health_ratio, 20))
            pygame.draw.rect(WINDOW, (0, 0, 0), (50, 50, 200, 20), 2)

            for rect in obstacle_list:
                # pygame.draw.rect(WINDOW, OBSTACLE_COLOR, x)
                platform_img = pygame.transform.scale(platform, (rect.width, rect.height))

                if level == 3:
                    if rect == ob2:
                        platform_img.fill((128, 128, 128))

                if level == 4:
                    if rect == ob3 or rect == ob4 or rect == ob5 or rect == ob6:
                        platform_img.fill((128, 128, 128))

                if level == 5:
                    if rect == ob2 or rect == ob4 or rect == ob5:
                        platform_img.fill((128, 128, 128))

                if level == 6:
                    if rect == ob2:
                        platform_img.fill((128, 128, 128))
                WINDOW.blit(platform_img, rect.topleft)

            if level == 2:
                portal_x = 680
                portal_y = 100
                portal_hitbox.topleft = (portal_x, portal_y)
                #pygame.draw.rect(WINDOW, (0, 0, 0), ob5)
                platform_img = pygame.transform.scale(platform_img, (ob5.width, ob5.height))
                platform_img.fill((128, 128, 128))
                WINDOW.blit(platform_img, ob5.topleft)
            if level == 'secret':
                portal_x = 680 + 250
                portal_y = 100 - 23.5
                portal_hitbox.topleft = (portal_x, portal_y)
                pygame.draw.rect(WINDOW, (0, 0, 0), portal_hitbox)
                for x in obstacle_list:
                    pygame.draw.rect(WINDOW, (0, 0, 0), x)

            if level == 3:
                portal_x = WINDOW_WIDTH - 75 - 20
                portal_y = 50
                portal_hitbox.topleft = (portal_x, portal_y)

            if level == 4:
                portal_x = WINDOW_WIDTH - 75 - 20 - 400
                portal_y = 50
                portal_hitbox.topleft = (portal_x, portal_y)
            if level == 5:
                portal_x = WINDOW_WIDTH - 95
                portal_y = 50
                portal_hitbox.topleft = (portal_x, portal_y)

            for coin in coin_list:
                coin.render_coin()

            if player.health <= 0:
                game_state = 'gameMenu'
                level = 1
                player.health = player.max_health
                player.x = 100
                player.y = 500
                obstacle_list = []
                portal_x = 680 - 300
                portal_y = 100 + 100
                portal_hitbox.topleft = (portal_x, portal_y)




            # WINDOW.fill(PLAYER_COLOR, player)
            WINDOW.blit(player.player_now, (player.x, player.y))
            WINDOW.blit(portal, (portal_x, portal_y))
            WINDOW.blit(level_counter1.text(), (170, 100))
            WINDOW.blit(coin_counter.text(coin_list), (300, 100))
            # WINDOW.blit(portal_surface, (680, 100-50))
        pygame.display.update()
        fpsClock.tick(FPS)


main()
