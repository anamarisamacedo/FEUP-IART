import pygame

class Bubble(pygame.sprite.Sprite):
    def __init__(self, pos, level):
        # sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/bubble' + str(level) + '.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        self.rect.center = pos
        self.level = level

    # returns projectiles if bubble dies
    def hit(self):
        if self.level > 1:
            self.level -= 1
            self.image = pygame.image.load('assets/bubble' + str(self.level) + '.png')
            self.image = pygame.transform.scale(self.image, (50, 50))
            return None
        else:
            self.kill()
            newExplosion = Explosion(self.rect.center)
            return [newExplosion.projectiles]


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        projectileUp = Projectile(pos, "up")
        projectileDown = Projectile(pos, "down")
        projectileLeft = Projectile(pos, "left")
        projectileRight = Projectile(pos, "right")
        self.projectiles = [projectileUp, projectileDown, projectileLeft, projectileRight]


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        # sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.x = pos[0]
        self.y = pos[1]
        self.rect.center = (self.x, self.y)
        self.direction = direction

    def update(self):
        if self.direction == "up":
            self.y += 0.5

        elif self.direction == "down":
            self.y -= 0.5

        elif self.direction == "left":
            self.x -= 0.5

        else:
            self.x += 0.5

        self.rect.center = (self.x, self.y)

