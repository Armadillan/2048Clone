#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pygame
# import numpy as np

class Interface:

    SQUARE = True
    
    BACKGROUND_COLOR = ("#bbada0")

    LIGHT_TEXT_COLOR = pygame.Color("#f9f6f2")
    DARK_TEXT_COLOR = ("#776e65")
    VALUES_WITH_DARK_TEXT = (2, 4)


    TILE_COLOR = {
        0: ("#cdc1b4"),
        2: pygame.Color("#eee4da"),
        4: pygame.Color("#eee1c9"),
        8: pygame.Color("#f3b27a"),
        16: pygame.Color("#f69664"),
        32: pygame.Color("#f77c5f"),
        64: pygame.Color("#f75f3b"),
        128: pygame.Color("#edd073"),
        256: pygame.Color("#edcc62"),
        512: pygame.Color("#edc950"),
        1024: pygame.Color("#edc53f"),
        2048: pygame.Color("#edc22e"),
        "BIG": pygame.Color("#3c3a33") # Tiles bigger than 2048
        }

    def __init__(self, env):
        
        self.env = env
        self.w = 600
        self.h = 600

        pygame.init()

        self.initialize_fonts()

    def initialize_fonts(self):

        self.tile_font_5 = pygame.font.Font(
            os.path.join("assets", "ClearSans-Bold.ttf"),
            int(self.h * 6/29 * 7/12)
            )
        self.tile_font_4 = pygame.font.Font(
            os.path.join("assets", "ClearSans-Bold.ttf"),
            int(self.h * 6/29 * 6/12)
            )
        self.tile_font_3 = pygame.font.Font(
            os.path.join("assets", "ClearSans-Bold.ttf"),
            int(self.h * 6/29 * 5/12)
            )
        self.tile_font_2 = pygame.font.Font(
            os.path.join("assets", "ClearSans-Bold.ttf"),
            int(self.h * 6/29 * 4/12)
            )
        self.tile_font_1 = pygame.font.Font(
            os.path.join("assets", "ClearSans-Bold.ttf"),
            int(self.h * 6/29 * 3/12)
            )
        
        self.gameover_font_1 = pygame.font.SysFont(
            "FreeSans", int(self.h * (1/10)), bold=True
            )
        self.gameover_size_1 = self.gameover_font_1.size("GAME OVER")
        self.gameover_text_1 = self.gameover_font_1.render(
            "GAME OVER", True, (20,20,20)
            )

        self.gameover_font_2 = pygame.font.SysFont(
            "FreeSans", int(self.h * (1/20),), bold=True
            )
        self.gameover_size_2 = self.gameover_font_2.size(
            "Press \"r\" to restart"
            )
        self.gameover_text_2 = self.gameover_font_2.render(
            "Press \"r\" to restart", True, (20,20,20)
                )

    def tile(self, x, y, n):

        rect_x = (x+1) * self.w/29 + x * self.w * (6/29)
        rect_y = (y+1) * self.h/29 + y * self.h * (6/29)

        rect = pygame.Rect(
        rect_x, rect_y, self.w * (6/29), self.h * (6/29))

        # Does not render text if the tile is 0
        if not n:
            text_render = pygame.Surface((0,0))
            text_x = 0
            text_y = 0

        else:

            # Get string from int and it's length
            text = str(n)
            l = len(text)

            # Chooses color for text
            if n in self.VALUES_WITH_DARK_TEXT:
                text_color = self.DARK_TEXT_COLOR
            else:
                text_color = self.LIGHT_TEXT_COLOR

            # Chooses font size based on length of text
            if l < 3:
                font = self.tile_font_5
            elif l == 3:
                font = self.tile_font_4
            elif l == 4:
                font = self.tile_font_3
            elif l < 7:
                font = self.tile_font_2
            else:
                font = self.tile_font_1

            # Renders font
            text_render = font.render(text, True, text_color)
            # Gets size of text
            size = font.size(text)

            # Calculates text coordinates
            text_x = (x+1) * self.w/29 \
                + (x+0.5) * self.w * (6/29) - size[0] / 2
            text_y = (y+1) * self.h/29 \
                + (y+0.5) * self.h * (6/29) - size[1] / 2

        return rect, text_render, (text_x, text_y)

    def check_action(self, action):

        modifiers = {
            0: (0, -1),
            1: (+1, 0),
            2: (0, +1),
            3: (-1, 0)
                }
        x_mod, y_mod = modifiers[action]
        board_array = self.env.state
        for x in range(4):
            for y in range(4):
                    if board_array[y][x] != 0 and \
                        4 not in (x_mod + x, y_mod + y)  and \
                        -1 not in (x_mod + x, y_mod + y) and \
                        ((board_array[y+y_mod][x+x_mod] == 0) or \
                        (board_array[y][x] == board_array[y+y_mod][x+x_mod])):
                            return True

        return False

    def main(self):
        """

        Starts the game.
        This is the main game loop.

        """

        # Initial status
        playing = True
        gameover = False
        score  = 0
        moves = 0

        # Gets initial game state
        board_array = self.env.reset()

        # Keeps a counter of score and moves made in the caption
        pygame.display.set_caption(
            "2048" + " " * 10 + "Score: 0   Moves: 0"
            )

        # Initializes window and a drawing surface
        win = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE)
        surface = win.copy()

        # Main game loop
        while playing:

            moved = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    playing = False
                    break

                if event.type == pygame.VIDEORESIZE:
                    # Handles window resizing

                    self.w, self.h = win.get_size()
                    # Sets width and height equal if SQUARE is True
                    if self.SQUARE:
                        if self.w > self.h:
                            self.w = self.h
                        else:
                            self.h = self.w
                    # Makes new drawing surface
                    surface = win.copy()
                    # Re-initalizes fonts based on new window size
                    self.initialize_fonts()

                if event.type == pygame.KEYDOWN:
                    # Handles user input

                    if event.key == pygame.K_r:
                        #Restarts the game
                        board_array = self.env.reset()
                        score = 0
                        moves = 0
                        moved = True
                        gameover = False
                        surface.fill(self.BACKGROUND_COLOR)

                    elif not gameover:

                        action_keymap = {
                            pygame.K_UP: 0, pygame.K_w: 0,
                            pygame.K_RIGHT: 1, pygame.K_d: 1,
                            pygame.K_DOWN : 2, pygame.K_s: 2,
                            pygame.K_LEFT: 3, pygame.K_a: 3,
                            }

                        if event.key in action_keymap:
                            action = action_keymap[event.key]
                            if self.check_action(action):
                                board_array, reward = self.env.step(action)
                                moved = True
                                moves += 1
                                score += reward

            # Breaks loop if game is over
            if not playing:
                break

            pygame.display.set_caption(
                "2048" + " " * 10 + f"Score: {int(score)}"
                + f"   Moves: {moves}"
            )

            # Draws all the graphics:
            surface.fill(self.BACKGROUND_COLOR)

            # Draws every tile
            for x in range(4):
                for y in range(4):

                    # Gets the tile "data"
                    n = board_array[y][x]
                    rect, text, text_coords = self.tile(x, y, n)

                    # Gets the color of the tile
                    try:
                        tile_color = self.TILE_COLOR[n]
                    except KeyError:
                        tile_color = self.TILE_COLOR["BIG"]

                    # Draws the background
                    pygame.draw.rect(
                        surface=surface,
                        color=tile_color,
                        rect=rect,
                        border_radius=int((self.w+self.h)/2 * 1/150)
                        )

                    # Blits the text surface to the drawing surface
                    surface.blit(text, text_coords)

            # Displays "gameover screen" if game is over
            if self.env.gameover:

                x_1 = self.w / 2 - self.gameover_size_1[0] / 2
                y_1 = self.h / 2 - self.h * 6/80
                x_2 = self.w / 2 - self.gameover_size_2[0] / 2
                y_2 = self.h / 2 + self.h * 1/30
                surface.blit(self.gameover_text_1, (x_1, y_1))
                surface.blit(self.gameover_text_2, (x_2, y_2))

                gameover = True

            # Fill window with background color
            win.fill(self.BACKGROUND_COLOR)

            # Blits drawing surface to the middle of the window
            w, h = win.get_size()
            if w > h:
                win.blit(surface, ((win.get_width()-self.w)/2,0))
            else:
                win.blit(surface, (0, (win.get_height()-self.h)/2))

            # Updates display
            pygame.display.update()

        # Quits pygame outside of the main game loop, if the game is over
        pygame.quit()

if __name__ == "__main__":
    # Plays the game without a bot attached :)
    # from env import PyEnv2048
    from env import Game

    # Creates Game object, passing an environment to the constructor
    # game = Game(PyEnv2048())
    game = Interface(Game())
    # Starts the interface
    game.main()
