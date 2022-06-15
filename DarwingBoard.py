# This file uses pygame to create a drawing board, so that we can draw a number,and pass that number to our model.

# required imports
import pygame
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import messagebox

# Pixel class is used to create pixels, as our display or grid is divided into 
# "28 X 28" pixels as the model required a matrix of (28 X 28) pixels to predict, The output.

class pixel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = (255,255,255)
        self.neighbors = []
    
    # To Draw pixels in the screen.
    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, (self.x, self.y, self.width + self.x, self.y + self.height))
    
    # Returns all the Neighbors of a given pixels for drawing thick. as we change the colours of all the neighboring pixels,including the clicked pixel.
    def getNeighbors(self, g):
        i = self.x // 20
        j = self.y // 20

        row = 28
        col = 28
    
        if i > 0:
            self.neighbors.append(g.pixels[i-1][j])
        if j > 0:
            self.neighbors.append(g.pixels[i][j-1])
        if i  < row - 1:
            self.neighbors.append(g.pixels[i+1][j])
        if j < col - 1:
            self.neighbors.append(g.pixels[i][j+1])
        
        if j > 0 and i > 0:
            self.neighbors.append(g.pixels[i-1][j-1])
        if j > 0 and i < row - 1:
            self.neighbors.append(g.pixels[i+1][j-1])
        if j < col - 1 and i < row - 1:
            self.neighbors.append(g.pixels[i+1][j+1])
        if j < col - 1 and i > 0:
            self.neighbors.append(g.pixels[i-1][j+1])

# Grid consists of (28 X 28) pixels that cover the whole screen.
class grid:
    # list to stroe pixel objects
    pixels = []
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.genratePixels()
    
    # this function grenate the pixels and append them in pixels list, we the grid object is formed.
    def genratePixels(self):
        x_gap = self.width // self.rows
        y_gap = self.height // self.rows
        self.pixels = []
        for r in range(self.rows):
            self.pixels.append([])
            for c in range(self.cols):
                self.pixels[r].append(pixel(r * x_gap, c * y_gap, x_gap, y_gap))
            
        for r in range(self.rows):
            for c in range(self.cols):
                self.pixels[r][c].getNeighbors(self)
    
    # This function is used to draw the grid, i.e. all the pixels on the screen.
    def Draw(self, surface):
        for r in range(self.rows):
            for c in range(self.cols):
                self.pixels[r][c].draw(surface)

    # This function returns the pixel at which user clicked.
    def click(self, pos):
        i, j = pos
        x = int(i) // self.pixels[0][0].width
        y = int(j) // self.pixels[0][0].height
        return self.pixels[x][y]
    
    # This fuction used convert all the data from grid to a predictable data, so that we can feed it to our model.
    def convert_binary(self):
        li = self.pixels

        newMatrix = [[] for x in range(len(li))]

        for i in range(len(li)):
            for j in range(len(li[i])):
                if li[i][j].colour == (255,255,255):
                    newMatrix[i].append(0)
                else:
                    newMatrix[i].append(1)

        mnist = tf.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x_test = tf.keras.utils.normalize(x_test, axis=1)
        for row in range(28):
            for x in range(28):
                x_test[0][x][row] = newMatrix[row][x]
    
        # plt.imshow(x_test[0])
        # plt.show()
        return x_test[:1]

# This function takes the data , which convert_binary returns and make prediction and display it using Tkinter message box.
def guess(li):
    model = tf.keras.models.load_model('epic_num_reader.model')
    predictions = model.predict(li)
    print(predictions[0])
    t = np.argmax(predictions[0])
    window = Tk()
    window.withdraw()
    messagebox.showinfo("Prediction", "I predict this number is a: " + str(t))
    window.destroy()

# This main function use all the upper code according to the requirement, and holds our pygame display 
def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                li = g.convert_binary()
                guess(li)
                g.genratePixels()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                clicked = g.click(pos)
                clicked.colour = (0,0,0)
                for n in clicked.neighbors:
                    n.colour = (0,0,0)
        g.Draw(win)
        pygame.display.update()

# Some essential intializations 
pygame.init()
width = height = 560

win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Number predictor (Draw in Middle for correct guess)")
g = grid(28, 28, width, height)

main()