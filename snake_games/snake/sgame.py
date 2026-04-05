import pygame
from pygame.locals import *
from random import randint
import os

class Apple:
    step = 44

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, self.step, self.step), 0)


class Player:
    step = 44
    direction = 0
    length = 3

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
        self.length = length
        # интерполяция
        self.x = [i * self.step for i in range(length)] + [-100.0] * 2000
        self.y = [0.0] * (length + 2000)
        # интерполяция
        self.target_x = self.x.copy()
        self.target_y = self.y.copy()
        self.speed = 8.0  

    def update(self):
        self.updateCount += 1
        if self.updateCount > self.updateCountMax:
            for i in range(self.length - 1, 0, -1):
                self.target_x[i] = self.target_x[i - 1]
                self.target_y[i] = self.target_y[i - 1]

            if self.direction == 0:
                self.target_x[0] += self.step
            elif self.direction == 1:
                self.target_x[0] -= self.step
            elif self.direction == 2:
                self.target_y[0] -= self.step
            elif self.direction == 3:
                self.target_y[0] += self.step

            self.updateCount = 0

        # интерполяция
        for i in range(self.length):
            dx = self.target_x[i] - self.x[i]
            dy = self.target_y[i] - self.y[i]
            self.x[i] += dx / self.speed
            self.y[i] += dy / self.speed

    def moveRight(self):
        if self.direction != 1:
            self.direction = 0

    def moveLeft(self):
        if self.direction != 0:
            self.direction = 1

    def moveUp(self):
        if self.direction != 3:
            self.direction = 2

    def moveDown(self):
        if self.direction != 2:
            self.direction = 3

    def draw(self, surface):
        for i in range(self.length):
            pygame.draw.rect(surface, (255, 0, 0),
                             (int(self.x[i]), int(self.y[i]), self.step, self.step), 0)


class Game:
    def isCollision(self, x1, y1, x2, y2, size):
        return x1 < x2 + size and x1 + size > x2 and y1 < y2 + size and y1 + size > y2


class SnakeApp:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.game = Game()
        self.player = Player(3)
        self.apple = Apple(5, 5)

    def on_init(self):
        pygame.init()
        os.putenv("SDL_FBDEV", "/dev/fb0")
        pygame.display.init()
        pygame.mouse.set_visible(False)
        self.DIMS = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self._display_surf = pygame.display.set_mode(self.DIMS, pygame.FULLSCREEN)
        self._running = True
        self._display_surf.fill((0, 0, 0))
        pygame.display.flip()
        self.clock = pygame.time.Clock()  # FPS

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()

        # Snake eats apple
        for i in range(self.player.length):
            if self.game.isCollision(
                self.apple.x, self.apple.y, self.player.x[i], self.player.y[i], self.player.step
            ):
                cols = self.DIMS[0] // self.apple.step - 2
                rows = self.DIMS[1] // self.apple.step - 2
                self.apple.x = randint(2, cols) * self.apple.step
                self.apple.y = randint(2, rows) * self.apple.step
                self.player.length += 1
                # интерполяция
                self.player.x[self.player.length - 1] = self.player.target_x[self.player.length - 2]
                self.player.y[self.player.length - 1] = self.player.target_y[self.player.length - 2]
                self.player.target_x[self.player.length - 1] = self.player.x[self.player.length - 1]
                self.player.target_y[self.player.length - 1] = self.player.y[self.player.length - 1]

        # снек коллайз
        for i in range(2, self.player.length):
            if self.game.isCollision(
                self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], self.player.step
            ):
                print("You lose! Collision")
                self._running = False

        if (
            self.player.x[0] < 0
            or self.player.y[0] < 0
            or self.player.x[0] >= self.DIMS[0]
            or self.player.y[0] >= self.DIMS[1]
        ):
            print("You lose! Out of bounds")
            self._running = False

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.player.draw(self._display_surf)
        self.apple.draw(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        exit(0)

    def on_execute(self):
        self.on_init()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            keys = pygame.key.get_pressed()
            if keys[K_RIGHT]:
                self.player.moveRight()
            if keys[K_LEFT]:
                self.player.moveLeft()
            if keys[K_UP]:
                self.player.moveUp()
            if keys[K_DOWN]:
                self.player.moveDown()
            if keys[K_ESCAPE]:
                self._running = False

            self.on_loop()
            self.on_render()
            self.clock.tick(60)
        self.on_cleanup()


if __name__ == "__main__":
    app = SnakeApp()
    app.on_execute()