# Example file showing a basic pygame "game loop"
import pygame
from random import randint, randrange

score = 0

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
pygame.font.init() # you have to call this at the start, 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

    # Define objects
class Object:
    def __init__(self, image, x, y, width, height):

        self.x = x
        self.y = y
        self.image = image
        self.alive = True
        self.width = width
        self.height = height
        self.conta = 0

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

cursor = sprite(100, 100)
cursor.load("cursor.png")

scene = []

def spawnDuckie():
    temp = Object(duck.image, 0, 0, duck.width, duck.height)

    temp.y = screen.get_height() / randint(1, 10)
    #temp.y = randint(1, 500)

    scene.append(temp)

for i in range(0, 5):
    spawnDuckie()
    print(scene)

def events():
    if pygame.mouse.get_pressed()[0] == True:
        checkMouse()

def checkMouse():
    mousePos = pygame.mouse.get_pos()
    global score
    #print(mousePos)
    for i in scene:
        if i.alive:
            if mousePos[0] > i.x and mousePos[0] < i.x + i.width:
                if mousePos[1] > i.y and mousePos[1] < i.y + i.height:
                    i.alive = False
                    score += 1
conta = 0

# Render function
def render(count):
    events()
    text = my_font.render("score: " + str(score), False, (0, 0, 0))
    for i in scene:
        if i.conta < 50:
            i.x += 2
            i.y += 1
        else:
            i.x += 2
            i.y -= 1
        if i.conta == 100:
            print(i.conta)
            i.conta = 0
        i.conta += 1

    
    screen.fill((0, 150, 255))
    for i in scene:
        if i.alive == True:
            screen.blit(i.image,  (i.x, i.y))
    # flip() the display to put your work on screen
    screen.blit(text, (3, 3))
    temp = (pygame.mouse.get_pos()[0] - cursor.width/2, pygame.mouse.get_pos()[1] - cursor.height/2)
    screen.blit(cursor.image, temp)
    pygame.display.flip()

    conta 

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
    render(conta)



    clock.tick(60)  # limits FPS to 60

pygame.quit()