#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
This module implements the Food class, which is not finished yet - no fancy
food like bananas or elixirs or something, but it's stable and it's ok 
"""
from typing import Tuple

from board import Board
from game_object import GameObject

Field = Tuple[int, int]


class Food(GameObject):
    def __init__(self, board: Board, pos: Field):
        super().__init__(board, char='F', color='g', fields=[pos])

