# Example file showing a basic pygame "game loop"
import pygame
import time 
from random import randint, randrange

# Adicionei algumas coisas em casa ontem, para adiantar algum trabalho (precebi mas agr n sei tf ta a acontecer aqui ;-;)


# TODO:
# Reiniciar o jogo cada ronda(quando todos os patos sairem do ecra) ((Racismo tbh))
# Dificuldade

score = 0
patosm = 0
b = 0

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1542, 1032))
clock = pygame.time.Clock()
running = True
pygame.font.init() # you have to call this at the start, 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Definir o jogo como uma classe
class Round:
    def __init__(self):
        self.maxFrame = 10
        self.scene = []
        self.state = 0
        self.patosm = 0
        self.curFrame = 0
    
    def roundStart(self, dif, ducknum):
        self.maxFrame = 6000
        self.state = 1
        self.dif = dif
        self.scene = []
        self.ducks = ducknum
        
        for i in range(0, self.ducks):
            spawnDuckie(self.scene)
    
    def roundEnd(self):
        global score
        self.maxFrame = 6000
        val = True
        for i in self.scene:
            if i.state == 0:
                val = False
        
        if val == True:
            if score > 0:
                screen.blit(dog.image[0][0], (90, 660))
            self.state = 2
        

# Define objects
class Object:
    def __init__(self, image, x, y, width, height, frameTime, id):
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
        self.id = id
        # Agora cada objeto tem estados, só é usado nos patos (W patos skill issue dos outros)
        self.state = 0

    def draw(self, background):
        # Isto foi necessario para fazer funcionar, NAO TIRAR (vou tirar)
        try:
            screen.blit(self.image[self.state][self.curFrame//self.frameTime],  (self.x, self.y))
        except:
            print(self.curFrame // self.frameTime)
            print(len(self.image[self.state]))

            # Mudar o frame da animação
        self.curFrame += 1
        if self.curFrame // self.frameTime >= len(self.image[self.state]):
            self.curFrame = 0

    def changeState(self, state):
        self.state = state


def countdown(t): 
    t = 1
    while t: 
        mins, secs = divmod(1, 2) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        t -= 1
      
    spawnDuckie()
    

class sprite:
    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.image = []
    
    def load(self, path):
        tempList = []
        for i in path:
            temp = pygame.image.load(i)
            temp = pygame.transform.scale(temp, (self.width, self.height))
            tempList.append(temp)

        self.image.append(tempList)

r1 = Round()

duck1 = sprite(100, 100)
duck1.load(["d11.png", "d12.png", "d13.png"])
duck1.load(["d1Hit.png"])
duck1.load(["d1Hit.png"])

duck2 = sprite(100, 100)
duck2.load(["d21.png", "d22.png", "d23.png"])
duck2.load(["d2Hit.png"])
duck2.load(["d2Hit.png"])

#duck3 = sprite(100, 100)
#duck3.load(["d31.png", "d32.png", "d33.png"])
#duck3.load(["d3Hit.png"])

cursor = sprite(100, 100)
cursor.load(["cursor.png"])

dog = sprite(100, 100)
dog.load(["dog1.png"])

background = sprite(screen.get_width(), screen.get_width() * 0.6692)
background.load(["background.png"])

def spawnDuckie(scene):
    val = False

    count = 0
    
    special = randint(1, 15)
    
    if special == 15:
        temp = Object(duck2.image, 0, 0, duck2.width, duck2.height, 10, 2)
    elif special == 14:
        temp = Object(duck2.image, 0, 0, duck2.width, duck2.height, 10, 2)
    elif special == 13:
        temp = Object(duck2.image, 0, 0, duck2.width, duck2.height, 10, 2)
    else:
        temp = Object(duck1.image, 0, 0, duck1.width, duck1.height, 10, 1)
    

    while val == False:
        count += 1
        val = True
        
        temp.y = screen.get_height() / randint(1, 20)

        for i in scene:
            if abs(temp.y - i.y) < i.height:
                val = False
            if temp.y + temp.height > 1032:
                val = False

        if count >= 50:
             val = True
        
    #temp.y = randint(1, 500)
    print(temp.y)
    scene.append(temp)

#for i in range(0, 1):
    #spawnDuckie(scene)

def events():
    if pygame.mouse.get_pressed()[0] == True:
        checkMouse()

def checkMouse():
    mousePos = pygame.mouse.get_pos()
    global score
    global patosm
    global b
    global r1
    #print(mousePos)
    for i in r1.scene:
        if i.id >= 1 and i.id <= 3:
            # Verificar se o pato está vivo
            if i.state == 0:
                # Verificar se o cursor está em cima do pato
                if mousePos[0] > i.x and mousePos[0] < i.x + i.width:
                    if mousePos[1] > i.y and mousePos[1] < i.y + i.height:
                        # Matar o pato
                        i.changeState(1)
                        # i.alive = False
                        if i.id == 2:
                            score += 2
                        else:
                            score += 1
                        #spawnDuckie()
                        b = b +1
                        #if b %2 == 0:
                            #countdown(0)
                        patosm = patosm + 1
conta = 0

res = 0

# Função para as fisicas
def physicz():
    global r1
    global patosm
    global res

    for i in r1.scene:                
        if i.state == 0:
            if i.id == 2:
                if i.conta < 50:
                    if patosm > 0:
                        if i.id == 2:
                            i.x += randint(10,11)
                        i.x += randint(3, 4)
                        a = randint(1,2)
                        if a == 1:
                            i.y -= randint (2, 3)
                        if a == 2:
                            i.y += randint (2, 3)
                        patosm = patosm +1
                    if patosm == 40:
                        patosm = 0
                    i.x += 2
                    i.y += 1
                else:
                    if patosm > 0:
                        i.x += randint(3, 4)
                        a = randint(1,2)
                        if a == 1:
                            i.y -= randint (2, 3)
                        if a == 2:
                            i.y += randint (2, 3)
                        patosm = patosm +1
                    if patosm == 40:
                        patosm = 0
                    i.x += 2
                    i.y -= 1
                if i.conta < 50:
                    if patosm > 0:
                        if i.id == 2:
                            i.x += randint(10,11)
                        i.x += randint(3, 4)
                        a = randint(1,2)
                        if a == 1:
                            i.y -= randint (2, 3)
                        if a == 2:
                            i.y += randint (2, 3)
                        patosm = patosm +1
                    if patosm == 40:
                        patosm = 0
                    i.x += 2
                i.y += 1
            else:
                if patosm > 0:
                    if i.id == 2:
                        i.x += randint(10, 11)
                    i.x += randint(3, 4)
                    a = randint(1,2)
                    if a == 1:
                        i.y -= randint (2, 3)
                    if a == 2:
                        i.y += randint (2, 3)
                    patosm = patosm +1
                if patosm == 40:
                    patosm = 0
                i.x += 2
                i.y -= 1
            if i.conta == 100:
                #print(i.conta)
                i.conta = 0
            i.conta += 1
        else:
            i.y += 6
        
        if i.x >= res.current_w:
            i.changeState(2)


# Render function
def render(count):
    screen.fill((0, 150, 255))

    global res
    global patosm
    global r1

    r1.roundEnd()
    
    res = pygame.display.Info()

    physicz()
    
    events()
    text = my_font.render("score: " + str(score), False, (0, 0, 0))
    
    for i in r1.scene:
        if i.alive == True:
            i.draw(screen)
    
    screen.blit(dog.image[0][0], (90, 800))

    screen.blit(background.image[0][0], (0, 0))

    # flip() the display to put your work on screen
    screen.blit(text, (3, 3))
    temp = (pygame.mouse.get_pos()[0] - cursor.width/2, pygame.mouse.get_pos()[1] - cursor.height/2)
    screen.blit(cursor.image[0][0], temp)
    pygame.display.flip()

    #conta 

# Ralsei é o melhor (não, patos são, QUACKIESSSS :3)
#imagina ter comentarios >:(
def enemy():
    enemy_list = []

    for e in range(0, 200):
        x_cor = random.randint(25, 361)
        e = Object("enemy.png", 70, 70, x_cor, 25)
        enemy_list.append(e)

        return enemy_list

r1.roundStart(1, 3)

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