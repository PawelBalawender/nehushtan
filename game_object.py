#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
This module implements an Abstract Base Class for every snake-ish object
"""


class GameObject:
    def __init__(self, board, char: str, color: str, fields: list):
        """
        Argument 'board' is of type Board from the board module
        I don't include it since it would cause a circular dependency
        """
        self.board = board
        self.char = char  # unique char that represent the obj on the board
        self.color = color  # color of the patch of this object in GUI
        self.fields = fields  # list of fields on brd occupied by the object

        self.board.add_obj(self)

