Spike Class
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
            player.health -= 1
            player.x = 100
            player.y = 500
            player.hitbox.topleft = (player.x, player.y)
