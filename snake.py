#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Just a snake class.
It protecc
It attacc
But most importantly
It knows how to find a snacc
(todo: or will know soon)
"""


class Snake(GameObject):
    def __init__(self, board: Board, callback_end: Callable):
        self.fields = [(2, 5),
                (3, 5),
                (4, 5),
                (5, 5),
                (6, 5),
                (7, 5)]
        self.orientation = 0  # 0, 1, 2, 3 == N, E, W, S
        self.speed = 1  # how many fields it moves in 1 turn
        self.callback_end = callback_end

        def foo(*args):
            pass

        self.actions = {
                0: foo,
                'S': foo,
                'F': self.feed,
                }

        super().__init__(board=board, char='S', color='r', fields=self.fields)

    def new_field(self) -> tuple:
        """
        Calculate the new positon of the snake's head
        if it's gonna make a move
        """
        head_x, head_y = self.fields[-1]
        dx, dy = [(0, 1), (1, 0), (0, -1), (-1, 0)][self.orientation]
        dx *= self.speed
        dy *= self.speed
        return head_x + dx, head_y + dy

    def set_orientation(self, orient: int) -> bool:
        """
        Check if the direction is legal, if it is - turn snake and
        return True, otherwise do nothing and return False
        """
        assert 0 <= orient < 4

        if {self.orientation, orient} in [{0, 2}, {1, 3}]:  # cant turn 180 deg
            return False

        self.orientation = orient
        return True

    def kill(self):
        """
        Game over
        """
        self.callback_end()

    def manage_events(self):
        """
        Catch up with what's going on on the board. If the snake has hit some food
        or something, do what should have been done
        """
        events = [self.board.fields[y][x] for (x, y) in self.fields]
        for i in events:
            self.actions[i]()

    def feed(self):
        """
        Find in which direction is the tail is going and get the field behind
        Diff betwen pre-tail and tail gotta be same as tail and post-tail
        """
        tail_x, tail_y = self.fields[0]
        pretail_x, pretail_y = self.fields[1]
        dx, dy = pretail_x - tail_x, pretail_y - tail_y

        post_tail = self.fields[0][0] + dx, self.fields[0][1] + dy
        self.fields.insert(0, post_tail)
        self.board.rm_food(self.fields[-1])
        self.board.update(self)

    def move(self) -> bool:
        """
        Calculate the new snake head's position, check
        if the movement is legal and then lose the tail and
        add new head_pos to the body; if isn't legal, game over
        """
        new = self.new_field()

        if not self.board.can_move(new):
            self.kill()
            return False

        self.fields = self.fields[1:] + [new]  # the actual movement

        # the tail becomes the head - no need to refresh every patch
        # self.patches[0].set_xy(new)
        # self.patches = self.patches[1:] + [self.patches[0]]

        self.manage_events()
        self.board.update(self)
        return True

