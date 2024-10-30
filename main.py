# Example file showing a basic pygame "game loop"
import pygame
from random import randint, randrange

score = 0
patosm = 0

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1542, 1032))
clock = pygame.time.Clock()
running = True
pygame.font.init() # you have to call this at the start, 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Define objects
class Object:
    def __init__(self, image, x, y, width, height, frameTime):

        self.x = x
        self.y = y
        self.image = image
        self.alive = True
        self.width = width
        self.height = height
        self.conta = 0
        self.curFrame = 0
        self.vel = 0
        self.frameTime = frameTime

    def draw(self, background):
        background.blit(self.image[self.curFrame], (self.x, self.y))


class sprite:
    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.image = []
    
    def load(self, path):
        for i in path:
            self.temp = pygame.image.load(i)
            self.temp = pygame.transform.scale(self.temp, (self.width, self.height))
            self.image.append(self.temp)

duck = sprite(100, 100)
duck.load(["duck1.png", "duck2.png", "duck3.png"])

cursor = sprite(100, 100)
cursor.load(["cursor.png"])

dog = sprite(100, 100)
dog.load(["dog1.png"])

background = sprite(screen.get_width(), screen.get_width() * 0.6692)
background.load(["background.png"])

scene = []

def spawnDuckie():
    val = False

    while val == False:
        val = True
        temp = Object(duck.image, 0, 0, duck.width, duck.height, 10)

        temp.y = screen.get_height() / randint(1, 20)

        for i in scene:
            if abs(temp.y - i.y) < duck.height:
                val = False
        
    #temp.y = randint(1, 500)
    print(temp.y)
    scene.append(temp)

for i in range(0, 5):
    spawnDuckie()

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
                    patosm = patosm + 1
conta = 0

# Render function
def render(count):
    events()
    text = my_font.render("score: " + str(score), False, (0, 0, 0))
    for i in scene:
        if i.conta < 50:
            if patosm > 0:
                i.x += randint(50, 80)
                i.y += randint (20, 40)
            i.x += 2
            i.y += 1
        else:
            if patosm > 0:
                i.x += randint(50, 80)
                i.y += randint (20, 40)
            i.x += 2
            i.y -= 1
        if i.conta == 100:
            print(i.conta)
            i.conta = 0
        i.conta += 1
    

    
    screen.fill((0, 150, 255))
    screen.blit(background.image[0], (0, 0))
    for i in scene:
        if i.alive == True:
            screen.blit(i.image[i.curFrame//i.frameTime],  (i.x, i.y))
            #screen.blit(i.image,  (i.x, i.y))
            i.curFrame += 1
            if i.curFrame // i.frameTime >= len(i.image):
                i.curFrame = 0

    # flip() the display to put your work on screen
    screen.blit(text, (3, 3))
    temp = (pygame.mouse.get_pos()[0] - cursor.width/2, pygame.mouse.get_pos()[1] - cursor.height/2)
    screen.blit(cursor.image[0], temp)
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