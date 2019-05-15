from Globals import *
import pygame

class Player:

    def __init__(self, id):
        self.id = id
        self.soldiers = []
        if id == 0:
            self.color = blue
            self.my_turn = True
            #self.default_img = pygame.image.load("img/blue/blueDefault.jpg")
            #self.default_img = pygame.transform.scale(self.default_img, (square_size, square_size))
            #self.default_img = pygame.image.tostring(self.default_img, "RGB")
        if id == 1:
            self.color = red
            self.my_turn = False
            #self.default_img = pygame.image.load("img/red/redDefault.jpg")
            #self.default_img = pygame.transform.scale(self.default_img, (square_size, square_size))
            #self.default_img = pygame.image.tostring(self.default_img, "RGB")


