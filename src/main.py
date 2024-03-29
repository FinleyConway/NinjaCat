import pygame
import GameObjects

import random

def main():
    pygame.init()
    pygame.font.init()

    # init window
    windowTitle: str = "Game"
    windowSize: pygame.Coordinate = [1000, 1000]

    pygame.display.set_caption(windowTitle)
    windowSurface = pygame.display.set_mode(windowSize)

    # main loop
    game_loop(windowSurface)

    pygame.quit()

def game_loop(windowSurface: pygame.Surface):
    isRunning: bool = True

    clock = pygame.time.Clock()
    targetFPS: int = 60

    textFont = pygame.font.SysFont('Arial', 30)
    aliveCounter = 0

    gameObjects = pygame.sprite.Group()

    gameObjects.add(GameObjects.Sprite("Assets/Background.png", "Background"))

    player = GameObjects.NinjaCat("Assets/Cat.png", [500, 500], gameObjects)

    gameObjects.add(player)
    for i in range(5):
        randomAttack = random.randint(0, 1) 
        gameObjects.add(GameObjects.Dog("Assets/Dog.png", player, randomAttack))

    # left
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [0, 280]))
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [0, 520]))
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [0, 760]))

    # middle
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [250, 280]))
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [250, 520]))
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [250, 760]))

    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [500, 280]))
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [500, 520]))
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [500, 760]))


    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [750, 280]))
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [750, 520]))
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [750, 760]))

    # right
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [935, 280]))
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [935, 520]))
    gameObjects.add(GameObjects.Platform("Assets/Platform.png", player, [935, 760]))

    dogTimer = 10
    timer = 0

    # game loop
    while (isRunning):
        deltaTime = clock.tick(targetFPS) / 1000

        if (player.hasMoved):
            aliveCounter += deltaTime

            timer += deltaTime
            if (timer >= dogTimer):
                randomAttack = random.randint(0, 1)
                gameObjects.add(GameObjects.Dog("Assets/Dog.png", player, randomAttack))
                timer = 0

        # query poll events
        for  event in pygame.event.get():
            if (event.type == pygame.QUIT):
                isRunning = False

        # update game objects
        update(deltaTime, gameObjects)

        # render game objects
        render(windowSurface, gameObjects, textFont, aliveCounter)

def update(deltaTime: float, gameObjects):
    gameObjects.update(deltaTime)

def render(surface: pygame.Surface, gameObjects, textFont, aliveCounter):
    # clear screen
    surface.fill(pygame.Color(0, 0, 0, 255))

    # draw screen
    gameObjects.draw(surface)

    textSurface = textFont.render(f"Score: {int(aliveCounter)}", False, (0, 0, 0))
    surface.blit(textSurface, (10, 10))

    # clear screen
    pygame.display.flip()

if (__name__ == "__main__"):
    main()
