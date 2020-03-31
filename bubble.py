import pygame

velocity = 1
maxLevel = 4
rowNr = 6
colNr = 5
scoreVerticalSpace = 80

class Bubble(pygame.sprite.Sprite):
    def __init__(self, pos, level):
        self.level = level
        self.score = 10
        self.pos = pos
        if level > maxLevel: self.level = maxLevel

        # sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/bubble' + str(self.level) + '.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        self.rect.center = (pos[0]*100 + 50, 100*pos[1] + scoreVerticalSpace)

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
            self.y += velocity

        elif self.direction == "down":
            self.y -= velocity

        elif self.direction == "left":
            self.x -= velocity

        elif self.direction == "right":
            self.x += velocity

        self.rect.center = (self.x, self.y)


