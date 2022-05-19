#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np

class Game:
    def __init__(self):

        self.state = np.zeros(shape=(4,4), dtype=np.int64)
        a, b = random.sample([(x,y) for x in range(4) for y in range(4)], 2)

        self.state[a] = 2
        self.state[b] = 2

        self.gameover = False

    def reset(self):
        self.__init__()
        return self.state


    def check_gameover(self):

        if not self.state.all():
            return False

        for y in range(3):
            for x in range(4):
                if self.state[y, x] == self.state[y+1, x]:
                    return False
        for y in range(4):
            for x in range(3):
                if self.state[y, x] == self.state[y, x+1]:
                    return False
        
        self.gameover = True
        return True

    def new_tile(self):

        empty_tiles = np.argwhere(self.state == 0)

        if not empty_tiles.any():
            return False

        if random.random() < 0.9:
            new_tile_val = 2
        else:
            new_tile_val = 4

        new_tile_loc = random.choice(empty_tiles)

        self.state[new_tile_loc[0], new_tile_loc[1]] = new_tile_val

        return new_tile_loc

    def step(self, action):

        if self.gameover:
            return self.reset()
        
        merged = []

        reward = 0

        moved = False

        if action == 0:

            for y in range(4):
                for x in range(4):

                    tile_val = self.state[y, x]

                    if tile_val:

                        new_y = y

                        while new_y > 0 and self.state[new_y - 1, x] == 0:
                            new_y -= 1
                        
                        if new_y > 0 and tile_val == self.state[new_y-1, x] and (new_y - 1, x) not in merged:

                            self.state[y, x] = 0 
                            self.state[new_y-1, x] *= 2
                            merged.append((new_y-1, x))
                            reward += tile_val * 2
                            moved = True
                        
                        elif new_y != y:

                            self.state[y, x] = 0
                            self.state[new_y, x] = tile_val
                            moved = True
        
        elif action == 1:

            for y in range(4):
                for x in range(3, -1, -1):

                    tile_val = self.state[y, x]

                    if tile_val:

                        new_x = x

                        while new_x < 3 and self.state[y, new_x + 1] == 0:
                            new_x += 1
                        
                        if new_x < 3 and tile_val == self.state[y, new_x + 1] and (y, new_x + 1) not in merged:

                            self.state[y, x] = 0 
                            self.state[y, new_x+1] *= 2
                            merged.append((y, new_x))
                            reward += tile_val * 2
                            moved = True
                        
                        elif new_x != x:

                            self.state[y, x] = 0
                            self.state[y, new_x] = tile_val
                            moved = True

        elif action == 2:

            for y in range(3, -1, -1):
                for x in range(4):

                    tile_val = self.state[y, x]

                    if tile_val:

                        new_y = y

                        while new_y < 3 and self.state[new_y + 1, x] == 0:
                            new_y += 1
                        
                        if new_y < 3 and tile_val == self.state[new_y+1, x] and (new_y +1, x) not in merged:

                            self.state[y, x] = 0 
                            self.state[new_y+1, x] *= 2
                            merged.append((new_y+1, x))
                            reward += tile_val * 2
                            moved = True
                        
                        elif new_y != y:

                            self.state[y, x] = 0
                            self.state[new_y, x] = tile_val
                            moved = True

        elif action == 3:

            for y in range(4):
                for x in range(4):

                    tile_val = self.state[y, x]

                    if tile_val:

                        new_x = x

                        while new_x > 0 and self.state[y, new_x-1] == 0:
                            new_x -= 1
                        
                        if new_x > 0 and tile_val == self.state[y, new_x-1] and (y, new_x-1) not in merged:

                            self.state[y, x] = 0 
                            self.state[y, new_x-1] *= 2
                            merged.append((y, new_x-1))
                            reward += tile_val * 2
                            moved = True
                        
                        elif new_x != x:

                            self.state[y, x] = 0
                            self.state[y, new_x] = tile_val
                            moved = True

        if moved:
            self.new_tile()
        
        self.check_gameover()

        return self.state, reward