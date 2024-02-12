import pygame
from pygame.locals import *
import time
import random

size = 40
backgroundColour = (0, 0, 0)
textColour = (255, 255, 255)

class Apple:
	def __init__(self, parentScreen):
		self.parentScreen = parentScreen
		self.image = pygame.image.load("diamond.png").convert()
		self.image = pygame.transform.scale(self.image, (40, 40))		
		self.x = size*3
		self.y = size+3

	def draw(self):
		self.parentScreen.blit(self.image, (self.x, self.y))
		pygame.display.flip()

	def move(self):
		self.x = random.randint(1,24)*size
		self.y = random.randint(1,19)*size

class snake:
	def __init__(self, parentScreen):
		self.parentScreen = parentScreen
		self.block = pygame.image.load("block.jpg").convert()
		self.block = pygame.transform.scale(self.block, (40, 40))
		self.direction = 'down'

		self.length = 1
		self.x = [40]
		self.y = [40]
		
	
	def increaseLength(self):
		self.length += 1
		self.x.append(-1)
		self.y.append(-1)

	def moveLeft(self):
		self.direction = 'left'

	def moveRight(self):
		self.direction = 'right'

	def moveUp(self):
		self.direction = 'up'

	def moveDown(self):
		self.direction = 'down'

	def draw(self):
		#self.parentScreen.fill(self.renderBackground)
		for i in range(self.length):
			self.parentScreen.blit(self.block, (self.x[i], self.y[i]))
		pygame.display.flip()

	def walk(self):

		for i in range(self.length-1,0,-1):
			self.x[i] = self.x[i-1]
			self.y[i] = self.y[i-1]

		if self.direction == 'left':
			self.x[0] -= size
		if self.direction == 'right':
			self.x[0] += size
		if self.direction == 'up':
			self.y[0] -= size
		if self.direction == 'down':
			self.y[0] += size
			
		self.draw()


class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Snake")

		pygame.mixer.init()
		self.backgroundMusic()

		self.surface = pygame.display.set_mode((1000, 800))
		#self.surface.fill(self.renderBackground)
		self.snake = snake(self.surface)
		self.snake.draw()
		self.apple = Apple(self.surface)
		self.apple.draw()

	def isCollision(self, x1, y1, x2, y2):
		if x1 >= x2 and x1 < x2 + size:
			if y1 >= y2 and y1 < y2 + size:
				return True
		return False


	def backgroundMusic(self):
		pygame.mixer.music.load("background.mp3")
		pygame.mixer.music.play(-1,0)

	def playSound(self, soundName):
		if soundName == "crash":
			sound = pygame.mixer.Sound("crash.mp3")
		elif soundName == 'mcEat':
			sound = pygame.mixer.Sound("mcEat.mp3")

		pygame.mixer.Sound.play(sound)

	def renderBackground(self):
		bg = pygame.image.load("backgroundPic.jpg")
		self.surface.blit(bg, (0,0))


	def play(self):
		self.renderBackground()
		self.snake.walk()
		self.apple.draw()
		self.displayScore()
		pygame.display.flip()

		#logic of snake colliding with apple
		if self.isCollision(self.snake.x[0], self.snake.y[0], self.apple.x,  self.apple.y):
			self.playSound("mcEat")
			self.snake.increaseLength()
			self.apple.move()

		#logic of snake colliding with itself
		for i in range(3, self.snake.length):
			if self.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
				self.playSound("crash")
				raise "Collision Occurred"

	def showGameOver(self):
		self.renderBackground()
		font = pygame.font.SysFont('arial', 30)
		lineOne = font.render(f"Game is over! Your score is {self.snake.length}", True, textColour)
		self.surface.blit(lineOne, (200, 300))
		lineTwo = font.render("To play again press Enter. To exit press Escape!", True, textColour)
		self.surface.blit(lineTwo, (200, 350))
		pygame.mixer.music.pause()
		pygame.display.flip()



	def displayScore(self):
		font = pygame.font.SysFont('arial', 30)
		score = font.render(f"score: {self.snake.length}", True, textColour)
		self.surface.blit(score, (850, 10))


	def reset(self):
		self.snake = snake(self.surface)
		self.apple = Apple(self.surface)

	def run(self):
		run = True
		pause = False

		while run:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						run = False

					if event.key == K_RETURN:
						pygame.mixer.music.unpause()
						pause = False

					if not pause:
						if event.key == K_LEFT:
							self.snake.moveLeft()

						if event.key == K_RIGHT:
							self.snake.moveRight()

						if event.key == K_UP:
							self.snake.moveUp()

						if event.key == K_DOWN:
							self.snake.moveDown()

				elif event.type == QUIT:
					run = False


			try:
				if not pause:
					self.play()

			except Exception as e:
				self.showGameOver()
				pause = True
				self.reset()

			time.sleep(0.2)



if __name__ == "__main__":
	game = Game()
	game.run()

	

