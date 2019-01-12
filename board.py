#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
This module implements the Board class, which is supposed to answer
any snake-ish request that would ever be requested
"""


class Board:
    def __init__(self, fig: Figure, ax: Ax, width: int=21, height: int=21):
        self.fig = fig
        self.ax = ax
        self.width = width
        self.height = height
        self.fields = [[0 for _ in range(width)] for _ in range(height)]
        # type: Dict[GameObj: (fields, patches)]
        GameObjDict = Dict[GameObject, Tuple[List[Field], List[Patch]]]
        self.objects: GameObjDict = dict()

        self.xsize = 1  # visual size of one tile
        self.ysize = 1
        self.EMPTY = 0  # it indicates an empty field in the array

    def rm_obj(self, obj: GameObject):
        """
        Find the fields that the given object has occupied on the board,
        clear them and then 'check out' the object from the board
        """
        # transpose to convert [(fld, ptch), ...] to [(fld, fld..), (ptch, ..)]
        for field, patch in zip(*self.objects[obj]):
            x, y = field
            self.fields[y][x] = self.EMPTY
            patch.set_visible(False)
            del patch
        del self.objects[obj]

    def add_obj(self, obj: GameObject):
        """
        'Check in' the given object and place its chars on the board
        """
        _patches = []
        for field in obj.fields:
            x, y = field
            self.fields[y][x] = obj.char
            patch = patches.Rectangle(field, self.xsize, self.ysize, fc=obj.color)
            _patches.append(patch)
            self.ax.add_patch(patch)

        self.objects[obj] = [obj.fields, _patches]

    def spawn_food(self):
        """Spawn new piece of food for the snake on the board"""
        range_x, range_y = range(self.width), range(self.height)
        e = self.EMPTY
        free = [(x, y) for x in range_x for y in range_y if self.fields[y][x] == e]
        # If the border was big enough, we could randomize field and then check
        # if it's occupied - would be faster then, but what about a case when
        # the snake is so big that it's on a significant part of the board?
        field = random.choice(free)
        f = Food(self, field)

    def rm_food(self, field: Field):
        """Remove the food that has already been eaten by the snake"""
        # v[0] are the fields. v[1] are the patches
        # actually it usually iterates once, but just to be sure;
        objs = [k for (k, v) in self.objects.items() if field in v[0]]
        for obj in objs:
            self.rm_obj(obj)
            self.spawn_food()

    def update(self, obj: GameObject):
        """Remove depreciated object and locate the fresh one"""
        self.rm_obj(obj)
        self.add_obj(obj)

    def can_move(self, field: tuple) -> bool:
        """Check if the given point isn't beyond the border and if it's not,
        check if it isn't occupied"""
        x, y = field
        if not ((0 <= x < self.width) & (0 <= y < self.height)):
            return False
        if self.fields[y][x] not in [self.EMPTY, 'F']:
            return False
        return True

    def print_asc(self):
        """Nicely print the board in the terminal"""
        border = '+' + ' - '*self.l + '+'
        print(border)
        for row in self.fields:
            print(' '.join(field for field in row))
        print(border)

