import random
import sys

import pygame
from pygame.math import Vector2 as vector

cellSize = 40
cellNumber = 20


class Fruit:
    def __init__(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = vector(self.x, self.y)
        self.image = pygame.image.load('./Graphics/apple.png').convert_alpha()

    def draw(self):
        rect = self.image.get_rect(
            topleft=((self.pos.x * cellSize, self.pos.y * cellSize)), size=(cellSize, cellSize))
        screen.blit(self.image, rect)

    def newFruit(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = vector(self.x, self.y)


class Snake:
    def __init__(self, main):
        self.main = main
        self.body = [vector(5, 10), vector(4, 10), vector(3, 10)]
        self.direction = vector(1, 0)
        self.movement = False
        self.crunchSound = pygame.mixer.Sound('./Sound/crunch.wav')

        self.headUp = pygame.image.load(
            './Graphics/head_up.png').convert_alpha()
        self.headDown = pygame.image.load(
            './Graphics/head_down.png').convert_alpha()
        self.headLeft = pygame.image.load(
            './Graphics/head_left.png').convert_alpha()
        self.headRight = pygame.image.load(
            './Graphics/head_right.png').convert_alpha()

        self.tailUp = pygame.image.load(
            './Graphics/tail_up.png').convert_alpha()
        self.tailDown = pygame.image.load(
            './Graphics/tail_down.png').convert_alpha()
        self.tailLeft = pygame.image.load(
            './Graphics/tail_left.png').convert_alpha()
        self.tailRight = pygame.image.load(
            './Graphics/tail_right.png').convert_alpha()

        self.bodyVertical = pygame.image.load(
            './Graphics/body_vertical.png').convert_alpha()
        self.bodyHorizontal = pygame.image.load(
            './Graphics/body_horizontal.png').convert_alpha()

        self.bodyBl = pygame.image.load(
            './Graphics/body_bl.png').convert_alpha()
        self.bodyBr = pygame.image.load(
            './Graphics/body_br.png').convert_alpha()
        self.bodyTl = pygame.image.load(
            './Graphics/body_tl.png').convert_alpha()
        self.bodyTr = pygame.image.load(
            './Graphics/body_tr.png').convert_alpha()

    def draw(self):
        self.drawHead()
        self.drawTail()

        for index, block in enumerate(self.body):
            rect = pygame.Rect(block.x * cellSize, block.y *
                               cellSize, cellSize, cellSize)
            if index == 0:
                screen.blit(self.head, rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, rect)
            else:
                prevBlock = self.body[index + 1] - block
                nextBlock = self.body[index - 1] - block
                if prevBlock.x == nextBlock.x:
                    screen.blit(self.bodyVertical, rect)
                elif prevBlock.y == nextBlock.y:
                    screen.blit(self.bodyHorizontal, rect)
                else:
                    if prevBlock.x == -1 and nextBlock.y == -1 or prevBlock.y == -1 and nextBlock.x == -1:
                        screen.blit(self.bodyTl, rect)
                    elif prevBlock.x == 1 and nextBlock.y == -1 or prevBlock.y == -1 and nextBlock.x == 1:
                        screen.blit(self.bodyTr, rect)
                    elif prevBlock.x == 1 and nextBlock.y == 1 or prevBlock.y == 1 and nextBlock.x == 1:
                        screen.blit(self.bodyBr, rect)
                    elif prevBlock.x == -1 and nextBlock.y == 1 or prevBlock.y == 1 and nextBlock.x == -1:
                        screen.blit(self.bodyBl, rect)

    def drawHead(self):
        headRelation = self.body[0] - self.body[1]

        if headRelation.x == 1:
            self.head = self.headRight
        if headRelation.x == -1:
            self.head = self.headLeft
        if headRelation.y == 1:
            self.head = self.headDown
        if headRelation.y == -1:
            self.head = self.headUp

    def drawTail(self):
        tailRelation = self.body[-1] - self.body[-2]

        if tailRelation.x == 1:
            self.tail = self.tailRight
        if tailRelation.x == -1:
            self.tail = self.tailLeft
        if tailRelation.y == 1:
            self.tail = self.tailDown
        if tailRelation.y == -1:
            self.tail = self.tailUp

    def moveSanke(self):
        bodyCopy = self.body[:-1]
        bodyCopy.insert(0, bodyCopy[0] + self.direction)
        self.body = bodyCopy

    def changeDriection(self, direction):
        if not self.direction.x + direction.x == 0:
            self.movement = True
            self.direction = direction

    def snakeGrow(self):
        lastBlock = self.body[len(self.body) - 1]
        self.body.append(lastBlock)

    def collisionWalls(self):
        for block in self.body:
            if block.x < 0:
                block.x = cellNumber
            if block.x > cellNumber:
                block.x = 0
            if block.y < 0:
                block.y = cellNumber
            if block.y > cellNumber:
                block.y = 0

    def collisionBody(self):
        copyBody = self.body[1:]
        for block in copyBody:
            if block == self.body[0]:
                self.main.gameOver = True


class Main:
    def __init__(self):
        self.snake = Snake(self)
        self.fruit = Fruit()
        self.gameOver = False

    def draw(self):
        self.drawGrass()
        self.fruit.draw()
        self.snake.draw()
        self.drawScore()

    def update(self):
        if not self.gameOver:
            if self.snake.movement:
                self.snake.moveSanke()
        else:
            self.resetGame()

        self.checkCollision()
        self.snake.collisionWalls()
        self.snake.collisionBody()

    def checkCollision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.newFruit()
            self.snake.snakeGrow()
            self.snake.crunchSound.play()

        for block in self.snake.body:
            if self.fruit.pos == block:
                self.fruit.newFruit()

    def drawGrass(self):
        grassColor = (167, 209, 61)

        for row in range(cellNumber):
            for cell in range(cellNumber):
                if row % 2 == 0:
                    if cell % 2 == 0:
                        grassRect = pygame.Rect(
                            row * cellSize, cell * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColor, grassRect)
                else:
                    if cell % 2 != 0:
                        grassRect = pygame.Rect(
                            row * cellSize, cell * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColor, grassRect)

    def drawScore(self):
        scoreText = str(len(self.snake.body) - 3)
        scoreSurface = gameFont.render(scoreText, True, (56, 74, 12))
        textX = cellSize * cellNumber - 60
        textY = cellSize * cellNumber - 40
        scoreRect = scoreSurface.get_rect(center=(textX, textY))
        screen.blit(scoreSurface, scoreRect)

        appleRect = self.fruit.image.get_rect(
            midright=(scoreRect.left, scoreRect.centery))
        screen.blit(self.fruit.image, appleRect)

    def resetGame(self):
        self.snake.movement = False
        self.snake.direction = vector(1, 0)
        self.snake.body = [vector(5, 10), vector(4, 10), vector(3, 10)]
        self.gameOver = False


pygame.init()
screen = pygame.display.set_mode(
    (cellSize * cellNumber, cellSize * cellNumber))
clock = pygame.time.Clock()
gameFont = pygame.font.Font('./Font/PoetsenOne-Regular.ttf', 25)

UPDATE_SCREEN = pygame.USEREVENT
pygame.time.set_timer(UPDATE_SCREEN, 150)

main = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == UPDATE_SCREEN:
            main.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                main.snake.changeDriection(vector(-1, 0))
            if event.key == pygame.K_RIGHT:
                main.snake.changeDriection(vector(1, 0))
            if event.key == pygame.K_UP:
                main.snake.changeDriection(vector(0, -1))
            if event.key == pygame.K_DOWN:
                main.snake.changeDriection(vector(0, 1))

    screen.fill((175, 215, 70))
    main.draw()

    pygame.display.update()
    clock.tick(60)
