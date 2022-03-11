# import pygame

# class Interface:
#     def __init__(self, width, height):
#         (self.width, self.height) = (width, height)
        
#         self.white = (255, 255, 255)
#         self.green = (0, 255, 0)
#         self.blue = (0, 0, 128)
#         self.color_light = (170,170,170)
#         # dark shade of the button
#         self.color_dark = (100,100,100)
        
#         pygame.init()
#         self.screen = pygame.display.set_mode((self.width, self.height))
#         pygame.display.set_caption('Kalaha AI implementation + UI')
#         self.running = True
#         # pygame.display.flip()
#         self.start_screen()
#         self.run()

#     def start_screen(self): 
#         self.font = pygame.font.Font('freesansbold.ttf', 32)
#         self.text_title = self.font.render('Welcome to Kalaha :)', True, self.green, self.blue)
#         self.text_quit = self.font.render('quit' , True , self.white)
#         self.textRect = self.text_title.get_rect()
#         self.textRect.center = (self.width/2, self.height*0.05)
#         # pygame.display.update()
    
#     def run(self):
#         while self.running:
#             self.screen.blit(self.text_title,self.textRect)    
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     #if the mouse is clicked on the
#                     # button the game is terminated
#                     if self.width*0.8 <= mouse[0] <= self.width/2+140 and self.height*0.5 <= mouse[1] <= self.height/2+40:
#                         pygame.quit()

#                 pygame.display.update()
#             self.screen.fill((60,25,60))
#             mouse = pygame.mouse.get_pos()
#             # if mouse is hovered on a button it
#             # changes to lighter shade
#             if self.width*0.8 <= mouse[0] <= self.width/2+140 and self.height*0.5 <= mouse[1] <= self.height/2+40:
#                 pygame.draw.rect(self.screen,self.color_light,[self.width*0.8,self.height*0.5,140,40])
                
#             else:
#                 pygame.draw.rect(self.screen,self.color_dark,[self.width*0.8,self.height*0.5,140,40])
            
#             # superimposing the text onto our button
#             self.screen.blit(self.text_quit , (self.width*0.8+50,self.height*0.5))

from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import QLocale
import sys

class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        uic.loadUi('pyqtui.ui', self)
        
        self.reset_button = self.findChild(QtWidgets.QPushButton, 'reset_button')
        self.reset_button.clicked.connect(self.handle_reset)

        self.quit_button = self.findChild(QtWidgets.QPushButton, 'quit_button')
        self.quit_button.clicked.connect(self.handle_quit)

        self.p1_cup_0_ = self.findChild(QtWidgets.QLabel, 'p1_cup_0')

        self.show()

        # # setup board
        # self.game = KalahaFight(6, 6)
        # self.game.fight()

    def handle_reset(self):
        self.game.reset_board()
    def handle_quit(self):
        sys.exit(0)
    def handle_show_board(self):
        self.p1_cup_0_.setText("xd")
