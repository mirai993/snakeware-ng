import pygame, random, os


def roundline(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    if distance == 0:
        return
    for i in range(distance):
        x = int(start[0] + dx * i / distance)
        y = int(start[1] + dy * i / distance)
        pygame.draw.circle(srf, color, (x, y), radius)


class SnakePaint:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.draw_on = False
        self.last_pos = (0, 0)
        self.color = (255, 128, 0)
        self.radius = 10
        self.eraser = False

    def on_init(self):
        pygame.init()
        os.putenv("SDL_FBDEV", "/dev/fb0")
        pygame.display.init()
        self.DIMS = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self._display_surf = pygame.display.set_mode(self.DIMS, pygame.FULLSCREEN)
        self._display_surf.fill((0, 0, 0))
        self._running = True

    def on_execute(self):
        self.on_init()
        self.start()

    def start(self):
        while self._running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self._running = False

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self._running = False

                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_d:
                        self.eraser = not self.eraser

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.draw_on = True
                    self.color = (0, 0, 0) if self.eraser else (
                        random.randrange(256),
                        random.randrange(256),
                        random.randrange(256),
                    )
                    self.last_pos = e.pos
                    pygame.draw.circle(self._display_surf, self.color, e.pos, self.radius)

                elif e.type == pygame.MOUSEBUTTONUP:
                    self.draw_on = False

                elif e.type == pygame.MOUSEMOTION and self.draw_on:
                    roundline(self._display_surf, self.color, self.last_pos, e.pos, self.radius)
                    self.last_pos = e.pos

            pygame.display.flip()