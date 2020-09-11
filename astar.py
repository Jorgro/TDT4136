from Map import Map_Obj
from enum import Enum


class Status(Enum):
    OPEN = 1
    CLOSED = 2


class Node:
    def __init__(self, state, g, h, status):
        self.state = state
        self.parents = []
        self.g = g
        self.h = h
        self.f = g + h
        self.status = status

    def add_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        self.child = child


class Astar():

    cost = 1

    def __init__(self):
        self.open = []  # Sorted by ascending f values, nodes with lot of promise popped early, contains unexpanded nodes
        self.closed = []  # no order, contains expanded nodes
        self.h = {}
        self.g = {}
        self.f = {}
        self.map = Map_Obj()
        self.current_state = tuple(self.map.get_start_pos())
        print(self.current_state)
        self.g[self.current_state] = 0
        self.h[self.current_state] = self.heuretic_function()
        self.f[self.current_state] = self.g[self.current_state] + \
            self.h[self.current_state]
        self.closed.append(self.current_state)
    # def agenda_loop():

    def heuretic_function(self):
        return 1


if __name__ == "__main__":
    astar = Astar()
    print(astar.f)
