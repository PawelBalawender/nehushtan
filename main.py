#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
This module implements the snake game
Graphics are made in MatPlotlib
"""
import threading
from typing import Tuple, Callable, Any, Dict, List
import random
import time
import sys

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# just for type hints
Field = Tuple[int, int]  # [(1, 0), (1, 1), (1, 2)...]
Patch = patches.Rectangle
Figure = matplotlib.figure.Figure
Ax = Any  # idk how to get the type of ax; writes no attribute error


if __name__ == '__main__':
    fig, ax = plt.subplots()


    is_alive = threading.Event()
    is_alive.set()

    b = Board(fig, ax, 11, 11)
    s = Snake(board=b, callback_end=is_alive.clear)
    f = Food(b, (10, 10))

    ax.set_xlim([0, b.width])
    ax.set_ylim([0, b.height])
    ax.set_xticks([i for i in range(b.width)])
    ax.set_yticks([i for i in range(b.height)])

    fig.canvas.draw()

    def keyboard_handler(event):
        dirs = {'up': 0, 'right': 1, 'down': 2, 'left': 3}
        try:
            result = s.set_orientation(dirs[event.key])
            if not result:
                print('Wrong direction! Remember that you canot\
rotate 180 degrees')
        except KeyError:
            pass
        except ValueError:
            pass

    def input_handler():
        while is_alive.is_set():
            inp = input()

            try:
                result = s.set_orientation(int(inp))
                if not result:
                    print('Wrong direction! Remember that you cannot\
rotate 180 degrees')
            except ValueError:
                pass


    cid = fig.canvas.mpl_connect('key_press_event', keyboard_handler)
    input_thread = threading.Thread(target=input_handler)
    input_thread.start()

    while is_alive.is_set():
        # s.move gotta be in the main thread, cause it deals with mpl methods
        # for instance in patch.set_visible(False) at object deleting
        # it will result in Runtime Error if put in in a thread
        s.move()
        fig.canvas.draw()
        plt.pause(0.4)

    # input is still blocking
    print('Press any button to quit')
    input_thread.join()

