import pygame
from Sprite import Sprite

import random
import sys
import math

class NinjaCat(Sprite):
    def __init__(self, spritePath, position, gameObjects: pygame.sprite.Group):
        super().__init__(spritePath, "NinjaCat")

        self.target = gameObjects

        self.speed = 600
        self.jumpVel = -50
        self.gravity = 300

        self.leftWall = 0
        self.rightWall = 970
        self.floorY = 940

        self.velocity = [0, 0]
        self.jumping = False

        self.rect.x = position[0]
        self.rect.y = position[1]

        self.canThrow = True
        self.newStarTimer = 1
        self.timer = 0

        self.hasMoved = False

    def update(self, deltaTime):
        keys = pygame.key.get_pressed()

        self.velocity[0] = 0

        # move left and right
        if (keys[pygame.K_a]):
            self.velocity[0] -= self.speed * deltaTime
            self.flip(horizontal=True)
            self.hasMoved = True

        if (keys[pygame.K_d]):
            self.velocity[0] += self.speed * deltaTime
            self.flip(horizontal=False)
            self.hasMoved = True

        # jump
        if (keys[pygame.K_SPACE] and not self.jumping):
            self.velocity[1] = self.jumpVel
            self.jumping = True
            self.hasMoved = True

        # gravity
        self.velocity[1] += self.gravity * deltaTime

        # set current velocity to sprite position
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # floor collision
        if (self.rect.y >= self.floorY):
            self.rect.y = self.floorY
            self.velocity[1] = 0
            self.jumping = False

        # wall collision
        if (self.rect.x <= self.leftWall):
            self.rect.x = self.leftWall
        if (self.rect.x >= self.rightWall):
            self.rect.x = self.rightWall

        self.timer += deltaTime
        if (self.timer >= self.newStarTimer):
            self.canThrow = True
            self.timer = 0

        self.throw_ninja_star()

    def throw_ninja_star(self):
        mouseButtons = pygame.mouse.get_pressed()
        if (mouseButtons[0] and self.canThrow):

            mousePosition = pygame.mouse.get_pos()
            direction = (mousePosition[0] - self.rect.centerx, mousePosition[1] - self.rect.centery)
            length = math.sqrt(pow(direction[0], 2) + pow(direction[1], 2))

            # avoid division by zero
            if (length != 0):
                direction = (direction[0] / length, direction[1] / length)

            # create a instance
            ninja_star = NinjaStar("Assets/ThrowingStar.png", self.target)
            ninja_star.rect.centerx = self.rect.centerx
            ninja_star.rect.centery = self.rect.centery
            ninja_star.direction = direction

            # add star to objects
            self.target.add(ninja_star)

            self.canThrow = False
            self.hasMoved = True

    def die(self):
        sys.exit()

class Dog(Sprite):
    def __init__(self, spritePath: str, player: NinjaCat, followType: int):
        super().__init__(spritePath, "Dog")

        self.player = player
        self.speed = random.randint(200, 400)
        self.startingRadius = 750
        self.followRadius = 50
        self.followType = followType

        if self.followType == 0:
            self.targetPoint = [player.rect.centerx, player.rect.centery]
        else:
            self.update_target_point()

        self.set_random_position()

    def update(self, deltaTime):
        if (not self.player.hasMoved): return

        if (self.followType == 0):
            self.follow_player(deltaTime)
        else:
            self.follow_random_point(deltaTime)

        # check for collision with the player
        if (self.rect.colliderect(self.player.rect)):
            self.player.die()

    def follow_player(self, deltaTime):
        # get direction to player
        directionVector = [self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery]
        magnitude = math.sqrt(pow(directionVector[0], 2) + pow(directionVector[1], 2))

        # normalise direction
        if (magnitude != 0):
            directionVector = [directionVector[0] / magnitude, directionVector[1] / magnitude]

        self.rect.x += int(directionVector[0] * self.speed * deltaTime)
        self.rect.y += int(directionVector[1] * self.speed * deltaTime)

    def follow_random_point(self, deltaTime):
        # get direction to player
        directionVector = [self.targetPoint[0] - self.rect.centerx, self.targetPoint[1] - self.rect.centery]
        magnitude = math.sqrt(pow(directionVector[0], 2) + pow(directionVector[1], 2))

        # normalise direction
        if (magnitude != 0):
            directionVector = [directionVector[0] / magnitude, directionVector[1] / magnitude]

        self.rect.x += int(directionVector[0] * self.speed * deltaTime)
        self.rect.y += int(directionVector[1] * self.speed * deltaTime)

        # check if the dog reached the target point
        if (abs(self.rect.centerx - self.targetPoint[0]) < 5 and abs(self.rect.centery - self.targetPoint[1]) < 5):
            self.update_target_point()

    def update_target_point(self):
        # create a random point around the player
        angle = random.uniform(0, 2 * math.pi)
        self.targetPoint = [
            self.player.rect.centerx + self.followRadius * math.cos(angle),
            self.player.rect.centery + self.followRadius * math.sin(angle)
        ]

    def set_random_position(self):
        # create a random point around the player
        angle = random.uniform(0, 2 * math.pi)
        random_position = [
            self.player.rect.centerx + self.startingRadius * math.cos(angle),
            self.player.rect.centery + self.startingRadius * math.sin(angle)
        ]

        self.rect.center = random_position

    def die(self):
        # reset dog
        randomAttack = random.randint(0, 1)
        self.followType = randomAttack
        self.set_random_position()


class Platform(Sprite):
    def __init__(self, spritePath, player: NinjaCat, position):
        super().__init__(spritePath, "Platform")

        self.player = player

        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self, deltaTime):
        padding = 5

        if (self.rect.colliderect(self.player.rect)):
            # if landed on the top platform
            # allows the player to go through the collider to land on top
            if (self.player.velocity[1] > 0):
                if (self.player.rect.y <= self.rect.y + padding):

                    # allow player to drop down
                    keys = pygame.key.get_pressed()
                    if (keys[pygame.K_s]):
                        self.player.jumping = True
                        self.player.rect[1] += self.player.gravity * deltaTime
                        self.player.hasMoved = True
                    # sit on top of platform
                    else:
                        self.player.rect.bottom = self.rect.top
                        self.player.velocity[1] = 0
                        self.player.jumping = False

class NinjaStar(Sprite):
    def __init__(self, spritePath, gameObjects):
        super().__init__(spritePath, "NinjaStar")

        self.target: pygame.sprite.Group = gameObjects

        self.direction = [0, 0]
        self.throwingSpeed = 300

        self.aliveTime = 0
        self.maxAliveTime = 10

    def update(self, deltaTime):
        self.rect.x += self.direction[0] * self.throwingSpeed * deltaTime
        self.rect.y += self.direction[1] * self.throwingSpeed * deltaTime

        # check if it collides with dog
        dogHitList = pygame.sprite.spritecollide(self, self.target, False)
        for dog in dogHitList:
            if (dog.spriteType == "Dog"):
                # kill dog and remove self
                dog.die()
                self.target.remove(self)

        # remove self if living too long
        self.aliveTime += deltaTime
        if (self.aliveTime >= self.maxAliveTime):
            self.target.remove(self)

