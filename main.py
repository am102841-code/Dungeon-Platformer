import pygame, sys, random, time, math, os, json
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# make the character selection after the player clicks the start button

def resource_path(relative_path):
    # Web-compatible resource path
    try:
        # For web environment (pygbag)
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            # For web, use relative paths
            base_path = os.path.dirname(__file__) if '__file__' in dir() else os.path.abspath(".")
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialize Variables
player = None
obstacle_list = []
coin_list = []
spikes = []
portal = None
points = 0
selected_character = None
showMessage = False
startTime = 0
showMessage2 = False
startTime2 = 0
points_added = False
pulse_side = "right"
player_dead = False
death_time = 0
pulse = 0
pulse_direction = 1
death_particles = []
glow_size = 100
glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
glow_counter = 0
glow_speed = 0.05
damage_flash_time = 0
damage_flash_duration = 150
torch_list = []
play_music = False
shop_notice_text = ""
shop_notice_until = 0
skins_notice_text = ""
skins_notice_until = 0

# Cutscene Variables
cutscene_phase = 0  # 0 = story text, 1 = character walk, 2 = press space
cutscene_start_time = 0
cutscene_text_index = 0
cutscene_char_index = 0
darkness_alpha = 0
cutscene_complete = False

cutscene_texts = [
    "You awaken in the darkness...",
    "A dungeon surrounds you...",
    "Your only escape is forward."
]


# Level 5 Completion Cutscene Variables
level5_cutscene_active = False
level5_cutscene_text_index = 0
level5_cutscene_char_index = 0
level5_cutscene_last_char_time = 0
level5_cutscene_texts = [
    "Who are you?",
    "Why am I trapped here?",
    "You will find out soon...",
    "Until then, goodbye old friend..."
]
level5_cutscene_complete = False
level5_cutscene_fade_started = False

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

creator_music_playing = False

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
SAVE_FILE = os.path.join(os.path.abspath("."), "save_game.json")

# overlay for all levels
overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
overlay.set_alpha(125)

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Platformer')

clock = pygame.time.Clock()

# Mysterious Figure Sprite
mysterious_figure = pygame.image.load(resource_path('assets/x/dark_figure.png')).convert_alpha()
mysterious_figure = pygame.transform.scale(mysterious_figure, (120, 150))

# Images
background = pygame.image.load(resource_path('assets/x/background.png')).convert_alpha()
background = pygame.transform.scale(background, (800, 600))
middle_background = pygame.image.load(resource_path('assets/x/Dark_Dungeon_6.jpg')).convert_alpha()
middle_background = pygame.transform.scale(middle_background, (800, 600))
platform = pygame.image.load(resource_path('assets/x/platform.png')).convert_alpha()
platform = pygame.transform.scale(platform, (200, 60))
ground_image = pygame.image.load(resource_path('assets/x/ground.webp')).convert_alpha()
ground_image = pygame.transform.scale(ground_image, (100, 20))

# Character Images
knight = pygame.image.load(resource_path('assets/x/KNIGHT2.png')).convert_alpha()
knight = pygame.transform.scale(knight, (100, 100))
wizard = pygame.image.load(resource_path('assets/x/WIZARD.png')).convert_alpha()
wizard = pygame.transform.scale(wizard, (100, 100))
archer = pygame.image.load(resource_path('assets/x/KNIGHT.png')).convert_alpha()
archer = pygame.transform.scale(archer, (65, 65))
# center stores the (x, y) coordinates

# music
pygame.mixer.music.load(resource_path("assets/x/music0.ogg"))
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# sounds [add sounds: jumping, landing on obstacle, hitting spike]
coin_sound = pygame.mixer.Sound(resource_path("assets/x/collected_coin.ogg"))
portal_sound = pygame.mixer.Sound(resource_path("assets/x/portal.ogg"))
damage_sound = pygame.mixer.Sound(resource_path("assets/x/damage.ogg"))
jumping_sound = pygame.mixer.Sound(resource_path("assets/x/jumping.ogg"))
selected_sound = pygame.mixer.Sound(resource_path("assets/x/select.ogg"))
click_sound = pygame.mixer.Sound(resource_path("assets/x/click_sound.ogg"))

# setting up player animations to loop forever in game menu

GROUND_Y = WINDOW_HEIGHT - knight.get_height()
menu_x = -64
menu_y = GROUND_Y

menu_x_speed = 2 * 3
menu_y_speed = 0

menu_on_ground = True
menu_jump_timer = 0

tutorial_initialized = False

# cutscene function
def draw_cutscene_text(text, x, y, max_chars=None):
    font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 27)

    if max_chars:
        text = text[:max_chars]

    text_surface = font.render(text, True, (255, 255, 255))
    WINDOW.blit(text_surface, (x, y))

# Pokemon-style dialogue box function
def draw_pokemon_dialogue_box(text, char_index, show_continue_prompt=False, speaker=""):
    # Dialogue box dimensions and position (smaller)
    box_width = 500
    box_height = 100
    box_x = (WINDOW_WIDTH - box_width) // 2
    box_y = WINDOW_HEIGHT - box_height - 20
    
    # Draw dialogue box background (grey with blue border)
    pygame.draw.rect(WINDOW, (128, 128, 128), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(WINDOW, (0, 0, 150), (box_x, box_y, box_width, box_height), 4)
    
    # Draw speaker name if provided
    if speaker:
        speaker_font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 18)
        speaker_text = speaker_font.render(speaker + ":", True, (255, 255, 0))
        WINDOW.blit(speaker_text, (box_x + 10, box_y + 5))
    
    # Draw text character by character
    font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 20)
    display_text = text[:char_index]
    
    # Word wrap
    words = display_text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] < box_width - 40:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)
    
    # Draw lines
    text_y_offset = 30 if speaker else 15
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (0, 0, 0))
        WINDOW.blit(text_surface, (box_x + 20, box_y + text_y_offset + i * 25))
    
    # Draw continue prompt (blinking indicator)
    if show_continue_prompt:
        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0:  # Blink every 500ms
            prompt_font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 18)
            prompt_text = prompt_font.render("▼", True, (0, 0, 150))
            WINDOW.blit(prompt_text, (box_x + box_width - 30, box_y + box_height - 25))

# Classes

# Player Class
class Player():
    def __init__(self):
        self.player_now = None
        self.x = 250
        self.y = 450
        self.player_image = pygame.image.load(resource_path('assets/x/KNIGHT2.png')).convert_alpha()
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
        self.health = 3
        self.max_health = 3
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
        self.image = pygame.image.load(resource_path("assets/x/SPIKE.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.hitbox = pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 10)

    def update(self):
        self.hitbox.topleft = (self.x, self.y)

    def collisions(self, player):
        if self.hitbox.colliderect(player.hitbox):
            global damage_flash_time
            damage_sound.play()
            player.health -= 1
            damage_flash_time = pygame.time.get_ticks()
            player.x = 100
            player.y = 500
            player.hitbox.topleft = (player.x, player.y)


# Enemy Class (fix and use later)
class Enemy():
    def __init__(self, x, y, width, height, platform_rect):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platform = platform_rect
        self.move_speed = 2
        self.direction = 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mode = "patrol"

    def patrol(self):
        self.x += self.move_speed * self.direction  # if self.direction is negative then the enemy will move to the left side, positive for the right side

        # Left boundary
        if self.x <= self.platform.left:
            self.direction = 1  # move to the right side

        # Right boundary
        if self.x + self.width >= self.platform.right:
            self.direction = -1

    def chase(self):
        if player.x > self.x:  # if player is past the enemy
            self.direction = 1  # move --> way

        else:
            self.direction = -1  # move <-- way

        self.x += self.move_speed * 1.5 * self.direction

    def check_player(self, player):
        if (
                player.rect.bottom == self.platform.top and self.platform.left <= player.rect.centerx <= self.platform.right):
            self.mode = "chase"

        else:
            self.mode = "patrol"

    def update(self, player):
        self.check_player(player)

        if self.mode == "patrol":
            self.patrol()
        elif self.mode == "chase":
            self.chase(player)

        self.rect.topleft = (self.x, self.y)

    def draw(self):
        pygame.draw.rect(WINDOW, (150, 0, 0), self.rect)


class Torch():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

        self.image = pygame.image.load(resource_path("assets/x/TORCH.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.current_alpha = 255
        self.min_alpha = 100
        self.max_alpha = 255

    def update(self):
        """Flicker randomly"""
        self.current_alpha = random.randint(self.min_alpha, self.max_alpha)

    def draw(self, surface):
        """Draw torch with flicker"""
        torch_copy = self.image.copy()
        torch_copy.set_alpha(int(self.current_alpha))
        surface.blit(torch_copy, (self.x, self.y))

# Level Counter Class
class level_counter():
    def __init__(self, number):
        self.number = number

    def text(self):
        fontObj = pygame.font.Font(resource_path('assets/x/FONT.ttf'), int(32 / 2))
        textSufaceObj = fontObj.render("Level: " + str(self.number), True, TEXT_COLOR, None)
        return textSufaceObj

    def set_number(self, newNumber):
        self.number = newNumber

level_counter1 = level_counter(1)

# Score Counter Class
class score_counter():
    def __init__(self):
        pass

    def text(self, coin_list=None):
        fontObj = pygame.font.Font(resource_path('assets/x/FONT.ttf'), int(32 / 2))
        textSufaceObj = fontObj.render("Points: " + str(points), True, TEXT_COLOR, None)
        return textSufaceObj


class FadeBackground:
    def __init__(self, screen_width, screen_height, max_alpha=255, duration=2000):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_alpha = max_alpha
        self.duration = duration

        # State attributes to check current conditions
        self.current_alpha = 0
        self.start_time = 0
        self.is_fading = False
        self.fade_type = "in"

        # Create the overlay surface
        self.overlay = pygame.Surface((screen_width, screen_height))
        self.overlay.fill((0, 0, 0))

    def start_fade_in(self):
        self.fade_type = "in"
        self.current_alpha = 0
        self.start_time = pygame.time.get_ticks()
        self.is_fading = True

    def update(self):
        if self.is_fading == False:
            return self.is_fading
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        if self.fade_type == "in":
            self.current_alpha = int(self.max_alpha * progress)
        if self.fade_type == "out":
            self.current_alpha = int(self.max_alpha * (1 - progress))
        if progress >= 1.0:
            self.is_fading = False

    def draw(self, screen):
        if self.current_alpha > 0:
            self.overlay.set_alpha(self.current_alpha)
            screen.blit(self.overlay, (0, 0))


# pygame.draw.circle(surface, color, center_coordinates, radius, width=0)

# sprite sheet?
# spinning coin
# spilt sprite sheet
# fix sheet


# Score counter
# When player collides --> coin dissapears and score goes up by 1


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
            pygame.draw.circle(WINDOW, (255, 215, 0), (int(self.x + self.width / 2), int(self.y + self.height / 2)),
                               self.width // 2)

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

# Portal Class
class Portal():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 125
        self.height = 125
        self.image = pygame.image.load(resource_path('assets/x/image (4).png'))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.hitbox = pygame.Rect(self.x + 25, self.y + 20, 75+25, 85)
        self.float_offset = 0
        self.base_y = self.y

    def update(self, player):
        self.hitbox.topleft = (self.x + 25, self.y + 20)

        if self.hitbox.colliderect(player.hitbox) and player.vel_y > 0:
            return True

        return False

    def draw(self, surface):
        #pygame.draw.circle(surface, (100, 100, 255, 50), (self.x+60, self.y+60), 70)
        surface.blit(self.image, (self.x, self.y))
        # debugging line to see the outline of the hitbox
        #pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.hitbox.topleft = (self.x + 25, self.y + 20)

    def animate(self):
        self.float_offset += 0.08
        self.y = self.base_y + int(math.sin(self.float_offset) * 10)
        self.hitbox.topleft = (self.x + 10, self.y + 10)

portal = Portal(650 - 100 - 15, 150)

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
        self.scale = 1

    def render_button(self):
        pygame.draw.rect(WINDOW, self.color, self.hitbox, 0, 5)

    def click(self):
        click_sound.play()

    def draw_text(self, text, font, button):
        txt = font.render(text, True, GREY)
        tx = button.x + button.width / 2 - txt.get_width() / 2
        ty = button.y + button.height / 2 - txt.get_height() / 2

        WINDOW.blit(txt, (tx, ty))


class Shop:
    def __init__(self):
        self.data = {
            "knight": {"price": 0},
            "wizard": {"price": 10},
            "archer": {"price": 12}
        }
        self.unlocked = {
            "knight": True,
            "wizard": False,
            "archer": False
        }
        self.current_skin = "knight"

    def is_unlocked(self, name):
        return self.unlocked.get(name, False)

    def buy(self, name, current_points):
        if name not in self.data:
            return False, "Unknown item.", current_points
        if self.is_unlocked(name):
            return False, f"{name.title()} is already unlocked.", current_points

        price = self.data[name]["price"]
        if current_points < price:
            return False, f"Not enough points for {name.title()}.", current_points

        self.unlocked[name] = True
        return True, f"{name.title()} purchased!", current_points - price

    def is_valid_item(self, name):
        return name in self.data

    def get_price(self, name):
        if not self.is_valid_item(name):
            return None
        return self.data[name]["price"]

    def get_status_text(self, name):
        if not self.is_valid_item(name):
            return "Unknown"
        if self.is_unlocked(name):
            if self.current_skin == name:
                return "Equipped"
            return "Unlocked"
        return f"Price: {self.get_price(name)}"

    def can_buy(self, name, current_points):
        if not self.is_valid_item(name):
            return False
        if self.is_unlocked(name):
            return False
        return current_points >= self.get_price(name)

    def render_shop(self, window, mouse_pos, points, knight_img, wizard_img, archer_img):
        title_font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 32)
        body_font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 20)
        small_font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 16)

        window.fill((35, 35, 40))

        title = title_font.render("Shop", True, (230, 230, 230))
        window.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 40))

        points_text = body_font.render(f"Your points: {points}", True, (255, 215, 0))
        window.blit(points_text, (40, 40))

        items = [
            ("knight", knight_img, (100, 160)),
            ("wizard", wizard_img, (320, 160)),
            ("archer", archer_img, (540, 160)),
        ]

        buy_buttons = {}

        for item_name, item_image, pos in items:
            card_rect = pygame.Rect(pos[0], pos[1], 180, 250)
            pygame.draw.rect(window, (60, 60, 70), card_rect, border_radius=8)
            pygame.draw.rect(window, (95, 95, 110), card_rect, 3, border_radius=8)

            img = pygame.transform.scale(item_image, (100, 100))
            window.blit(img, (card_rect.centerx - 50, card_rect.y + 20))

            name_text = body_font.render(item_name.title(), True, (230, 230, 230))
            window.blit(name_text, (card_rect.centerx - name_text.get_width() // 2, card_rect.y + 130))

            if self.is_unlocked(item_name):
                status = small_font.render("Unlocked", True, (120, 255, 120))
                btn_label = "Owned"
                normal_color = (110, 110, 120)
                hover_color = (90, 90, 100)
            else:
                price = self.get_price(item_name)
                status = small_font.render(f"Price: {price}", True, (255, 215, 0))
                btn_label = "Buy"
                normal_color = (110, 140, 200)
                hover_color = (90, 120, 180)

            window.blit(status, (card_rect.centerx - status.get_width() // 2, card_rect.y + 160))

            buy_btn = button(card_rect.x + 25, card_rect.y + 190, 130, 40, normal_color, btn_label, None)
            if buy_btn.hitbox.collidepoint(mouse_pos):
                buy_btn.color = hover_color
            buy_btn.render_button()

            btn_text = small_font.render(buy_btn.text, True, (245, 245, 245))
            window.blit(btn_text, (
                buy_btn.hitbox.centerx - btn_text.get_width() // 2,
                buy_btn.hitbox.centery - btn_text.get_height() // 2
            ))

            buy_buttons[item_name] = buy_btn

        back_btn = button(640, 520, 120, 45, (140, 80, 80), "Back", None)
        if back_btn.hitbox.collidepoint(mouse_pos):
            back_btn.color = (120, 65, 65)
        back_btn.render_button()

        back_text = small_font.render("Back", True, (255, 255, 255))
        window.blit(back_text, (
            back_btn.hitbox.centerx - back_text.get_width() // 2,
            back_btn.hitbox.centery - back_text.get_height() // 2
        ))

        return buy_buttons, back_btn

shop = Shop()

class CreatorCard:
    def __init__(self, x, y, title, summary, details):
        self.x = x
        self.y = y
        self.title = title
        self.summary = summary
        self.details = details  # list of strings

        self.base_w = 180+25
        self.base_h = 120+25
        self.hover_w = 230+25
        self.hover_h = 190+25

        self.current_w = float(self.base_w)
        self.current_h = float(self.base_h)

    def update(self, mouse_pos):
        rect = pygame.Rect(self.x, self.y, int(self.current_w), int(self.current_h))
        is_hovered = rect.collidepoint(mouse_pos)

        target_w = self.hover_w if is_hovered else self.base_w
        target_h = self.hover_h if is_hovered else self.base_h

        # smooth expansion / shrink
        speed = 0.18
        self.current_w += (target_w - self.current_w) * speed
        self.current_h += (target_h - self.current_h) * speed

        return is_hovered

    def draw(self, surface, title_font, body_font, is_hovered):
        rect = pygame.Rect(self.x, self.y, int(self.current_w), int(self.current_h))

        bg_color = (35, 35, 45) if not is_hovered else (45, 55, 75)
        border_color = (90, 120, 180) if not is_hovered else (130, 190, 255)

        pygame.draw.rect(surface, bg_color, rect, border_radius=12)
        pygame.draw.rect(surface, border_color, rect, width=3, border_radius=12)

        title_surf = title_font.render(self.title, True, (235, 235, 245))
        surface.blit(title_surf, (rect.x + 12, rect.y + 10))

        summary_surf = body_font.render(self.summary, True, (185, 195, 215))
        surface.blit(summary_surf, (rect.x + 12, rect.y + 45))

        if is_hovered:
            y = rect.y + 75
            for line in self.details:
                detail_surf = body_font.render("- " + line, True, (215, 225, 245))
                surface.blit(detail_surf, (rect.x + 12, y))
                y += 22


creator_cards = [
    CreatorCard(90-20-25, 180, "About Me", "Indie dev + student-athlete", [
        "Built this game over 2 years",
        "Focused on level feel",
        "Enjoys fantasy platformers"
    ]),
    CreatorCard(310-10, 180, "Game Features", "Systems in this game", [
        "Physics + collision",
        "Cutscenes + music",
        "Portals, spikes, coins"
    ]),
    CreatorCard(530-5+25+5, 180, "Thanks", "People who helped", [
        "Playtesters and friends",
        "Feedback improved balance",
        "Thank you for playing"
    ]),
]

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
    global player
    global level, show_message2, selected_character, show_message3, showMessage, startTime, showMessage2, startTime2
    global WINDOW, damage_flash_time
    global background, torch_list
    global secret_obstacle_list, play_music
    global tutorial_initialized
    global spikes
    global show_message
    global points, points_added
    global menu_jump_timer, menu_on_ground, menu_x_speed, menu_y_speed, menu_y, menu_x
    global jumping_sound, overlay
    global shop, shop_notice_text, shop_notice_until, skins_notice_text, skins_notice_until
    global fade_bg, level5_cutscene_fade_started

    player = Player()
    
    # Create fade background instance
    fade_bg = FadeBackground(WINDOW_WIDTH, WINDOW_HEIGHT, max_alpha=255, duration=3000)

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
    # pulse_value = 0
    # if level == 5:
    # pulse_value = abs(pygame.frame.get_ticks() % 600 - 300) / 300
    global glow_counter
    ### Obstacle Setup ###
    obstacle_list = []
    spikes = []
    # level 1 obstacles
    obstacle_list.clear()
    ob1 = pygame.Rect(290+20+20, 395 + 15, 150, 40)
    ground = pygame.Rect(0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50)
    obstacle_list = [ob1, ground]

    ### Portal ###
    portal = Portal(650-100-15, 150)
    coin_list = []

    coin1 = Coin(ob1.left + ob1.width / 2 - 20 - 15, ob1.top - 25 - 15)
    coin_list.append(coin1)

    coin2 = Coin(ob1.left + ob1.width / 2 + 15, ob1.top - 25 - 15)
    coin_list.append(coin2)

    # spike = pygame.image.load('SPIKE.png').convert_alpha()
    # spike = pygame.transform.scale(spike, (50,50))

    # testing
    level_counter1 = level_counter(1)
    coin_counter = score_counter()
    game_state = 'gameplay'
    # The main game loop
    game_state = 'gameMenu'

    while looping:

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if keys[pygame.K_LCTRL] and keys[pygame.K_LSHIFT] and keys[pygame.K_r]:
            pygame.quit()
            # subprocess.call([sys.executable, __file__])  # Not supported in web
            sys.exit()

        if game_state == 'gameMenu':
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(resource_path("assets/x/music0.ogg"))
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(-1)

            mouseClicked = False
            knight_selected = True
            wizard_selected = False

            button_width = 260
            button_height = 50

            mouse_pos = pygame.mouse.get_pos()

            background_img = pygame.image.load(resource_path('assets/x/DUNGEON.jpg')).convert_alpha()
            background_img = pygame.transform.scale(background_img, (800, 600))
            WINDOW.blit(background_img, (0, 0))

            title_font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 42    )
            title_text = "Dungeon Platformer"

            # shadow for title
            shadow_surface = title_font.render(title_text, True, (0, 0, 0))
            x = int(WINDOW.get_width() / 2 - shadow_surface.get_width() / 2)
            y = int(WINDOW.get_height() / 2 - 45 - shadow_surface.get_height() / 2) - 35
            WINDOW.blit(shadow_surface, (x + 3, y + 3))
            title_surface = title_font.render(title_text, True, TEXT_COLOR)
            WINDOW.blit(title_surface, (x, y))

            # Start Button
            font = pygame.font.Font('assets/x/early-gameboy.ttf', 25)
            sx = 280
            sy = 250 + 10 + 17.5 + 17.5 + 5 + 2
            start_button = button(sx, sy, button_width, button_height, (160, 160, 160), 'start', None)

            if start_button.hitbox.collidepoint(mouse_pos):
                start_button.color = (130, 130, 130)
            else:
                start_button.color = (160, 160, 160)

            start_button.render_button()
            font = pygame.font.Font('assets/x/early-gameboy.ttf', 25)

            txt = font.render("Start", True, GREY, None)
            tx = sx + button_width/2 - txt.get_width()/2
            ty = sy + button_height/2 - txt.get_height()/2

            WINDOW.blit(txt, (tx, ty))

            # Creator Button
            x = 280
            y = 330 + 17.5 + 17.5 - 2.5
            button2 = button(x, y, button_width, button_height, (160, 160, 160), 'creator', None)
            if button2.hitbox.collidepoint(mouse_pos):
                button2.color = (130, 130, 130)
            else:
                button2.color = (160, 160, 160)

            button2.render_button()
            font = pygame.font.Font('assets/x/early-gameboy.ttf', 25)
            txt = font.render("Creator", True, GREY, None)
            tx = x + button2.width / 2 - 30 - 5 - 10 -15 - 7.5 - 10 - 7
            ty = y + button2.height / 2 - 5 - 5 - 5
            WINDOW.blit(txt, (tx, ty))

            # Tutorial Button
            x = 280
            y = 410 + 17.5
            tb = button(x, y, button_width, button_height, (160, 160, 160), 'tutorial', None)

            if tb.hitbox.collidepoint(mouse_pos):
                tb.color = (130, 130, 130)
            else:
                tb.color = (160, 160, 160)

            tb.render_button()
            txt = font.render("Tutorial", True, GREY, None)
            tx = tb.x + tb.width / 2 - 30 - 5 - 35 - 24
            ty = tb.y + tb.height / 2 - 5 - 5 - 6
            WINDOW.blit(txt, (tx, ty))

            # Characters Button
            x = 50 + tb.width / 3 + 150
            y = 20
            new_x = 280
            new_y = 490
            skins = button(new_x, new_y, button_width, button_height, (160, 160, 160), 'Characters', None)

            if skins.hitbox.collidepoint(mouse_pos):
                skins.color = (130, 130, 130)
            else:
                skins.color = (160, 160, 160)

            # Open World Button
            x_value = 280 + 100
            y_value = 490 + 100
            shop_button = button(x_value, y_value, button_width, button_height, (160, 160, 160), 'Shop', None)

            if shop_button.hitbox.collidepoint(mouse_pos):
                shop_button.color = (130, 130, 130)
            else:
                shop_button.color = (160, 160, 160)

            skins.render_button()
            text = font.render("Open World", True, GREY, None)
            x = skins.x + skins.width / 2 - 50 - 7.5 + 45 - 15 - 20 - 50 - 10
            y = skins.y + skins.height / 2 - 10 - 6
            WINDOW.blit(text, (x, y))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Character Button
                    if start_button.hitbox.collidepoint(mouse_x, mouse_y):
                        game_state = "charecter_select"
                        start_button.click()
                    # Creator Button
                    elif button2.hitbox.collidepoint(mouse_x, mouse_y):
                        game_state = 'creator'
                        button2.click()
                    # Tutorial Button
                    elif tb.hitbox.collidepoint(mouse_x, mouse_y):
                        tb.click()
                        selected_character = "knight"
                        game_state = 'tutorial_level'
                    # Open World Button
                    elif skins.hitbox.collidepoint(mouse_x, mouse_y):
                        skins.click()
                        game_state = 'open_world'


            if showMessage:
                elapsed = pygame.time.get_ticks() - startTime
                duration_ms = 2500
                if elapsed < duration_ms:
                    fontobj = pygame.font.Font(None, 32)
                    msg = "Choose a character from the Characters menu to play."
                    WINDOW.blit(fontobj.render(msg, True, (255, 255, 255)), (300 - 150, 300 - 75 - 75))
                else:
                    showMessage = False

            if showMessage2:
                elapsed2 = pygame.time.get_ticks() - startTime2
                duration_ms2 = 2500
                if elapsed2 < duration_ms2:
                    fontobj = pygame.font.Font(None, 32)
                    msg2 = "Choose a character from the Characters menu to play."
                    WINDOW.blit(fontobj.render(msg2, True, (255, 255, 255)), (300 - 150, 300 - 75 - 75))
                else:
                    showMessage2 = False
            # player animation
            menu_x += menu_x_speed

            if menu_x > WINDOW_WIDTH:
                menu_x = -64

            menu_jump_timer += 1
            if menu_jump_timer > 120 / 2 and menu_on_ground:  # 120 frames = 2 seconds [this value sets how much the character jumps when going across the screen
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

        # SHOP (replace this section)
        elif game_state == "open_world":
            pass

        elif game_state == 'tutorial_level':
            # Exit Button
            exit_button = button(exit_button_rect.x, exit_button_rect.y, exit_button_rect.width,
                                 exit_button_rect.height, 'orange', 'exit', None)
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
                        exit_button.click()
                        game_state = 'gameMenu'
                        level = 1

                        # reset tutorial objects
                        obstacle_list.clear()
                        spikes.clear()
                        tutorial_initialized = False

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
                spikes.append(Spike(ob2.x + 60, ob2.y - 60 + 15))
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
                obstacle_list = [ob1, ob2, ground]

                tutorial_initialized = True

            # --- Input ---
            keys = pygame.key.get_pressed()
            player.vel_x = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.vel_x = -player.move_speed
                if selected_character == "wizard":
                    player.player_now = wizard
                elif selected_character == "archer":
                    player.player_now = archer
                else:  # knight
                    player.player_now = knight
                player.facing_left = True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.vel_x = player.move_speed
                if selected_character == "wizard":
                    player.player_now = pygame.transform.flip(wizard, True, False)
                elif selected_character == "archer":
                    player.player_now = pygame.transform.flip(archer, True, False)
                else:  # knight
                    player.player_now = pygame.transform.flip(knight, True, False)
                player.facing_left = False
            if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and player.on_ground:
                jumping_sound.play()
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

            WINDOW.blit(background, (0, 0))
            WINDOW.blit(text_surface, (200 - 75, 150))
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

            # WINDOW.blit(Spike.image, Spike.hitbox.topleft)

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
                exit_button.click()
                game_state = 'gameMenu'


        # Creator Page
        elif game_state == 'creator':
            global creator_music_playing
            # mouseClicked = False
            WINDOW.fill('darkgrey')

            Titlefontobj = pygame.font.Font(None, 64)
            if not creator_music_playing:
                pygame.mixer.music.load(resource_path("assets/x/CREATOR_MUSIC.ogg"))
                pygame.mixer.music.set_volume(2.5)
                pygame.mixer.music.play(-1)
                creator_music_playing = True

            mouse_pos = pygame.mouse.get_pos()

            title_font = pygame.font.Font(None, 32)
            body_font = pygame.font.Font(None, 22)

            for card in creator_cards:
                hovered = card.update(mouse_pos)
                card.draw(WINDOW, title_font, body_font, hovered)

            # Exit Button
            exit_button = button(600, 500 - 75 + 100 - 50 + 5 + 5, 100, 100, 'orange', 'exit', None)
            exit_button.render_button()
            exitfontobj = pygame.font.Font(None, 32)

            # Exit Button text
            ExitText = exitfontobj.render("Exit", True, TEXT_COLOR, None)
            x = 600 + 50 - 25
            y = 500 - 75 + 50 - 25 + 15 + 50 + 5 + 5

            WINDOW.blit(ExitText, (x, y))

            Titlefontobj = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 96)
            Title = Titlefontobj.render("Creator", True, (220, 240, 255))
            x = WINDOW_WIDTH // 2 - Title.get_width() // 2
            y = 40
            WINDOW.blit(Title, (x, y))

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
                exit_button.click()
                game_state = 'gameMenu'
                creator_music_playing = False

        # win screen
        elif game_state == 'win':
            WINDOW.fill('grey')
            font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 35)
            text = font.render("YOU WIN!", True, (255, 255, 255))
            x = WINDOW_WIDTH // 2 - text.get_width() // 2
            y = WINDOW_HEIGHT // 2 - 200
            WINDOW.blit(text, (x, y))

            smaller_font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 18)
            text2 = smaller_font.render("Show this screen and collect your prize!", True, (255, 255, 255))
            x = WINDOW_WIDTH // 2 - text2.get_width() // 2
            y = WINDOW_HEIGHT // 2 + 150 - 275
            WINDOW.blit(text2, (x, y))

            text3 = font.render("Hold control shift r to restart.", True, (255, 255, 255))
            x = WINDOW_WIDTH // 2 - text3.get_width() // 2
            y = WINDOW_HEIGHT // 2 + 150 - 275 + 75
            WINDOW.blit(text3, (x, y))

            start_x = -100
            end_x = 400

            player_x = start_x
            player_y = 250
            player_speed = 2 # pixels per frame

            if player_x < end_x:
                player_x += player_speed
                if player_x > end_x:
                    player_x = end_x  # ensure it stops exactly at target
            #WINDOW.blit(player_image, (player.x, player.y))


            if player_x == end_x:
                pass # start showing text and the next part of the cutscene



            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.quit()
                        os.system(f'python "{__file__}"')
                        sys.exit()

        elif game_state == 'cutscene':
            global cutscene_phase, cutscene_start_time, cutscene_text_index, cutscene_char_index, darkness_alpha, damage_flash_time

            WINDOW.blit(background, (0, 0))
            if not play_music:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(resource_path("assets/x/cutscene.ogg"))
                pygame.mixer.music.set_volume(1.5)
                pygame.mixer.music.play(-1)  # -1 makes it loop forever
                play_music = True

            # ===== PHASE 1: Story Text =====
            if cutscene_phase == 0:
                if cutscene_start_time == 0:
                    cutscene_start_time = pygame.time.get_ticks()

                elapsed = pygame.time.get_ticks() - cutscene_start_time

                # Show first text line (0-3 seconds)
                if elapsed < 3000:
                    cutscene_char_index = int((elapsed / 3000) * len(cutscene_texts[0]))
                    draw_cutscene_text(cutscene_texts[0][:cutscene_char_index], 20, 200)

                # Show second text line (3-6 seconds)
                elif elapsed < 6000:
                    draw_cutscene_text(cutscene_texts[0], 20, 200)
                    cutscene_char_index = int(((elapsed - 3000) / 3000) * len(cutscene_texts[1]))
                    draw_cutscene_text(cutscene_texts[1][:cutscene_char_index], 50, 280)
                # Show third text line (6-9 seconds)
                elif elapsed < 9000:
                    draw_cutscene_text(cutscene_texts[0], 20, 200)
                    draw_cutscene_text(cutscene_texts[1], 20, 280)
                    cutscene_char_index = int(((elapsed - 6000) / 3000) * len(cutscene_texts[2]))
                    draw_cutscene_text(cutscene_texts[2][:cutscene_char_index], 50, 360)

                # All text shown, wait 1 second then move to phase 2
                if elapsed > 10000:
                    cutscene_phase = 1
                    cutscene_start_time = pygame.time.get_ticks()
                    darkness_alpha = 0
                else:
                    # Allow SPACE to skip early
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        cutscene_phase = 1
                        cutscene_start_time = pygame.time.get_ticks()
                        darkness_alpha = 0

            # ===== PHASE 2: Character Walks Across Screen =====
            elif cutscene_phase == 1:
                if cutscene_start_time == 0:
                    cutscene_start_time = pygame.time.get_ticks()

                elapsed = pygame.time.get_ticks() - cutscene_start_time
                walk_duration = 4350  # milliseconds

                # Character position (left to right)
                progress = elapsed / walk_duration  # 0.0 to 1.0
                char_x = -100 + (progress * (WINDOW_WIDTH + 200))  # -100 to 900

                # Darkness increases as character walks
                darkness_alpha = int(200 * progress)  # 0 to 200

                # Draw character
                if selected_character == "wizard":
                    wizard_flipped = pygame.transform.flip(wizard, True, False)
                    WINDOW.blit(wizard_flipped, (char_x, 250))
                elif selected_character == "archer":
                    archer_flipped = pygame.transform.flip(archer, True, False)
                    WINDOW.blit(archer_flipped, (char_x, 250))
                else:  # knight
                    knight_flipped = pygame.transform.flip(knight, True, False)
                    WINDOW.blit(knight_flipped, (char_x, 250))

                # Draw darkness overlay
                darkness_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                darkness_surface.fill((0, 0, 0))
                darkness_surface.set_alpha(darkness_alpha)
                WINDOW.blit(darkness_surface, (0, 0))

                # Move to phase 3 when walk is done
                if elapsed > walk_duration:
                    cutscene_phase = 2
                    cutscene_start_time = 0
                    darkness_alpha = 200

            # ===== PHASE 3: Press SPACE to Continue =====
            elif cutscene_phase == 2:
                # Black screen
                WINDOW.fill((0, 0, 0))

                # Text
                font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 20)
                text_surface = font.render("Press SPACE to begin your journey...", True, (255, 255, 255))
                x = WINDOW_WIDTH // 2 - text_surface.get_width() // 2
                y = WINDOW_HEIGHT // 2
                WINDOW.blit(text_surface, (x, y))

                # Wait for SPACE
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    # Reset to Level 1
                    level = 1
                    level_counter1.set_number(1)

                    # Reset player
                    player.health = player.max_health
                    player.x = 100
                    player.y = 500
                    player.vel_x = 0
                    player.vel_y = 0

                    # Reset obstacles
                    ob1 = pygame.Rect(290+20, 395 + 15, 100, 50)
                    ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
                    obstacle_list = [ob1, ground]
                    spikes.clear()
                    coin_list = []

                    # Add coins to level 1
                    coin1 = Coin(ob1.left + ob1.width / 2 - 20 - 15, ob1.top - 25 - 15)
                    coin_list.append(coin1)
                    coin2 = Coin(ob1.left + ob1.width / 2 + 15, ob1.top - 25 - 15)
                    coin_list.append(coin2)

                    # Reset portal
                    portal.set_position(650 - 100 - 7.5, 150 - 25)
                    damage_flash_time = 0

                    # Start gameplay
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(resource_path("assets/x/music0.ogg"))
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                    play_music = False
                    game_state = 'gameplay'

                    # Reset cutscene variables for next time
                    cutscene_phase = 0
                    cutscene_start_time = 0

            # Handle quit event
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

        elif game_state == 'level5_cutscene':
            global level5_cutscene_active, level5_cutscene_text_index, level5_cutscene_char_index, level5_cutscene_last_char_time, level5_cutscene_complete

            # Draw background
            WINDOW.blit(background, (0, 0))

            # Draw mysterious figure on the right side
            figure_x = 550
            figure_y = 250
            figure_float_offset = math.sin(pygame.time.get_ticks() * 0.003) * 5
            WINDOW.blit(mysterious_figure, (figure_x, figure_y + figure_float_offset))

            # Draw player on the left side (facing right toward the figure)
            player_x = 150
            player_y = 280
            if selected_character == "wizard":
                player_img = pygame.transform.flip(wizard, True, False)
            elif selected_character == "archer":
                player_img = pygame.transform.flip(archer, True, False)
            else:
                player_img = pygame.transform.flip(knight, True, False)
            WINDOW.blit(player_img, (player_x, player_y))

            # Draw interaction effect (glowing line between them)
            interaction_alpha = int(100 + 50 * math.sin(pygame.time.get_ticks() * 0.005))
            interaction_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(interaction_surface, (150, 100, 255, interaction_alpha),
                           (player_x + 50, player_y + 30), (figure_x + 60, figure_y + 50 + figure_float_offset), 3)
            WINDOW.blit(interaction_surface, (0, 0))

            # Typewriter effect - add characters over time
            current_time = pygame.time.get_ticks()
            if current_time - level5_cutscene_last_char_time > 30:  # 30ms per character
                if level5_cutscene_text_index < len(level5_cutscene_texts):
                    if level5_cutscene_char_index < len(level5_cutscene_texts[level5_cutscene_text_index]):
                        level5_cutscene_char_index += 1
                        level5_cutscene_last_char_time = current_time

            # Check if current line is complete
            if level5_cutscene_text_index < len(level5_cutscene_texts):
                line_complete = level5_cutscene_char_index >= len(level5_cutscene_texts[level5_cutscene_text_index])
            else:
                line_complete = True

            # Draw dialogue box with speaker
            if level5_cutscene_text_index == 0:
                speaker = "Player"
            elif level5_cutscene_text_index == 1:
                speaker = "Player"
            elif level5_cutscene_text_index == 2:
                speaker = "Cloaked Figure"
            elif level5_cutscene_text_index == 3:
                speaker = "Cloaked Figure"
            elif level5_cutscene_text_index == 4:
                speaker = ""
            else:
                speaker = ""

            # Only draw dialogue if index is within bounds
            if level5_cutscene_text_index < len(level5_cutscene_texts):
                draw_pokemon_dialogue_box(
                    level5_cutscene_texts[level5_cutscene_text_index],
                    level5_cutscene_char_index,
                    show_continue_prompt=line_complete,
                    speaker=speaker
                )

            # Update fade animation
            fade_bg.update()

            # Start fade when all dialogue is complete
            if level5_cutscene_text_index >= len(level5_cutscene_texts) and not fade_bg.is_fading and not level5_cutscene_fade_started:
                fade_bg.start_fade_in()
                level5_cutscene_fade_started = True

            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if line_complete:
                            # Move to next line
                            level5_cutscene_text_index += 1
                            level5_cutscene_char_index = 0

                            # Check if cutscene is complete
                            if level5_cutscene_text_index >= len(level5_cutscene_texts):
                                level5_cutscene_complete = True
                        else:
                            # Skip to end of current line
                            level5_cutscene_char_index = len(level5_cutscene_texts[level5_cutscene_text_index])

            # If cutscene is complete and fade is done, transition to level 6
            if level5_cutscene_complete and fade_bg.current_alpha >= 255:
                # Reset cutscene variables
                level5_cutscene_active = False
                level5_cutscene_text_index = 0
                level5_cutscene_char_index = 0
                level5_cutscene_last_char_time = 0
                level5_cutscene_complete = False
                level5_cutscene_fade_started = False

                # Advance to Level 6 (win state)
                game_state = 'win'

                # setting screen and background sizes less from the secret level
                background = pygame.transform.scale(background, (800, 600))

            # Draw fade overlay on top
            fade_bg.draw(WINDOW)

            pygame.display.update()

        elif game_state == "charecter_select":
            # title: choose your charecter
            # draw all of the characters in their boxes
            # characters: knight; scarlet knight; wizard; witch; healer
            WINDOW.fill('lightgrey')

            # text
            my_font = pygame.font.Font(resource_path('assets/x/FONT.ttf'), 24)
            # font2 = pygame.font.Font(None, 75)
            text = my_font.render("Click to choose your character", True, (0, 0, 0), None)
            x = 125 - 75 - 20 - 7.5
            y = 40 + 20 + 25
            WINDOW.blit(text, (x, y))

            # knight image
            knight2 = pygame.transform.scale(knight, (240 - 30 - 20, 240 - 30 - 20))
            WINDOW.blit(knight2, (125 - 50 - 25 + 50 - 10 + 20 - 5, 200 - 20 - 25 + 40))

            # knight text
            font3 = pygame.font.Font(None, 32)
            text = font3.render("Knight", True, (0, 0, 0), None)
            WINDOW.blit(text, (130 + 15, 335))

            # make hitbox
            hitbox = knight.get_rect()
            hitbox.topleft = (125, 200)

            # wizard image
            wizard_image = pygame.image.load(resource_path("assets/x/WIZARD.png")).convert_alpha()
            wizard_image = pygame.transform.scale(wizard_image, (200, 200))
            WINDOW.blit(wizard_image, (265 - 25, 200))

            # wizard text
            text = font3.render("Wizard", True, (0, 0, 0), None)
            WINDOW.blit(text, (130 + 15 + 125 + 20, 335))

            # make hitbox2
            hitbox2 = wizard_image.get_rect()
            hitbox2.topleft = (225, 200)

            # archer image
            archer_image = pygame.image.load(resource_path("assets/x/KNIGHT.png")).convert_alpha()
            archer_image = pygame.transform.scale(archer_image, (120, 120))
            WINDOW.blit(archer_image, (265 - 25 + 15 + 250 - 100 + 30 - 10, 200))

            # archer text
            archer_text = font3.render("Archer", True, (0, 0, 0), None)
            WINDOW.blit(archer_text, (130 + 15 + 125 + 20 + 125 + 30 - 10, 335))

            # make hitbox3
            hitbox3 = archer_image.get_rect()
            hitbox3.topleft = (130 + 15 + 125 + 20 + 125, 335)

            # rectangle borders
            border = pygame.Rect(130 - 25, 200, 170 - 25, 170)
            pygame.draw.rect(WINDOW, (0, 0, 0), border, width=5)

            border2 = pygame.Rect(130 - 25 + 150, 200, 170 - 25, 170)
            pygame.draw.rect(WINDOW, (0, 0, 0), border2, width=5)

            border3 = pygame.Rect(130 - 25 + 150 + 175 - 20 - 3.5, 200, 170 - 25, 170)
            pygame.draw.rect(WINDOW, (0, 0, 0), border3, width=5)

            # elf image
            # elf = pygame.image.load("ELF.png").convert_alpha()
            # elf = pygame.transform.scale(elf, (100, 100))
            # WINDOW.blit(elf, (445, 200))

            # Exit Button
            exit_button = button(600, 500 - 75, 100+25, 100, 'orange', 'exit', None)
            exit_button.render_button()
            exitfontobj = pygame.font.Font(None, 32)

            # Exit Button text
            ExitText = exitfontobj.render("Continue", True, TEXT_COLOR, None)
            x = 600 + 50 - 25 - 20+10
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
                if selected_character is None:
                    exit_button.click()
                    skins_notice_text = "Choose a character first!"
                    skins_notice_until = pygame.time.get_ticks() + 2000
                else:
                    exit_button.click()
                    game_state = "cutscene"
                    level = 1
                    level_counter1.set_number(1)
                    ob1 = pygame.Rect(290, 395 + 15, 100, 50)
                    ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
                    obstacle_list[:] = [ob1, ground]
                    spikes.clear()
                    player.health = player.max_health
                    player.x = 100
                    player.y = 500
                    tutorial_initialized = False

            # if knight is clicked
            if hitbox.collidepoint((mouse_x, mouse_y)) and mouseClicked:
                selected_character = "knight"
                selected_sound.play()
                start_time = time.time()
                player.player_image = knight
                player.player_flipped_image = pygame.transform.flip(knight, True, False)
                player.player_now = knight
                show_message = True
                text = "Knight was selected!"
                # WINDOW.blit(k, (kx, ky)) # make the text stay for longer

            if hitbox2.collidepoint((mouse_x, mouse_y)) and mouseClicked:
                selected_character = "wizard"
                selected_sound.play()
                start_time2 = time.time()
                player.player_image = wizard
                player.player_flipped_image = pygame.transform.flip(wizard, True, False)
                player.player_now = wizard
                show_message2 = True
                text2 = "Wizard was selected!"

            if hitbox3.collidepoint((mouse_x, mouse_y)) and mouseClicked:
                selected_character = "archer"
                selected_sound.play()
                start_time3 = time.time()
                player.player_image = archer
                player.player_flipped_image = pygame.transform.flip(archer, True, False)
                player.player_now = archer
                show_message3 = True
                text3 = "Archer was selected!"

            # Show Knight text
            if show_message == True:
                if time.time() - start_time < 1:
                    WINDOW.blit(exitfontobj.render("Knight was selected!", True, (0, 0, 0)), (450 + 75, 200 - 50))
                else:
                    show_message = False

            # Show Wizard text
            if show_message2 == True:
                if time.time() - start_time2 < 1:
                    WINDOW.blit(exitfontobj.render("Wizard was selected!", True, (0, 0, 0)), (450 + 75, 200 - 50))
                else:
                    show_message2 = False

            if show_message3 == True:
                if time.time() - start_time3 < 1:
                    WINDOW.blit(exitfontobj.render("Archer was selected!", True, (0, 0, 0)), (450 + 75, 200 - 50))
                else:
                    show_message3 = False

            if pygame.time.get_ticks() < skins_notice_until:
                notice_surface = exitfontobj.render(skins_notice_text, True, (0, 0, 0))
                WINDOW.blit(notice_surface, (450, 170))


        elif game_state == 'tutorial_level':
            # Exit Button
            exit_button = button(exit_button_rect.x, exit_button_rect.y, exit_button_rect.width,
                                 exit_button_rect.height, 'orange', 'exit', None)
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
                        exit_button.click()
                        game_state = 'gameMenu'
                        level = 1

                        # reset tutorial objects
                        obstacle_list.clear()
                        spikes.clear()
                        tutorial_initialized = False

            WINDOW.fill('lightblue')

            font2 = pygame.font.SysFont(None, 36)
            text_surface = font2.render("Use the arrow or letter keys to move and jump!", True, (155, 155, 155))


        elif game_state == 'gameplay':
            # for testing
            # level = 2
            # level_changing = True
            level_changing = False
            # Get inputs
            keys = pygame.key.get_pressed()

            # Drawing backgrounds
            # WINDOW.blit(background, (0, 0))
            WINDOW.blit(middle_background, (0, 0))

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
                # coin_sound.play()
                player.on_ground = False
            if keys[pygame.K_SLASH]:
                colorImage = pygame.Surface(player.player_image.get_size()).convert_alpha()
                colorImage.fill(player.player_color)
                player.player_image.blit(colorImage, (player.x, player.y), special_flags=pygame.BLEND_RGBA_MULT)


            # portal collisions to go to the next level
            touched_portal = portal.update(player)

            if touched_portal and not level_changing:
                portal_sound.play()
                player.player_reset = True
                level += 1
                level_changing = True
                level_counter1.set_number(level)

            if level == 1 and level_changing:
                level_changing = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load(resource_path("assets/x/music0.ogg"))
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(-1)
                damage_flash_time = 0  # Reset flash timer
                portal.set_position(650-100-7.5, 150-25)
                player.x = 100
                player.y = 500

                # Step 2: set overlay color per level
                level_colors = {
                    1: (255, 255, 255),  # normal
                    2: (0, 0, 255),  # faint blue
                    3: (255, 0, 0),  # faint red
                    4: (0, 255, 0),  # faint green
                    5: (255, 165, 0),  # orange
                }

                # update the overlay color every frame in the loop
                overlay.fill(level_colors.get(level, (255, 255, 255)))  # default white if level > 5

                # level 1 obstacles
                obstacle_list.clear()
                ob1 = pygame.Rect(290+20, 395 + 15+10, 100, 50)
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
                obstacle_list = [ob1, ground]

            # Level 2
            if level == 2 and level_changing:
                level_changing = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load(resource_path("assets/x/music2.ogg"))
                pygame.mixer.music.play(-1)  # -1 makes it loop forever
                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                # obstacles
                ob2 = pygame.Rect(565 - 200 - 75 + 200, 270 + 40 + 20, 75, 40)
                ob3 = pygame.Rect(450 - 200, 450, 175, 40)
                ob5 = pygame.Rect(650 / 2 - 250 - 75 + 345 + 50 - 250 + 7000, 650 / 2 - 70 - 25, 50,
                                  40 + 7000)  # secret level block
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)

                # enemies
                # enemies = []
                # enemies.append(ob2.x + 20, ob2.y - 5, 40, 40, ob2)

                # coins
                coin1 = Coin(ob2.left + ob2.width / 2, ob2.top - 25 - 15)
                coin1.randomize_pos()
                coin_list.append(coin1)

                coin2 = Coin(ob3.left + ob3.width / 2 + 20, ob3.top - 25 - 15)
                coin_list.append(coin2)

                coin3 = Coin(ob3.left + ob3.width / 2 - 50, ob3.top - 25 - 15)
                coin_list.append(coin3)

                # torches
                torch_list = []

                # lists
                obstacle_list = [ob2, ob3, ground]
                coin_list = [coin1, coin2, coin3]

                # pygame.draw.rect(WINDOW, (255, 0, 0), enemy.player_rect)
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
                #portal_hitbox.topleft = (portal_x, portal_y)

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
                pygame.mixer.music.load(resource_path("assets/x/music3.ogg"))
                pygame.mixer.music.play(-1)  # -1 makes it loop forever

                # setting screen and background sizes less from the secret level
                background = pygame.transform.scale(background, (800, 600))

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                # ob1 = pygame.Rect(x, y, width, height)
                ob1 = pygame.Rect(375 + 7000, 600 - 100 - 200 + 100 + 50, 175, 40)
                ob2 = pygame.Rect(250 + 7000, 600 - 120 - 250 + 100 + 50 - 85, 175, 40)  # make grey
                ob4 = pygame.Rect(ob2.x - 200 + 400 + 50 + 7000, ob2.y - 125, 100, 40)

                # only visible obstacle
                ob5 = pygame.Rect(250, 400 + 20, 200 + 50 + 75, 40)

                spikes.clear()
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)

                # lists
                coin_list = []
                obstacle_list = [ob1, ob2, ob4, ob5, ground]

                # coins
                coin3 = Coin(ob5.left + ob5.width / 2 - 30, ob5.top - 25 - 15)
                coin_list.append(coin3)

                coin4 = Coin(ob5.left + ob5.width / 2 + 20 +10-10, ob5.top - 25 - 15)
                coin_list.append(coin4)

                coin5 = Coin(ob5.left + ob5.width / 2 + 20+20+30, ob5.top - 25 - 15)
                coin_list.append(coin5)

            # level 4
            if level == 4 and level_changing == True:
                level_changing = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load(resource_path("assets/x/music4.ogg"))
                pygame.mixer.music.play(-1)  # -1 makes it loop forever
                portal = Portal(650-100-15, 150)
                # setting screen and background sizes less from the secret level
                background = pygame.transform.scale(background, (800, 600))

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                # platforms
                ob1 = pygame.Rect(150, 450, 80, 40)
                ob2 = pygame.Rect(ob1.x + 100 + 75, ob1.y - 50, 70, 40)
                ob3 = pygame.Rect(ob2.x + 90, ob2.y - 50, 60, 40)
                ob4 = pygame.Rect(ob2.x + 90+75, ob2.y - 50, 60, 40)

                # spikes
                spikes.clear()

                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)

                # lists
                coin_list = []
                obstacle_list = [ob1, ob2, ob4, ground]

                # coins
                coin3 = Coin(ob3.left + ob3.width / 2, ob3.top - 25 - 15)
                coin_list.append(coin3)

            # level 5
            if level == 5 and level_changing == True:
                level_changing = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load(resource_path("assets/x/music5.ogg"))
                pygame.mixer.music.play(-1)  # -1 makes it loop forever
                portal = Portal(650 - 100 + 125, 150 - 75 - 20-10)
                # setting screen and background sizes less from the secret level
                background = pygame.transform.scale(background, (800, 600))

                if player.player_reset == True:
                    player.x = 100
                    player.y = 500
                    player.player_reset = False

                # obstacles
                ob1 = pygame.Rect(200 - 80, 425, 200, 50)
                ob2 = pygame.Rect(250 + 25, 225 + 50 + 30, 50, 50)  # filled with grey
                ob3 = pygame.Rect(ob2.x + 40 + 75 - 50, ob2.y - 75 + 35, 200, 50)  # add coin on top
                ob4 = pygame.Rect(ob3.x + 100 + 50, ob3.y - 75, 50, 50)  # filled with grey
                ob5 = pygame.Rect(ob4.x + 75 + 75, ob4.y, 50, 50)  # filled with grey
                ground = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH + 400, 10)

                # lists
                obstacle_list = [ob1, ob2, ob3, ob4, ob5, ground]
                coin_list = []

                # spikes
                spikes.clear()
                spikes.append(Spike(ob3.x + 20 + 30, ob3.y - ob3.height))
                spikes.append(Spike(800 - 175, 100))

                # coins
                coin4 = Coin(ob1.left + ob1.width / 2, ob1.top - 25 - 15)
                coin4.randomize_pos()
                coin_list.append(coin4)

            # level 6
            if level == 6 and level_changing == True:
                level5_cutscene_active = True
                game_state = 'level5_cutscene'
                level_changing = False
                # Reset fade to start fresh
                fade_bg.current_alpha = 0
                fade_bg.is_fading = False

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
            #portal_hitbox.topleft = (portal_x, portal_y)

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

                if rect == ground:
                    # Tile the ground image horizontally
                    tile_width = ground_image.get_width()
                    for x in range(0, rect.width, tile_width):
                        WINDOW.blit(ground_image, (rect.x + x, rect.y))
                    
                    # Add dark overlay on ground
                    ground_overlay = pygame.Surface((rect.width, rect.height))
                    ground_overlay.fill((0, 0, 0))
                    ground_overlay.set_alpha(255)
                    WINDOW.blit(ground_overlay, (rect.x, rect.y))
                else:
                    if level == 3:
                        if rect == ob2:
                            platform_img.fill((128, 128, 128))

                    if level == 4:
                        if rect == ob3:
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
                #portal_hitbox.topleft = (portal_x, portal_y)
                # pygame.draw.rect(WINDOW, (0, 0, 0), ob5)
                platform_img = pygame.transform.scale(platform_img, (ob5.width, ob5.height))
                platform_img.fill((128, 128, 128))
                WINDOW.blit(platform_img, (ob5.x, ob5.y))

            if level == 'secret':
                portal_x = 680 + 250
                portal_y = 100 - 23.5
                #portal_hitbox.topleft = (portal_x, portal_y)
                #pygame.draw.rect(WINDOW, (0, 0, 0), portal_hitbox)

            if level == 3:
                portal_x = WINDOW_WIDTH - 75 - 20 - 150
                portal_y = 150
                #portal_hitbox.topleft = (portal_x, portal_y)
                for spike in spikes:
                    WINDOW.blit(spike.image, (spike.x, spike.y))

                for spike in spikes:
                    spike.update()
                    spike.collisions(player)

            if level == 4:
                portal_x = WINDOW_WIDTH - 75 - 20 - 400 + 200 + 200
                portal_y = 150 - 75
                #portal_hitbox.topleft = (portal_x, portal_y)
                for spike in spikes:
                    WINDOW.blit(spike.image, (spike.x, spike.y))

                for spike in spikes:
                    spike.update()
                    spike.collisions(player)
            if level == 5:
                portal_x = WINDOW_WIDTH - 95
                portal_y = 50
                #portal_hitbox.topleft = (portal_x, portal_y)
                # pulse_surface = pygame.Surface((40, WINDOW_HEIGHT), pygame.SRCALPHA)
                # pulse_surface.fill((100, 100, 225, int(80 + pulse_value * 120)))
                # WINDOW.blit(pulse_surface, (WINDOW_WIDTH - 40, 0))
                for spike in spikes:
                    WINDOW.blit(spike.image, (spike.x, spike.y))

                for spike in spikes:
                    spike.update()
                    spike.collisions(player)

            for coin in coin_list:
                coin.render_coin()

            for torch in torch_list:
                torch.update()
                torch.draw(WINDOW)

            """
            for enemy in enemies:
                enemy.update(player)
                enemy.draw(WINDOW)
            """

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
            global player_dead
            if player.health <= 0 and not player_dead:
                player_dead = True
                death_time = pygame.time.get_ticks()
                game_state = "game_over"

                # vx and vy variables change the speed of the particles
                for i in range(20):
                    particle = {
                        "x": WINDOW_WIDTH // 2,
                        "y": WINDOW_HEIGHT // 2,
                        "vx": random.randint(-4, 4),
                        "vy": random.randint(-4, 4),
                        "life": 180
                    }
                    death_particles.append(particle)

                ''' 
                game_state = 'gameMenu'
                level = 1
                player.health = player.max_health
                player.x = 100
                player.y = 500
                obstacle_list = []
                portal_x = 380
                portal_y = 200
                portal_hitbox.topleft = (portal_x, portal_y)
                '''

            # WINDOW.fill(PLAYER_COLOR, player)
            # WINDOW.blit(player.player_now, (player.x, player.y))
            #WINDOW.blit(portal, (portal_x, portal_y))
            portal.animate()
            portal.draw(WINDOW)
            #WINDOW.blit(middle_background, (-player.x * 0.1, 0))
            WINDOW.blit(level_counter1.text(), (170-20-15, 100))
            WINDOW.blit(coin_counter.text(), (300, 100))
            # Screen flash effect when taking damage
            if pygame.time.get_ticks() - damage_flash_time < damage_flash_duration:
                flash_intensity = 255 * (1 - (pygame.time.get_ticks() - damage_flash_time) / damage_flash_duration)
                flash_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                flash_surface.fill((255, 100, 100))  # Light red color
                flash_surface.set_alpha(int(flash_intensity / 3))  # Make it semi-transparent
                WINDOW.blit(flash_surface, (0, 0))


        elif game_state == "game_over":
            global pulse, pulse_direction
            # pulse
            pulse += pulse_direction

            if pulse > 120:
                pulse_direction = -1
            if pulse < 40:
                pulse_direction = 1

            WINDOW.fill((pulse, 0, 0))

            # death particles
            for particle in death_particles:
                particle["x"] += particle["vx"]
                particle["y"] += particle["vy"]
                particle["life"] -= 1

                pygame.draw.circle(WINDOW, (200, 0, 0), (int(particle["x"]), int(particle["y"])), 4)

            death_particles[:] = [p for p in death_particles if p["life"] > 0]

            fallen_player = pygame.transform.rotate(knight, 90)
            fallen_player.set_alpha(150)
            WINDOW.blit(fallen_player, (WINDOW_WIDTH//2 - 50, 350))

            font = pygame.font.Font(None, 50)
            text = font.render("The dungeon claims another soul...", True, (200, 200, 200))
            text2 = font.render("Your journey ends here.", True, (200, 200, 200))
            text3 = font.render("Hold control shift r to restart.", True, (200, 200, 200))

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - death_time

            if elapsed_time > 1000:
                WINDOW.blit(text, (180 - 100, 250 - 150))

            if elapsed_time > 3000:
                WINDOW.blit(text2, (230 - 100, 320 - 150))

            if elapsed_time > 5000:
                WINDOW.blit(text3, (260 - 100, 400 - 150))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.quit()
                        # subprocess.call([sys.executable, __file__])  # Not supported in web
                        sys.exit()

                        '''
                        player_dead = False
                        level = 1
                        player.health = player.max_health
                        player.x = 100
                        player.y = 500
                        game_state = "gameMenu"
                        '''

        pygame.display.update()
        fpsClock.tick(FPS)

main()
