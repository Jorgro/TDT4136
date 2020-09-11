from Map import Map_Obj
from enum import Enum


class Status(Enum):  # currently not used
    OPEN = 1
    CLOSED = 2


class State:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.id = ??

    def __eq__(self, other):
        return other.coordinates[0] == self.coordinates[0] and other.coordinates[1] == self.coordinates[1]

    def __ne__(self, other):
        return not self.__eq__(other)


class Node:
    def __init__(self, state, g, h, status):
        self.state = state  # The state property of a search node is a representation of a particular configuration of the problem being solved
        self.parents = []
        # list of all successor nodes, whether or not this node is currently their best parent.
        self.childs = []
        self.g = g  # cost of getting to this node
        self.h = h  # estimated cost to goal
        self.f = g + h
        self.status = status  # open or closed
        self.parent = None  # best parent

    def __ne__(self, other):
        return True

    def __eq__(self, other):
        return True


class BestSearchFirst():

    cost = 1

    def __init__(self):
        self.open = []  # Sorted by ascending f values, nodes with lot of promise popped early, contains unexpanded nodes
        self.closed = []  # no order, contains expanded nodes
        self.map = Map_Obj()
        self.nodes = {}
        self.current_state = tuple(self.map.get_start_pos())
        print(self.current_state)
        self.g[self.current_state] = 0
        self.h[self.current_state] = self.heuretic_function()
        self.f[self.current_state] = self.g[self.current_state] + \
            self.h[self.current_state]
        self.closed.append(self.current_state)

    def agenda_loop(self):
        """ Agenda loop """

        solution = False

        while not solution:
            if not open:
                return False
            x = self.open.pop()
            self.closed.append(x)

            if self.check_solution(x):
                solution = True
            else:
                successors = self.generate_successor_states(x)
                in_open = False
                in_closed = False
                for s in successors:
                    if s in self.open:
                        in_open = True
                        s_star = self.open[self.open.index(s)]
                        if s.state == s_star.state:
                            s = s_star

                    elif s in self.closed:
                        in_closed = True
                        s_star = self.open[self.open.index(s)]
                        if s.state == s_star.state:
                            s = s_star
                    x.childs.append(s)
                    if not in_open and not in_closed:
                        self.attach_and_eval(s, x)
                        self.open.append(s)
                        self.open = sorted(
                            self.open, key=lambda val: val.f, reverse=True)
                            print(self.open)
                    elif:

    def propagate_path_improvements(p):
        for c in p.childs:
            if p.g + arc_cost(p, c) < c.g:
                c.parent = p
                c.g = p.g + arc_cost(p, c)
                c.f = c.g + c.h
                propagate_path_improvements(c)

    def create_state_identifier(state):
        return None

    def attach_and_eval(self, child, parent):
        """ simply attaches a child node to a node that is now considered its best parent (so far) """
        child.parent = parent
        c.g = p.g + self.arc_cost(parent, child)
        self.heuretic_evaluation(c)
        c.f = c.g + c.h

    def arc_cost(p, c):
        """ This calculates the arc cost between two nodes (parent and child) """
        return 1
   def generate_successor_states(self, node):
        """ Given a node in the search tree this generates all possible succesor states to the node's state """
        return True

    def heuretic_evaluation(self, node):
        """ Gives a heuretic evaluation of the distance to the goal  """

        node.h = 1
        return 1

    def check_solution(self):
        """ Compares the state of the nodes to the goal state """
        return True

    def create_root_node(self):
        """ This creates the initial search state and incorporates it into a node
object that becomes the root of the search tree """
        return True


if __name__ == "__main__":
    astar = BestSearchFirst()
    print(astar.f)
