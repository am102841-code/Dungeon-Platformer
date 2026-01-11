import pygame, sys, random, time
from pygame.locals import *

pygame.init()
pygame.mixer.init()

### Priorities/ Improvements ###
# store points as a variable so the points does nto reset to 0 after each level ends
# add more sound effects (done 12/29 and 1/1/25)

# Initialize Variables
points = 0
selected_character = None
showMessage = False
startTime = 0
showMessage2 = False
startTime2 = 0
points_added = False
pulse_side = "right"

# Knight
show_message = False
start_time = 0
text = ""

# Wizard
show_message2 = False
start_time2 = 0
text2 = ""

# Archer
show_message3 = False
start_time3 = 0
text3 = ""

# Colours
BACKGROUND = (255, 255, 255)
OBSTACLE_COLOR = (0, 0, 0)
PLAYER_COLOR = (0, 199, 255)
TEXT_COLOR = (100, 100, 100)
CREATOR_COLOR = (153, 204, 255)
GREY = (224, 224, 224)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
level = 1

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Platformer')

clock = pygame.time.Clock()

# Images
background = pygame.image.load('background.png').convert_alpha()
background = pygame.transform.scale(background, (800, 600))
platform = pygame.image.load('PLATFORM.png').convert_alpha()

# Characters Images
knight = pygame.image.load('KNIGHT2.png').convert_alpha()
knight = pygame.transform.scale(knight, (100, 100))
wizard = pygame.image.load('WIZARD.png').convert_alpha()
wizard = pygame.transform.scale(wizard, (100, 100))
archer = pygame.image.load('KNIGHT.png').convert_alpha()
archer = pygame.transform.scale(archer, (65, 65))
start_img = pygame.image.load('start_button.png').convert_alpha()
start_img = pygame.transform.scale(start_img, (160, 120))
# center stores the (x, y) coordinates
start_rect = start_img.get_rect(center=(WINDOW_WIDTH // 2 - 60 - 15 - 20- 10, WINDOW_HEIGHT // 2 + 75 - 40 + 20))
creator_img = pygame.image.load('creator_button.png').convert_alpha()
creator_img = pygame.transform.scale(creator_img, (152*1.5, 152*1.5+20))
creator_rect = creator_img.get_rect(center=(WINDOW_WIDTH // 2 - 60 - 15 + 100 + 75+50-15-10 - 10, WINDOW_HEIGHT // 2 + 75 + 6.5- 40 + 20 + 75-50+40-15-4.5))

# music
pygame.mixer.music.load("music0.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# sounds [add sounds: jumping, landing on obstacle, hitting spike]
coin_sound = pygame.mixer.Sound("collected_coin.wav")
portal_sound = pygame.mixer.Sound("portal.wav")
damage_sound = pygame.mixer.Sound("damage.wav")
jumping_sound = pygame.mixer.Sound("jumping.wav")

# setting up player animations to loop forever in game menu

GROUND_Y = WINDOW_HEIGHT - knight.get_height()
menu_x = -64
menu_y = GROUND_Y

menu_x_speed = 2*3 # sets the speed fo the character
menu_y_speed = 0

menu_on_ground = True
menu_jump_timer = 0


tutorial_initialized = False

    # Classes

class ColoredPlatform:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color   #(red, green, blue)
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill(color)

    def draw(self, surface, image):
        pass

# Player Class
class Player():
    def __init__(self):
        self.player_now = None
        self.x = 250
        self.y = 450
        self.player_image = pygame.image.load('KNIGHT2.png').convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (65, 65))
        self.player_flipped_image = pygame.transform.flip(self.player_image, True, False)
        self.vel_y = 0
        self.vel_x = 0
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

# Spike Class
class Spike():
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
            damage_sound.play()
            player.health -= 1
            player.x = 100
            player.y = 500
            player.hitbox.topleft = (player.x, player.y)

# Enemy Class (fix and use later)
class Enemy():
    def __init__(self):
        self.x = 200
        self.y = 200
        self.move_speed = 4
        self.on_ground = False
        self.health = 5
        self.player_rect = pygame.Rect(self.x, self.y, 65 / 2, 65 / 2)
        self.facing_left = True

# Level Counter Class
class level_counter():
    def __init__(self, number):
        self.number = number

    def text(self):
        fontObj = pygame.font.Font(None, 32)
        textSufaceObj = fontObj.render("Level " + str(self.number), True, TEXT_COLOR, None)
        return textSufaceObj

    def set_number(self, newNumber):
        self.number = newNumber

# Score Counter Class
class score_counter():
    def __init__(self):
        pass

    def text(self, coin_list=None):
        fontObj = pygame.font.Font(None, 32)
        textSufaceObj = fontObj.render("Points: " + str(points), True, TEXT_COLOR, None)
        return textSufaceObj


# pygame.draw.circle(surface, color, center_coordinates, radius, width=0)

# sprite sheet?
# spinning coin
# spilt sprite sheet
# fix sheet

# Coin Animation Class
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

# Not Using right now --> fix
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

# Coin Class
class Coin():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.collected = False
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_hitbox(self):
        return self.hitbox

    def render_coin(self):
        if not self.collected:
            # Draw a simple yellow circle
            pygame.draw.circle(WINDOW, (255, 215, 0), (int(self.x + self.width / 2 ), int(self.y + self.height / 2)), self.width // 2)

    def collide(self, playerHitbox):
        global points
        if self.get_hitbox().colliderect(playerHitbox) and not self.collected:
            coin_sound.play()
            self.collected = True
            points += 1

    def randomize_pos(self):
        self.x += random.randint(-30, 30)
        self.y += random.randint(-30, 30)
        self.hitbox.topleft = (self.x, self.y)

# Button Class
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


exit_button_rect = pygame.Rect(WINDOW_WIDTH - 125, 50, 100, 100)

# The main function that controls the game
def main():
    looping = True

    global level, show_message2, selected_character, show_message3, showMessage, startTime, showMessage2, startTime2
    global WINDOW
    global background
    global secret_obstacle_list
    global tutorial_initialized
    global spikes
    global show_message
    global points, points_added
    global menu_jump_timer, menu_on_ground, menu_x_speed, menu_y_speed, menu_y, menu_x
    global jumping_sound

    player = Player()

    if selected_character == "wizard":
        player.player_now = wizard
        player.player_flipped_image = pygame.transform.flip(wizard, True, False)

    elif selected_character == "knight":
        player.player_now = knight
        player.player_flipped_image = pygame.transform.flip(knight, True, False)

    else:
        player.player_now = knight
        player.player_flipped_image = pygame.transform.flip(knight, True, False)

    # calculate pulse value (abs = absolute value)
    #pulse_value = 0
    #if level == 5:
        #pulse_value = abs(pygame.frame.get_ticks() % 600 - 300) / 300

    ### Obstacle Setup ###
    enemy = Enemy()
    obstacle_list = []
    spikes = []
    # level 1 obstacles
    obstacle_list.clear()
    ob1 = pygame.Rect(290-60, 395 + 15, 150, 40)
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

    coin1 = Coin(ob1.left + ob1.width / 2, ob1.top - 25 - 15)
    coin1.randomize_pos()
    coin_list.append(coin1)


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
            knight_selected = True
            wizard_selected = False

            background_img = pygame.image.load('game_menu.png').convert_alpha()
            background_img = pygame.transform.scale(background_img, (800, 600))
            WINDOW.blit(background_img, (0, 0))

            #WINDOW.fill('light blue')
            fontObj = pygame.font.Font(None, 64)
            PlatformerText = fontObj.render("Dungeon Platformer", True, GREY, None)
            WINDOW.blit(PlatformerText, (WINDOW.get_width() / 2 - PlatformerText.get_width() / 2,
                                         WINDOW.get_height() / 2 - 45 - PlatformerText.get_height() / 2))

            # Test Button
            test_button = button(0, 0, 100, 100, 'orange', 'hello', None)
            # test_button.render_button()

            # start button
            WINDOW.blit(start_img, start_rect)

            # creator button
            WINDOW.blit(creator_img, creator_rect)


            # Tutorial Button
            x = 50
            y = 20
            tb = button(x, y, 200, 100 / 2, (160, 160, 160), 'tutorial', None)
            tb.render_button()
            tbfontobj = pygame.font.Font(None, 32)

            # Tutorial Button text
            txt = tbfontobj.render("Tutorial", True, GREY, None)
            x = 100
            y = 45 - 10
            WINDOW.blit(txt, (x, y))

            # Characters button
            x = 50 + tb.width/3 + 150
            y = 20
            skins = button(x, y, tb.width, tb.height, (160, 160, 160), 'Characters', None)
            skins.render_button()
            font3 = pygame.font.Font(None, 32)

            # text
            text = font3.render("Characters", True, GREY, None)
            x = skins.x + skins.width/2 - 50 - 7.5
            y = skins.y + skins.height/2- 10
            WINDOW.blit(text, (x, y))




            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    if start_rect.collidepoint(mouse_x, mouse_y):
                        if selected_character is None:
                            showMessage = True
                            startTime = pygame.time.get_ticks()  # store ms timestamp

                        else:
                            level = 1
                            level_counter1.set_number(1)
                            player.health = player.max_health
                            player.x = 100
                            player.y = 500
                            tutorial_initialized = False
                            game_state = 'gameplay'

                    elif creator_rect.collidepoint(mouse_x, mouse_y):
                        game_state = 'creator'

                    elif tb.hitbox.collidepoint(mouse_x, mouse_y):
                        if selected_character is None:
                            showMessage2 = True
                            startTime2 = pygame.time.get_ticks()

                        else:
                            game_state = 'tutorial_level'


                    elif skins.hitbox.collidepoint(mouse_x, mouse_y):
                        game_state = 'skins'



            # check to show the text
            if showMessage == True:
                elapsed = pygame.time.get_ticks() - startTime
                duration_ms = 2500  # how long to show in milliseconds (3 seconds)
                if elapsed < duration_ms:
                    fontobj = pygame.font.Font(None, 32)
                    msg = "Choose a character from the Characters menu to play."
                    WINDOW.blit(fontobj.render(msg, True, (255, 255, 255)), (300-150, 300-75-75))
                else:
                    showMessage = False

            if showMessage2:
                elapsed2 = pygame.time.get_ticks() - startTime2
                duration_ms2 = 2500  # how long to show in milliseconds (3 seconds)
                if elapsed2 < duration_ms2:
                    fontobj = pygame.font.Font(None, 32)
                    msg2 = "Choose a character from the Characters menu to play."
                    WINDOW.blit(fontobj.render(msg2, True, (255, 255, 255)), (300-150, 300-75-75))
                else:
                    showMessage2 = False

            # player animation
            menu_x += menu_x_speed

            if menu_x > WINDOW_WIDTH:
                menu_x = -64


            menu_jump_timer += 1
            if menu_jump_timer > 120/2 and menu_on_ground:  # 120 frames = 2 seconds [this value sets how much the character jumps when going across the screen
                menu_y_speed = -15  # jump
                menu_on_ground = False
                if not jumping_sound.get_num_channels():
                    jumping_sound.play()  # sound
                menu_jump_timer = 0  # reset timer

            menu_y_speed += 1
            menu_y += menu_y_speed

            if menu_y >= GROUND_Y:
                menu_y = GROUND_Y
                menu_y_speed = 0
                menu_on_ground = True

            WINDOW.blit(knight, (menu_x, menu_y))

            pygame.display.update()


        elif game_state == "skins":
            # characters: knight; scarlet knight; wizard; witch; healer
            WINDOW.fill('lightgrey')

            # text
            my_font = pygame.font.Font('FONT.ttf', 24)
            #font2 = pygame.font.Font(None, 75)
            text = my_font.render("Click to choose your character", True, (0, 0, 0), None)
            x = 125 - 75 - 20 - 7.5
            y = 40 + 20 + 25
            WINDOW.blit(text, (x, y))

            # knight image
            knight2 = pygame.transform.scale(knight, (240-30-20, 240-30-20))
            WINDOW.blit(knight2, (125-50-25+50-10+20-5, 200-20-25+40))

            # knight text
            font3 = pygame.font.Font(None, 32)
            text = font3.render("Knight", True, (0, 0, 0), None)
            WINDOW.blit(text, (130 + 15, 335))

            # make hitbox
            hitbox = knight.get_rect()
            hitbox.topleft = (125, 200)

            # wizard image
            wizard_image = pygame.image.load("WIZARD.png").convert_alpha()
            wizard_image = pygame.transform.scale(wizard_image, (200, 200))
            WINDOW.blit(wizard_image, (265-25, 200))

            # wizard text
            text = font3.render("Wizard", True, (0, 0, 0), None)
            WINDOW.blit(text, (130 + 15 + 125 + 20, 335))

            # make hitbox2
            hitbox2 = wizard_image.get_rect()
            hitbox2.topleft = (225, 200)

            # archer image
            archer_image = pygame.image.load("KNIGHT.png").convert_alpha()
            archer_image = pygame.transform.scale(archer_image, (120, 120))
            WINDOW.blit(archer_image, (265-25+15+250-100+30-10, 200))

            # archer text
            archer_text = font3.render("Archer", True, (0, 0, 0), None)
            WINDOW.blit(archer_text, (130 + 15 + 125 + 20 + 125+30-10, 335))

            # make hitbox3
            hitbox3 = archer_image.get_rect()
            hitbox3.topleft = (130 + 15 + 125 + 20 + 125, 335)


            # rectangle borders
            border = pygame.Rect(130-25, 200, 170-25, 170)
            pygame.draw.rect(WINDOW, (0, 0, 0), border, width=5)

            border2 = pygame.Rect(130-25 + 150, 200, 170-25, 170)
            pygame.draw.rect(WINDOW, (0, 0, 0), border2, width=5)

            border3 = pygame.Rect(130-25 + 150+175-20-3.5, 200, 170-25, 170)
            pygame.draw.rect(WINDOW, (0, 0, 0), border3, width=5)

            # elf image
            #elf = pygame.image.load("ELF.png").convert_alpha()
            #elf = pygame.transform.scale(elf, (100, 100))
            #WINDOW.blit(elf, (445, 200))

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
            # if knight is clicked
            if hitbox.collidepoint((mouse_x, mouse_y)) and mouseClicked:
                selected_character = "knight"
                start_time = time.time()
                player.player_image = knight
                player.player_flipped_image = pygame.transform.flip(knight, True, False)
                show_message = True
                text = "Knight was selected!"
                #WINDOW.blit(k, (kx, ky)) # make the text stay for longer

            # if wizard is clicked
            if hitbox2.collidepoint((mouse_x, mouse_y)) and mouseClicked:
                selected_character = "wizard"
                start_time2 = time.time()
                player.player_image = wizard
                player.player_flipped_image = pygame.transform.flip(wizard, True, False)
                show_message2 = True
                text2 = "Wizard was selected!"
                #WINDOW.blit(w, (wx, wy))

            if hitbox3.collidepoint((mouse_x, mouse_y)) and mouseClicked:
                selected_character = "archer"
                start_time3 = time.time()
                # use the archer image (the smaller 'archer' surface you created earlier)
                player.player_image = archer
                player.player_flipped_image = pygame.transform.flip(archer, True, False)
                show_message3 = True
                text3 = "Archer was selected!"

            # Show Knight text
            if show_message == True:
                if time.time() - start_time < 1:
                    WINDOW.blit(exitfontobj.render("Knight was selected!", True, (0, 0, 0)), (450+75, 200-50))
                else:
                    show_message = False

            # Show Wizard text
            if show_message2 == True:
                if time.time() - start_time2 < 1:
                    WINDOW.blit(exitfontobj.render("Wizard was selected!", True, (0, 0, 0)), (450+75, 200-50))
                else:
                    show_message2 = False

            if show_message3 == True:
                if time.time() - start_time3 < 1:
                    WINDOW.blit(exitfontobj.render("Archer was selected!", True, (0, 0, 0)), (450+75, 200-50))
                else:
                    show_message3 = False

        elif game_state == 'tutorial_level':
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
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if exit_button_rect.collidepoint(mouse_pos):
                        game_state = 'gameMenu'
                        level = 1


            WINDOW.fill('lightblue')

            font2 = pygame.font.SysFont(None, 36)
            text_surface = font2.render("Use the arrow or letter keys to move and jump!", True, (155, 155, 155))


            if tutorial_initialized == False:
                player.x = 100
                player.y = 500
                player.vel_x = 0
                player.vel_y = 0
                player.on_ground = False
                player.hitbox.topleft = (player.x, player.y)

                ob1 = pygame.Rect(375 - 150, WINDOW_HEIGHT - 200 + 75, 200, 40)
                ob2 = pygame.Rect(ob1.x + ob1.width + 50, ob1.y - 75, 250, 40)
                spikes.append(Spike(ob2.x+60, ob2.y-60+15))
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
                obstacle_list = [ob1, ob2, ground]


                tutorial_initialized = True



            # --- Input ---
            keys = pygame.key.get_pressed()
            player.vel_x = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.vel_x = -player.move_speed
                player.player_now = player.player_image
                player.facing_left = True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.vel_x = player.move_speed
                player.player_now = player.player_flipped_image
                player.facing_left = False
            if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and player.on_ground:
                jumping_sound.play()
                player.vel_y = player.jump_strength
                #coin_sound.play()
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


            WINDOW.blit(background, (0, 0))
            WINDOW.blit(text_surface, (200-75, 150))
            exit_button.render_button()
            WINDOW.blit(ExitText, (x, y))
            if selected_character is not None:
                WINDOW.blit(player.player_now, (player.x, player.y))
            for ob in obstacle_list:
                WINDOW.blit(pygame.transform.scale(platform, (ob.width, ob.height)), ob.topleft)

            for spike in spikes:
                WINDOW.blit(spike.image, (spike.x, spike.y))

            if player.hitbox.left < 0:
                player.x = 0
                player.hitbox.left = 0

            # Right boundary
            if player.hitbox.right > WINDOW_WIDTH:
                player.x = WINDOW_WIDTH - player.hitbox.width
                player.hitbox.right = WINDOW_WIDTH


            #WINDOW.blit(Spike.image, Spike.hitbox.topleft)

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
            WINDOW.fill('lightgrey')

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
            keys = pygame.key.get_pressed()

            # Movement
            player.vel_x = 0

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.vel_x = -player.move_speed
                player.player_now = player.player_image
                player.facing_left = True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.vel_x = player.move_speed
                player.player_now = player.player_flipped_image
                player.facing_left = False
            if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and player.on_ground == True:
                jumping_sound.play()
                player.vel_y = player.jump_strength
                #coin_sound.play()
                player.on_ground = False
            if keys[pygame.K_SLASH]:
                colorImage = pygame.Surface(player.player_image.get_size()).convert_alpha()
                colorImage.fill(player.player_color)
                player.player_image.blit(colorImage, (player.x, player.y), special_flags=pygame.BLEND_RGBA_MULT)

            if player.hitbox.colliderect(portal_hitbox) and level == 1:
                portal_sound.play()
                player.player_reset = True
                level = 2
                level_changing = True
                level_counter1.set_number(int(level))
            elif player.hitbox.colliderect(portal_hitbox) and (level == 2 or level == 'secret'):
                portal_sound.play()
                player.player_reset = True
                level = 3
                level_changing = True
                level_counter1.set_number(int(level))
            elif player.hitbox.colliderect(portal_hitbox) and level == 3:
                portal_sound.play()
                player.player_reset = True
                level = 4
                level_changing = True
                level_counter1.set_number(int(level))
            elif player.hitbox.colliderect(portal_hitbox) and level == 4:
                portal_sound.play()
                player.player_reset = True
                level = 5
                level_changing = True
                level_counter1.set_number(int(level))
            elif player.hitbox.colliderect(portal_hitbox) and level == 5:
                portal_sound.play()
                player.player_reset = True
                level = 6
                level_changing = True
                level_counter1.set_number(int(level))


            if level == 1 and level_changing:
                level_changing = False
                player.x = 100
                player.y = 500

                # level 1 obstacles
                obstacle_list.clear()
                ob1 = pygame.Rect(290, 395 + 15, 100, 50)
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
                obstacle_list = [ob1, ground]

            # Level 2
            if level == 2 and level_changing:
                level_changing = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music2.mp3")
                pygame.mixer.music.play(-1) # -1 makes it loop forever
                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                # obstacles
                ob2 = pygame.Rect(565 - 200, 270+40, 200, 40)
                ob3 = pygame.Rect(450-200, 450, 175, 40)
                ob5 = pygame.Rect(650 / 2 - 250 - 75 + 345 + 50 - 250, 650 / 2 - 70 - 25, 50, 40)  # secret level block
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)

                # coins
                coin1 = Coin(ob2.left + ob2.width / 2, ob2.top - 25 - 15)
                coin1.randomize_pos()
                coin_list.append(coin1)

                coin2 = Coin(ob3.left + ob3.width / 2 + 20, ob3.top - 25 - 15)
                coin_list.append(coin2)

                coin3 = Coin(ob3.left + ob3.width / 2 - 50, ob3.top - 25 - 15)
                coin_list.append(coin3)

                # lists
                obstacle_list = [ob2, ob3, ground]
                coin_list = [coin1, coin2, coin3]


                pygame.draw.rect(WINDOW, (255, 0, 0), enemy.player_rect)
            if level == 2 and not level_changing:
                if player.hitbox.colliderect(ob5):
                    player.player_reset = True
                    level_counter1.set_number(str('secret'))
                    level_changing = True
                    print("touched secret level")
                    level = "secret"
                    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    background = pygame.transform.scale(background, (800, 600))

            # secret level
            if level == "secret" and level_changing:
                level_changing = False

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                portal_x, portal_y = 300, 100
                portal_hitbox.topleft = (portal_x, portal_y)



                '''
                # obstacles
                ob1 = pygame.Rect(350, 560, 100, 50)# middle - red
                ob2 = pygame.Rect(300, 490, 120, 50) # left - brown??
                ob3 = pygame.Rect(450, 500, 75, 50) # right - blue
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)
                # lists
                coin_list = []
                obstacle_list = [ground]

                # coins
                coin1 = Coin(ob2.left + ob2.width / 2, ob2.top - 25 - 15)
                coin1.randomize_pos()
                coin_list.append(coin1)

                coin2 = Coin(ob1.left + ob1.width / 2, ob1.top - 25 - 15)
                coin2.randomize_pos()
                coin_list.append(coin2)

                coin3 = Coin(ob3.left + ob3.width / 2, ob3.top - 25 - 15)
                coin3.randomize_pos()
                coin_list.append(coin3)

                for rect in obstacle_list:
                    # Fill with a color
                    pygame.draw.rect(WINDOW, (128, 128, 128), rect)
                '''


            if level == "secret" and not level_changing:
                horizontal_collision(player, obstacle_list)

            # level 3
            if level == 3 and level_changing == True:
                level_changing = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music3.mp3")
                pygame.mixer.music.play(-1)  # -1 makes it loop forever

                # setting screen and background sizes less from the secret level
                WINDOW = pygame.display.set_mode((800, 600))
                background = pygame.transform.scale(background, (800, 600))

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                # ob1 = pygame.Rect(x, y, width, height)
                ob1 = pygame.Rect(375, 600-100-200+100+50, 175, 40)
                ob2 = pygame.Rect(250-75, 600-120-250+100+50-85, 175, 40)  # make grey
                ob4 = pygame.Rect(ob2.x-200+400+50, ob2.y-125, 100, 40)
                spikes.clear()
                #spikes.append(Spike(550+75, 150+25-50))
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)

                # lists
                coin_list = []
                obstacle_list = [ob1, ob2, ob4, ground]

                # coins
                coin3 = Coin(ob1.left + ob1.width / 2, ob1.top - 25 - 15)
                coin3.randomize_pos()
                coin_list.append(coin3)

                coin4 = Coin(ob2.left + ob2.width / 2, ob2.top - 25 - 15)
                coin4.randomize_pos()
                coin_list.append(coin4)

            # level 4
            if level == 4 and level_changing == True:
                level_changing = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music4.mp3")
                pygame.mixer.music.play(-1)  # -1 makes it loop forever

                # setting screen and background sizes less from the secret level
                WINDOW = pygame.display.set_mode((800, 600))
                background = pygame.transform.scale(background, (800, 600))

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                ob1 = pygame.Rect(200, 350, 100, 50)
                ob2 = pygame.Rect(475, 350, 100, 50)
                ob3 = pygame.Rect(375, 545 - 50, 50, 50)  # fill with grey
                # ob4 = pygame.Rect(375, 350, 50, 50) # fill with grey
                ob5 = pygame.Rect(475 + 45 + 75 + 25, 200 + 12 + 10, 50, 50)  # fill with grey
                ob6 = pygame.Rect(ob5.x - 25 - 75 - 25 - 15, ob5.y - 35 - 50, 50, 50)  # fill with grey
                spikes.clear()
                #spikes.append(Spike(ob5.x + 20, ob5.y - ob5.height))
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)

                # lists
                coin_list = []
                obstacle_list = [ob1, ob2, ob3, ob5, ob6, ground]

                # coins
                coin3 = Coin(ob1.left + ob1.width / 2, ob1.top - 25 - 15)
                coin3.randomize_pos()
                coin_list.append(coin3)

                coin4 = Coin(ob2.left + ob2.width / 2, ob2.top - 25 - 15)
                coin4.randomize_pos()
                coin_list.append(coin4)

            # level 5
            if level == 5 and level_changing == True:
                level_changing = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music5.mp3")
                pygame.mixer.music.play(-1)  # -1 makes it loop forever

                # setting screen and background sizes less from the secret level
                WINDOW = pygame.display.set_mode((800, 600))
                background = pygame.transform.scale(background, (800, 600))

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                # obstacles
                ob1 = pygame.Rect(200-80, 425, 200, 50)
                ob2 = pygame.Rect(250 + 25, 225 + 50 + 30, 50, 50) # filled with grey
                ob3 = pygame.Rect(ob2.x + 40 + 75-50, ob2.y - 75 + 35, 200, 50) # add coin on top
                ob4 = pygame.Rect(ob3.x + 100 + 50, ob3.y - 75, 50, 50) # filled with grey
                ob5 = pygame.Rect(ob4.x + 75 + 75, ob4.y, 50, 50) # filled with grey
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)

                # lists
                obstacle_list = [ob1, ob2, ob3, ob4, ob5, ground]
                coin_list = []

                # spikes
                spikes.clear()
                spikes.append(Spike(ob3.x + 20 + 30, ob3.y - ob3.height))
                spikes.append(Spike(800-175, 100))

                # coins
                coin4 = Coin(ob1.left + ob1.width / 2, ob1.top - 25 - 15)
                coin4.randomize_pos()
                coin_list.append(coin4)

                coin5 = Coin(ob3.left + ob3.width / 2 - 20, ob3.top - 25 - 15)
                coin5.randomize_pos()
                coin_list.append(coin5)

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
                ob2 = pygame.Rect(ob1.x + 100 + 75, ob1.y - 50 - 50, 60, 50) # fill with grey
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
                if points_added:
                    points += 1
                    points_added = False
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

                WINDOW.blit(platform_img, (rect.x, rect.y))

            if level == 2:
                portal_x = 680 - 100
                portal_y = 100
                portal_hitbox.topleft = (portal_x, portal_y)
                #pygame.draw.rect(WINDOW, (0, 0, 0), ob5)
                platform_img = pygame.transform.scale(platform_img, (ob5.width, ob5.height))
                platform_img.fill((128, 128, 128))
                WINDOW.blit(platform_img, (ob5.x, ob5.y))

            if level == 'secret':
                portal_x = 680 + 250
                portal_y = 100 - 23.5
                portal_hitbox.topleft = (portal_x, portal_y)
                pygame.draw.rect(WINDOW, (0, 0, 0), portal_hitbox)


            if level == 3:
                portal_x = WINDOW_WIDTH - 75 - 20 - 150
                portal_y = 50
                portal_hitbox.topleft = (portal_x, portal_y)
                for spike in spikes:
                    WINDOW.blit(spike.image, (spike.x, spike.y))

                for spike in spikes:
                    spike.update()
                    spike.collisions(player)

            if level == 4:
                portal_x = WINDOW_WIDTH - 75 - 20 - 400
                portal_y = 50 - 25 - 10
                portal_hitbox.topleft = (portal_x, portal_y)
                for spike in spikes:
                    WINDOW.blit(spike.image, (spike.x, spike.y))

                for spike in spikes:
                    spike.update()
                    spike.collisions(player)
            if level == 5:
                portal_x = WINDOW_WIDTH - 95
                portal_y = 50
                portal_hitbox.topleft = (portal_x, portal_y)
                #pulse_surface = pygame.Surface((40, WINDOW_HEIGHT), pygame.SRCALPHA)
                #pulse_surface.fill((100, 100, 225, int(80 + pulse_value * 120)))
                #WINDOW.blit(pulse_surface, (WINDOW_WIDTH - 40, 0))
                for spike in spikes:
                    WINDOW.blit(spike.image, (spike.x, spike.y))

                for spike in spikes:
                    spike.update()
                    spike.collisions(player)

            for coin in coin_list:
                coin.render_coin()

            if player.player_image:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    player.vel_x = player.move_speed
                    player.player_now = player.player_flipped_image
                    player.facing_left = False
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    player.vel_x = -player.move_speed
                    player.player_now = player.player_image
                    player.facing_left = True

                if selected_character is not None:
                    WINDOW.blit(player.player_now, (player.x, player.y))


            if player.health <= 0:
                game_state = "Died_screen"
                if game_state == "Died_screen":
                    WINDOW.fill("lightgrey")
                    fonts = pygame.font.Font(None, 64)
                    fonts.render("Game Over!", True, (0, 0, 0), None)
                game_state = 'gameMenu'
                level = 1
                player.health = player.max_health
                player.x = 100
                player.y = 500
                obstacle_list = []
                portal_x = 380
                portal_y = 200
                portal_hitbox.topleft = (portal_x, portal_y)

            # WINDOW.fill(PLAYER_COLOR, player)
            #WINDOW.blit(player.player_now, (player.x, player.y))
            WINDOW.blit(portal, (portal_x, portal_y))
            WINDOW.blit(level_counter1.text(), (170, 100))
            WINDOW.blit(coin_counter.text(), (300, 100))
            # WINDOW.blit(portal_surface, (680, 100-50))
        pygame.display.update()
        fpsClock.tick(FPS)


main()
