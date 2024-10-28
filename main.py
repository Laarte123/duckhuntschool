# Example file showing a basic pygame "game loop"
import pygame
#from livewires import games, color
#import pygame.display, pygame.mouse
from random import randint, randrange

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Define objects
class Object:
    def __init__(self, image, x, y):

        self.x = x
        self.y = y
        self.image = image

    def draw(self, background):
        background.blit(self.image, (self.x, self.y))

class sprite:
    def __init__(self, width, height):

        self.width = width
        self.height = height
    
    def load(self, path):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

duck = sprite(100, 100)
duck.load("duck.png")

scene = []

def spawnDuckie():
    temp = Object(duck.image, 0, 0)

    # temp.y = screen.get_height() / randint(1, 10)
    temp.y = randint(1, 500)

    scene.append(temp)

for i in range(0, 3):
    spawnDuckie()
    print(scene)

# Render function
def render():
    screen.fill((0, 150, 255))
    for i in scene:
        screen.blit(i.image,  (i.x, i.y))
    # flip() the display to put your work on screen
    pygame.display.flip()

# Ralsei é o melhor (não, patos são, QUACKIESSSS :3)
#imagina ter comentarios >:(
def enemy():
    enemy_list = []

    for e in range(0, 200):
        x_cor = random.randint(25, 361)
        e = Object("enemy.png", 70, 70, x_cor, 25)
        enemy_list.append(e)

        return enemy_list


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    render()



    clock.tick(60)  # limits FPS to 60

pygame.quit()