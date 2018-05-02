add_library('sound')
import os 

path = os.getcwd()
print path
cat = loadImage(path+"/files/images.png")
poop = loadImage(path+"/files/poo.png")
heart = loadImage(path+"/files/heart.png")
startscreen = loadImage(path+"/files/screen.png")
bckground = loadImage (path +"/files/backgroundd.png")
bckground.resize(700,700)
backgroundmusic = SoundFile (this, path+"/files/backgroundmusic.mp3") 
coin = SoundFile (this, path+"/files/coin.mp3")
gameover = SoundFile (this, path+"/files/gameover.mp3")

hsf = path+"highscore.txt"

import random, time

def setup():
  size (game.screenw,game.screenh)
  backgroundmusic.play() 


def distance(o1,o2):
  d = ((o1.x - o2.x)**2.0 + (o1.y - o2.y)**2.0 )**(0.5)
  return d

class Game: 

  def __init__(self):
    self.pooplist = []
    self.heartlist = []
    self.creature = None 
    self.screenw = 700
    self.screenh = 700
    self.score = 0
    self.highscore = 0
    self.state = "UNSTARTED"

  def creategame(self):
    self.pooplist = []
    self.heartlist = []
    self.creature = Creature(self.screenw//2,self.screenh-40,70,80, self.screenw,8)
    self.score = 0
    self.state = "PLAYING"

    
    with open(hsf, "a") as f:
      pass
    with open(hsf, "r") as f:
      hs = f.read().strip()
      print("hs", hs)
      if hs == '':
        self.highscore = 0
      else:
        self.highscore = int(hs)



  def display(self):
    for poop in self.pooplist: 
      poop.display()

    for heart in self.heartlist:
      heart.display()

    self.creature.display()

    fill(255)
    textAlign(LEFT)
    textSize(20)
    text("Score: "+str(self.score), 30, 30)
    text("Highscore: "+str(self.highscore), 30, 60)


  def generateObjects(self):

    r = random.random() 
    if 0.1 >= r: 

      self.pooplist.append(Poop(random.randint(0,700),0,30,30,6)) 
      for poop in self.pooplist: 
        if poop.y >= self.screenh: 
          self.pooplist.remove(poop)

    if 1 - 0.05 <= r: 

      self.heartlist.append(Heart(random.randint(0,700),0,30,30,8))
      for heart in self.heartlist:
        if heart.y >= self.screenh:
          self.heartlist.remove(heart)

  def checkCollision(self):
    for poop in self.pooplist:
      if distance(poop,self.creature) < (poop.w + self.creature.w) / 2 - 8:
        self.endGame()
        backgroundmusic.stop()
        gameover.play()

    for heart in self.heartlist: 
      if distance(heart,self.creature) < (heart.w + self.creature.w) / 2: 
        self.score += 1
        coin.play()
        if self.score > self.highscore:
          self.highscore = self.score
        self.heartlist.remove(heart)
        print ("score", self.score)

  def move(self):
    for poop in self.pooplist:
      poop.move()

    for heart in self.heartlist: 
      heart.move() 

    self.creature.move()

  def endGame(self):
    self.state = "GAME OVER"
    with open(hsf, "w") as f:
      f.write(str(self.highscore))

class Creature:

  def __init__(self,x,y,w,h,screenw,dx):
    self.x = x 
    self.y = y 
    self.w = w
    self.h = h
    self.keyHandler = {37:False, 39:False}
    self.screenw = screenw
    self.dx = dx
    self.doraemon = cat
    
  def display(self):
    fill(255,0,0)
    imageMode(CENTER)
    image(self.doraemon,self.x,self.y,self.w,self.h)

  def move(self):
    if self.keyHandler[37] == True:
      self.x-=self.dx 
    if self.keyHandler[39] == True: 
      self.x+=self.dx
    if self.screenw < self.x: 
      self.x = 0
    if self.x < 0:
      self.x = 700


class Poop: 

  def __init__(self,x,y,w,h,dy):
    self.x = x 
    self.y = y 
    self.w = w 
    self.h = h 
    self.dy = dy
    self.poop = poop


  def display(self):
    fill(139,69,19)
    image(self.poop,self.x,self.y,self.w,self.h) 

  def move(self):
    self.y += self.dy 

class Heart: 

  def __init__(self,x,y,w,h,dy):
    self.x = x 
    self.y = y 
    self.w = w 
    self.h = h 
    self.dy = dy
    self.heart = heart


  def display(self):
    fill(255,200,200)
    image(self.heart,self.x,self.y,self.w,self.h)

  def move(self): 
    self.y += self.dy

game = Game()


def draw():
  if game.state == "UNSTARTED": 
    print("UNSTARTED")
    image(startscreen, 0, 0, 700, 700)
    textSize(30)
    textAlign(CENTER)
    text ("[PRESS ANY KEY TO PLAY]", game.screenw/2,game.screenh-100)
    

  elif game.state == "PLAYING":
    #image(bckground,0,0,700,700)
    background(bckground)
    game.display() 
    game.move()
    game.generateObjects()
    game.checkCollision()
  elif game.state == "GAME OVER":
    text("RESTART", game.screenw-100, game.screenh-100)

def keyPressed():
  # print (keyCode)
  if game.state == "UNSTARTED":
    print ("PRESS ANY KEY TO PLAY")
    game.creategame()
  game.creature.keyHandler[keyCode]=True 


def keyReleased():
  game.creature.keyHandler[keyCode]=False 


def mousePressed():
  if int(mouseX) in range(game.screenw-160, game.screenw-40) \
    and int(mouseY) in range(game.screenh-130, game.screenh-100):
    time.sleep(0.5)
    game.creategame()



        
