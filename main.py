import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOUR = (104, 166, 67)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.apple_x = random.randint(1, 23) * SIZE
        self.apple_y = random.randint(1, 15) * SIZE

    def make_apple(self):
        self.parent_screen.blit(self.apple, (self.apple_x, self.apple_y))
        pygame.display.flip()

    def new_cords(self):
        self.apple_x = random.randint(1, 23) * SIZE
        self.apple_y = random.randint(1, 15) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.Apple = Apple(self.parent_screen)
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [150] * length
        self.y = [150] * length
        self._direction = 'R'
        self.length = length

    def set_dir(self, dir):
        self._direction = dir

    def make_snake(self, x, y):
        self.parent_screen.blit(self.block, (x, y))
        pygame.display.flip()

    def draw_snake(self):
        #self.parent_screen.fill(BACKGROUND_COLOUR)
        # self.Apple.make_apple()
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def walk_snake(self, ):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self._direction == 'L':
            self.x[0] -= 40

        elif self._direction == 'R':
            self.x[0] += 40

        elif self._direction == 'U':
            self.y[0] -= 40

        elif self._direction == 'D':
            self.y[0] += 40

        self.draw_snake()

    def increase_length(self):
        self.length += 1
        self.x.append(1200)
        self.y.append(1200)
        self.draw_snake()


class Game:
    score = 0

    def __init__(self):
        pygame.init()
        self.play_background_music()
        self.screen = pygame.display.set_mode((1000, 700))
        #self.screen.fill(BACKGROUND_COLOUR)
        self.Snake = Snake(self.screen, 1)
        self.snake_speed = 1
        self.Snake.draw_snake()
        self.Apple = Apple(self.screen)
        self.Apple.make_apple()
        self.counter = 0
        self.running = True

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score, (800, 10))
        pygame.display.flip()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    def render_background(self):
        bg = pygame.image.load('resources/background.jpg')
        self.screen.blit(bg,(0,0))

    def play_sound(self,url):
        sound = pygame.mixer.Sound(url)
        pygame.mixer.Sound.play(sound)

    def collision(self):
        appx = self.Apple.apple_x
        appy = self.Apple.apple_y

        # Snake Collision with Apple
        if ((self.Snake.x[0] < appx + 40) and (self.Snake.x[0] > appx - 40)) and \
                ((self.Snake.y[0] > appy - 40) and (self.Snake.y[0] < appy + 40)):
            self.Apple.new_cords()
            self.Snake.increase_length()
            pygame.display.flip()
            self.score += 1
            self.play_sound('resources/ding.mp3')

        # Snake collision with itself
        for i in range(3, self.Snake.length):
            if ((self.Snake.x[0] < self.Snake.x[i] + 40) and (self.Snake.x[0] > self.Snake.x[i] - 40)) and \
                    ((self.Snake.y[0] > self.Snake.y[i] - 40) and (self.Snake.y[0] < self.Snake.y[i] + 40)):
                self.play_sound('resources/crash.mp3')
                raise "Game_Over"

    def play(self):
        self.render_background()
        self.Snake.walk_snake()
        self.Apple.make_apple()
        self.display_score()
        self.collision()

    def reset(self):
        self.Snake = Snake(self.screen, 1)
        self.Apple = Apple(self.screen)
        self.score = 0

    def show_game_over(self):
        self.render_background()
        self.screen.fill(BACKGROUND_COLOUR)
        font1 = pygame.font.SysFont('arail', 50)
        font2 = pygame.font.SysFont('arail', 40)
        line1 = font1.render(f"Game Over", True, (255, 255, 255))
        self.screen.blit(line1, (400, 250))
        line2 = font2.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(line2, (450, 300))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def run(self):
        pause = False
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

                    if not pause:
                        if event.key == K_DOWN:
                            self.Snake.set_dir('D')

                        if event.key == K_LEFT:
                            self.Snake.set_dir('L')

                        if event.key == K_RIGHT:
                            self.Snake.set_dir('R')

                        if event.key == K_UP:
                            self.Snake.set_dir('U')

                    if event.key == K_RETURN and pause == True:
                        pygame.mixer.music.unpause()
                        pause = False
                        self.reset()

                elif event.type == QUIT:
                    self.running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
            time.sleep(0.1)
            # self.counter += 1


if __name__ == "__main__":
    game = Game()
    game.run()
