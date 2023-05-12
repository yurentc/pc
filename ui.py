import pygame
import sys
from PyQt5.QtCore import Qt, QDateTime, QThread, pyqtSignal, QUrl
from acwing_spider import get_title_by_id
from datetime import datetime, timedelta
from PyQt5.QtCore import QDate
from vikas import VikaTable
from PyQt5.QtGui import QDesktopServices

# Initialize Pygame
pygame.init()

# Create a screen size
screen_width = 600
screen_height = 410
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title
pygame.display.set_caption('王钦泽的学习宝典')

# Define colors
WHITE = (255, 255, 255)

# Load fonts

font = pygame.font.Font("Microsoft YaHei", size)
font.origin = True

font_small = pygame.font.Font(None, 25)
font_medium = pygame.font.Font(None, 30)
font_large = pygame.font.Font(None, 50)

# TODO: Replace the following placeholders with the actual data
titles = ["题号", "题目标题", "次", "复习时间", "开始时间"]
data = [["1", "Example Title 1", "3", "2023-04-18", "2023-04-10"],
        ["2", "Example Title 2", "2", "2023-04-20", "2023-04-15"]]

running = True
while running:
    screen.fill(WHITE)

    # Draw the table headers
    x_pos = 10
    for title in titles:
        title_surface = font_medium.render(title, True, (0, 0, 0))
        screen.blit(title_surface, (x_pos, 10))
        x_pos += screen_width // len(titles)

    # Draw the table data
    y_pos = 50
    for row in data:
        x_pos = 10
        for cell in row:
            cell_surface = font_small.render(cell, True, (0, 0, 0))
            screen.blit(cell_surface, (x_pos, y_pos))
            x_pos += screen_width // len(titles)
        y_pos += 30

    # TODO: Add more UI elements (inputs, buttons, etc.) using Pygame

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()