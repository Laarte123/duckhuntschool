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
click = False
health = 100

powers =[0, 0, 0]
pa = "nada"

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 1120))
clock = pygame.time.Clock()
running = True
pygame.font.init() # you have to call this at the start, 
pygame.mixer.pre_init()
pygame.mixer.init()

screen.set_alpha(None)

# Fonts
my_font = pygame.font.Font('gamefont.ttf', 40)
titleFont = pygame.font.Font('m29.TTF', 150)

# Sound effects
win = pygame.mixer.Sound("dogHappy.wav")
lose = pygame.mixer.Sound("dogL.wav")
shoot = pygame.mixer.Sound("gunShot.wav")
intro = pygame.mixer.Sound("intro.mp3")
musica = pygame.mixer.music.load("dht.wav")

class Game:
    def __init__(self):
        self.state = 1
        self.roundNum = 1
        self.roundDiff = 1

# Definir o jogo como uma classe
class Round:
    def __init__(self):
        self.maxFrame = 10
        self.scene = []
        self.state = 3
        self.patosm = 0
        self.curFrame = 0
        self.dogpos = 800
        self.rScore = 0
        if pa == "ammo":
            self.ammo = 999999
        else:
            self.ammo = 3
        self.subrnd = 9
        self.doganim = 0
    
    def roundStart(self, dif, ducknum, gm):
        self.curFrame = 0
        self.maxFrame = 180
        self.state = 1
        self.dif = dif
        self.scene = []
        self.ducks = ducknum
        self.rScore = 0
        self.ammo = 3

        self.dogpos = 800

        # Avançar a subronda e verificar se a ronda acabou
        self.subrnd += 1
        if self.subrnd >= 10:
            gm.roundNum += 1
            gm.roundDiff += 0.3
            self.subrnd = 0
            self.curFrame = 0
            self.state = 3
            for i in miniDDisplay:
                i.state = 0
        else:
            spawnDuckie(self.scene)
            self.state = 0
    
    def roundCheck(self, dog):
        #UwUUwUUwU
        if self.state == 0:
            val = True
            for i in self.scene:
                if i.state != 1:
                    val = False
            
            if self.ammo <= 0:
                val = True
            
            if val == True:
                self.roundEnd(dog)

        elif self.state == 3:
            self.maxFrame = 301
            dog.changeState(2)
            if self.curFrame <= 1:
                intro.play()
                dog.frameTime = 4
                dog.x = 110
                dog.y = 700
                self.doganim = 0
            elif self.curFrame <= 64:
                dog.x += 2
                self.doganim += 1
                if self.doganim >= 12:
                    self.doganim = 0
            elif self.curFrame >= 65 and self.curFrame < 82:
                self.doganim += 1
                if self.doganim >= 20:
                    self.doganim = 12
            elif self.curFrame >= 82 and self.curFrame < 134:
                dog.x += 2
                self.doganim += 1
                if self.doganim >= 12:
                    self.doganim = 0
            elif self.curFrame >= 134 and self.curFrame < 142:
                self.doganim = 20
            elif self.curFrame >= 160 and self.curFrame < 200:
                self.doganim = 25
                dog.x += 2
                dog.y -= 9
            elif self.curFrame >= 200:
                self.doganim = 31
                dog.x += 2
                dog.y += 9
            if self.curFrame == 300:
                spawnDuckie(self.scene)
                self.state = 0
            screen.blit(dog.image[2][self.doganim // 4], (dog.x, dog.y))
        

        if r1.state == 2:
            if r1.curFrame >= r1.maxFrame:
                self.roundStart(gm.roundDiff, 1, gm)
            else:
                self.roundEnd(dog)
        
        self.curFrame += 1

        #print(len(self.scene), self.curFrame, self.doganim)
    
    def roundEnd(self, dog):
        global score
        global win
        global lose
        global screen
        global miniDDisplay
        global health
        print("THY BEAST HAS BEEN SLAYED!")

        # Só é executado no primeiro frame
        if self.state == 0:
            self.state = 2
            self.curFrame = 0
            if self.rScore != 0:
                # Jogador acerta o pato
                win.play()
                dog.changeState(0)
                print(self.subrnd)
                miniDDisplay[self.subrnd].state = 1

                # Colocar a posição do cão
                if self.scene[-1].x < 295:
                    dog.x = 295
                elif self.scene[-1].x > 720:
                    dog.x = 720
                else:
                    dog.x = self.scene[-1].x

            # Jogador perde o pato
            else:
                dog.changeState(1)
                lose.play()
                health -= 5
                if health <= 0:
                    gm.state = 1
                dog.x = screen.get_width() / 2 - dog.width / 2


        # Atualizar a altura do cão
        dog.y = self.dogpos
        dog.draw(screen)

        # Mover o cão para cima por 100 frames e mover para baixo nos ultimos 100 frames
        if self.curFrame <= 100:
            if self.dogpos >= 580:
                self.dogpos -= 5
            else:
                self.dogpos = 579
        elif self.curFrame >= 100:
            self.dogpos += 5
        
        self.maxFrame = 200
        
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
        self.cFall = 0
        self.frameTime = frameTime
        self.id = id
        # Agora cada objeto tem estados, só é usado nos patos (W patos skill issue dos outros)
        self.state = 0
        self.speed = randint(2* self.id, 3* self.id) + 1

        print(self.speed)

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
        self.conta = 0

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

gm = Game()
r1 = Round()

duck1 = sprite(100, 100)
duck1.load(["d11.png", "d12.png", "d13.png"])
duck1.load(["d1Hit.png"])
duck1.load(["d1s.png"])

duck2 = sprite(100, 100)
duck2.load(["d21.png", "d22.png", "d23.png"])
duck2.load(["d2Hit.png"])
duck2.load(["d2s.png"])

duck3 = sprite(100, 100)
duck3.load(["d31.png", "d32.png", "d33.png"])
duck3.load(["d3Hit.png"])
duck3.load(["d3s.png"])

S = sprite(100, 100)
S.load(["spam1.png", "spam2.png"])
S.load(["spam1.png", "spam2.png"])
S.load(["spam1.png", "spam2.png"])

cursor = sprite(100, 100)
cursor.load(["cursor.png"])

dog = sprite(200, 200)
dog.load(["dog1.png"])
dog.load(["dogL1.png", "dogL2.png"])
dog.load(["dogCut1.png", "dogCut2.png","dogCut3.png","dogCut4.png","dogCut5.png","dogCut6.png","dogCut7.png","dogCut8.png"])

dogObj = Object(dog.image, 0, 0, dog.width, dog.height, 10, 0)

miniD = sprite(30, 30)
miniD.load(["miniD1.png"])
miniD.load(["miniD2.png"])

bullet = sprite(30, 30)
bullet.load(["bullet.png"])

x2 = sprite(50, 50)
x2.load(["x2.png"])

vida = sprite(50,50)
vida.load(["jug.png"])

ammo = sprite(50, 50)
ammo.load (["ammo.png"])

psprite = sprite(50, 50)
psprite.load(["x2.png"])
psprite.load(["jug.png"])
psprite.load(["ammo.png"])

pow = Object(psprite.image, 0, 0, psprite.width, psprite.height, 10, 0)

miniDDisplay = []

for i in range(0, 10):
    miniObj = Object(miniD.image, 0, 0, miniD.width, miniD.height, 10, 0)
    miniDDisplay.append(miniObj)

background1 = sprite(screen.get_width(), screen.get_height())
background1.load(["back1.png"])

background2 = sprite(screen.get_width(), screen.get_width() * 0.6692)
background2.load(["background2.png"])


def spawnDuckie(scene):
    val = False

    count = 0
    
    special = randint(1, 20)

    if special == 15:
        temp = Object(duck2.image, 0, 0, duck2.width, duck2.height, 10, 2)
    elif special == 16:
        temp = Object(duck3.image, 0, 0, duck3.width, duck3.height, 10, 3)
    elif special == 17:
        temp = Object(duck2.image, 0, 0, duck2.width, duck2.height, 10, 2)
    elif special == 18:
        temp = Object(S.image, 0, 0, S.width, S.height, 10, 4)
    elif special == 19:
        temp = Object(S.image, 0, 0, S.width, S.height, 10, 4)
    elif special == 20:
        temp = Object(duck1.image, 0, 0, duck1.width, duck1.height, 10, 1)
    else:
        temp = Object(S.image, 0, 0, S.width, S.height, 10, 4)

    
#UwU

    while val == False:
        count += 1
        val = True
        
        temp.y = screen.get_height() / randint(1, 20) + 100
        if temp.y > 400:
            temp.y = 500

        temp.x = randint(-150, -100)

        for i in scene:
            if abs(temp.y - i.y) < i.height:
                val = False
            if temp.y + temp.height > 1032:
                val = False

        if count >= 50:
             val = True
        
    scene.append(temp)

def events():
    global running
    global health
    eventList = pygame.event.get()

    # Verificar eventos
    for i in eventList:
        #print(i)
        if i.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == 1:
                checkMouse()
            elif pygame.mouse.get_pressed()[2] == 1:
                health -= 5
        if i.type == pygame.QUIT:
            running = False

def checkMouse():
    mousePos = pygame.mouse.get_pos()
    global score
    global patosm
    global b
    global r1
    global click
    global running
    #print(mousePos)
    if gm.state == 0:
        if r1.state == 0:
            shoot.play()
            r1.ammo -= 1
            for i in r1.scene:
                if i.id >= 1 and i.id <= 4:
                    # Verificar se o pato está vivo
                    if i.state == 0:
                        # Verificar se o cursor está em cima do pato
                        if mousePos[0] > i.x and mousePos[0] < i.x + i.width:
                            if mousePos[1] > i.y and mousePos[1] < i.y + i.height:
                                click = True
                                # Matar o pato
                                i.changeState(2)
                                # i.alive = False
                                if powers[0]:
                                    score += i.id * 2
                                else:
                                    if i.id == 2:
                                        score += 2
                                        r1.rScore += 2
                                    if i.id == 1:
                                        score += 1
                                        r1.rScore += 1
                                    if i.id == 3:
                                        score += 3
                                        r1.rScore += 3
                                b = b +1
                                patosm = patosm + 1
                                if i.id == 4:
                                    j = randint(0,2)
                                    score += 2
                                    r1.rScore += 2
                                    powers[j] = True
                                break
    # Menu principal
    elif gm.state == 1:
        # Verificar se o jogador clicou em alguma as opções
        if topt1hit.collidepoint(mousePos[0], mousePos[1]):
            gm.state = 0
            pygame.mixer.music.stop()
        elif topt2hit.collidepoint(mousePos[0], mousePos[1]):
            gm.state = 2
            pygame.mixer.music.stop()
        elif topt3hit.collidepoint(mousePos[0], mousePos[1]):
            running = False
    # Definições
    #elif gm.state == 2:

res = 0

# Função para as fisicas
def physicz():
    #UwU
    global r1
    global res

    for i in r1.scene:
        # Evitar que o pato vá para fora do ecra
        if i.y  < 100:
            i.conta = 51
        if i.y > 600:
            i.y = i.y - 3
        
        # Mudar a velocidade do pato cada 33 frames
        if i.conta == 33:
            i.speed = randint(2, 3)
        elif i.conta == 66:
            i.speed = randint(2, 3)
             
        if i.state == 0:
            a = randint(1,2)

            # Fazer o pato subir
            if i.conta > 50:
                # Mover o pato conforme o seu nivel
                if i.id == 1:
                    #i.x += randint(4, 6)
                    i.x += 6 * gm.roundDiff
                    i.y += randint(2, 3)
                elif i.id == 2:
                    #i.x += randint(5, 8)
                    i.x += 8 * gm.roundDiff
                    i.y += 2
                elif i.id == 3:
                    #i.x += randint(8, 11)
                    i.x += 11 * gm.roundDiff
                    i.y += 3
                elif i.id == 4:
                    i.x += 8 * gm.roundDiff
                    i.y += 2
            # O mesmo mas quando está a descer
            else:
                if i.id == 1:
                    i.x += 6 * gm.roundDiff
                    i.y -= randint(2, 3)
                elif i.id == 2:
                    i.x += 8 * gm.roundDiff
                    i.y -= 2
                elif i.id == 3:
                    i.x += 11 * gm.roundDiff
                    i.y -= 3
                elif i.id == 4:
                    i.x += 8 * gm.roundDiff
                    i.y -= 2

            # Reniciar o contador cada 100 frames
            if i.conta == 100:
                i.conta = 0

        # Fazer o pato cair caso ter levado um tiro
        elif i.state == 1:
            i.y += 9
            i.cFall += 1
            # Tirar para funi
            if i.conta % 5 == 0:
                i.image[1][0] = pygame.transform.flip(i.image[1][0], True, False)
                if i.cFall % 2 == 0:
                    i.x += 5
                else:
                    i.x -= 5
        elif i.state == 2:
            if i.conta >= 20:
                i.changeState(1)
        i.conta += 1
        
        
        if i.x >= res.current_w:
            i.changeState(1)


# Render function
def render():
    global res
    global patosm
    global r1
    global dogObj
    global click
    global gm
    global health

    if gm.state == 0:
        print(r1.curFrame, r1.state, r1.subrnd)
        pygame.mouse.set_visible(False)
        if click == False:

            screen.fill((0, 150, 255))

            if r1.state == 1:
                if r1.curFrame >= r1.maxFrame:
                    r1.state = 0
                    r1.curFrame = 0
            
            res = pygame.display.Info()

            physicz()
            
            events()
            text = my_font.render("score: " + str(score), False, (128, 208, 16))
            roundTxt = my_font.render(str(gm.roundNum), False, (128, 208, 16))
            scoreTxt = my_font.render(str(score), False, (255, 255, 255))
            htxt = my_font.render(str(health), False, (255, 255, 255))
            
            for i in r1.scene:
                i.draw(screen)

            hrec = pygame.rect.Rect(480, 1050, 200 * (health / 100), 25)

            hr = pygame.rect.Rect(680 - health * 5, 1050, 200 * (health / 100), 25)

            pygame.draw.rect(screen, (255, 255, 255), hr)

            screen.blit(background1.image[0][0], (0, 0))

            r1.roundCheck(dogObj)

            if r1.state == 3 :
                if r1.curFrame >= 200:
                    screen.blit(background1.image[0][0], (0, 0))
            
            if r1.state == 2:
                screen.blit(background1.image[0][0], (0, 0))

            t = 0
            for j in powers:
                global pa
                if j == True:
                    if t == 0:
                        pow.changestate(0)
                        pow.draw()
                        pa = "x2"
                    elif t == 1:
                        pow.changestate(1)
                        pow.draw()
                        pa = "vida"
                    elif t == 2:
                        pow.changestate(2)
                        pow.draw()
                        pa = "ammo"
                t+=1

            # score text
            screen.blit(scoreTxt, (192 * 5, 200 * 5))

            screen.blit(roundTxt, (41 * 5, 183 * 5))

            screen.blit(htxt, (100, 1))

            x = 450
            ctemp = 1
            for i in miniDDisplay:
                screen.blit(i.image[i.state][0], (x + ctemp * 30, 1005))
                ctemp+=1.3
            
            x = 95
            ctemp = 1
            for i in range(r1.ammo):
                screen.blit(bullet.image[0][0], (x + ctemp * 30, 1005))
                ctemp+=1.3

            temp = (pygame.mouse.get_pos()[0] - cursor.width/2, pygame.mouse.get_pos()[1] - cursor.height/2)
            screen.blit(cursor.image[0][0], temp)
        
        else:
            click = False
            screen.fill((0, 0, 0))
            for i in r1.scene:
                rtemp = pygame.Rect(i.x, i.y, i.width, i.height)
                pygame.draw.rect(screen, (255, 255, 255), rtemp)
    
    elif gm.state == 1:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        pygame.mouse.set_visible(True)
        events()
        screen.fill((0, 0, 0))
        tline = pygame.Rect(160, 320, 980, 10)
        global topt1hit
        global topt2hit
        global topt3hit
        topt1hit = pygame.Rect(320, 640, 400, 35)
        topt2hit = pygame.Rect(320, 720, 400, 35)
        topt3hit = pygame.Rect(320, 800, 400, 35)

        title = titleFont.render("Duck", False, (0, 235, 222))
        title2 = titleFont.render("Hunt", False, (0, 235, 222))
        topt1 = my_font.render("Start game", False, (255, 174, 10))
        topt2 = my_font.render("Settings", False, (255, 174, 10))
        topt3 = my_font.render("Quit", False, (255, 174, 10))

        pygame.draw.rect(screen, (255, 174, 10), tline)
        screen.blit(title, (160, 80))
        screen.blit(title2, (360, 360))
        screen.blit(topt1, (320, 640))
        screen.blit(topt2, (320, 720))
        screen.blit(topt3, (320, 800))
    
    #elif gm.state == 3:

    fps = clock.get_fps()
    fpsTxt = my_font.render(str(int(fps)), False, (255, 255, 255))
    screen.blit(fpsTxt, (0, 0))
    pygame.display.flip()
    clock.tick(60)
    #clock.tick()

# Ralsei é o melhor (não, patos são, QUACKIESSSS :3)
#imagina ter comentarios >:(
#r1.roundStart(1, 1, gm)
r1.dogpos = 800

while running:
    # Literalmente o jogo inteiro
    render()

pygame.quit()
