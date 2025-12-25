class Coin():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15 
        self.collected = False
        self.hitbox = pygame.Rect(0, 0, 15, 15)

    def get_hitbox(self):
        return self.hitbox.move(self.x, self.y)

    def render_coin(self, COIN):
        WINDOW.blit(COIN, (self.x, self.y)) 

    def collide(self, playerHitbox):
        if self.get_hitbox().colliderect(playerHitbox) and self.collected == False:
            self.collected = True

    def randomize_pos(self):
        self.x = self.x + random.randint(-30, 30)
