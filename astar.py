from Map import Map_Obj
from enum import Enum

cost = {' . '}


class Status(Enum):  # currently not used
    OPEN = 1
    CLOSED = 2


class State:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def __eq__(self, other):
        return other.coordinates[0] == self.coordinates[0] and other.coordinates[1] == self.coordinates[1]

    def __ne__(self, other):
        if (other == None):
            return True
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.coordinates)

    def __str__(self):
        return str(self.coordinates)

    def __repr__(self):
        return str(self.coordinates)


class Node:
    def __init__(self, state):
        self.state = state  # The state property of a search node is a representation of a particular configuration of the problem being solved
        # list of all successor nodes, whether or not this node is currently their best parent.
        self.childs = []
        # self.g = g  # cost of getting to this node
        # self.h = h  # estimated cost to goal
        # self.f = g + h
        # self.status = status  # open or closed
        self.parent = None  # best parent

        self.g = 0
        self.h = 0
        self.f = 0

    def __ne__(self, other):
        if (other == None):
            return True
        return not self.__eq__(other)

    # TODO: Make sure this is correct
    def __eq__(self, other):
        return self.state == other.state and self.g == other.g and self.h == other.h and self.f == other.f

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return f'Coordinates of state: {str(self.state)} g: {self.g} h: {self.h} f: {self.f}'


class BestSearchFirst():

    def __init__(self, task=1):
        self.open = []  # Sorted by ascending f values, nodes with lot of promise popped early, contains unexpanded nodes
        self.closed = []  # no order, contains expanded nodes
        self.map = Map_Obj(task)
        self.nodes = []
        self.goal = State(tuple(self.map.get_goal_pos()))  # for task 1-2
        self.current_state = State(tuple(self.map.get_start_pos()))

        self.root_node = Node(self.current_state)
        self.root_node.g = 0
        self.heuretic_evaluation(self.root_node)
        self.root_node.f = self.root_node.g + self.root_node.h

        self.open.append(self.root_node)
        self.solution_node = None

    def arc_cost(self, p, c):
        """ This calculates the arc cost between two nodes (parent and child) """
        return self.map.get_cell_value(c.state.coordinates)

    def propagate_path_improvements(self, p):
        for c in p.childs:
            if p.g + self.arc_cost(p, c) < c.g:
                c.parent = p
                c.g = p.g + self.arc_cost(p, c)
                c.f = c.g + c.h
                self.propagate_path_improvements(c)

    def agenda_loop(self):
        """ Agenda loop """

        solution = False
        iterations = 0
        while not solution:
            if not self.open:
                print("Something definitely went wrong!")
                return False
            x = self.open.pop()
            self.closed.append(x)
            solution_state = None
            if self.check_solution(x):
                solution = True
                self.solution_node = x
            else:
                successors = self.generate_successor_nodes(x)

                for s in successors:
                    in_open = False
                    in_closed = False
                    if s in self.open:
                        in_open = True
                        s_star = self.open[self.open.index(s)]
                        if s.state == s_star.state:
                            s = s_star
                    elif s in self.closed:
                        in_closed = True
                        s_star = self.closed[self.closed.index(s)]
                        if s.state == s_star.state:
                            s = s_star
                    x.childs.append(s)
                    if not in_open and not in_closed:
                        self.attach_and_eval(s, x)
                        self.open.append(s)
                        self.open = sorted(
                            self.open, key=lambda val: val.f, reverse=True)
                    elif x.g + self.arc_cost(x, s) < s.g:  # found cheaper path to s
                        self.attach_and_eval(s, x)
                        if in_closed:
                            self.propagate_path_improvements(s)

            iterations += 1
        return solution, solution_state

    def create_state_identifier(state):
        return None

    def attach_and_eval(self, c, p):
        """ simply attaches a child node to a node that is now considered its best parent (so far) """
        c.parent = p
        c.g = p.g + self.arc_cost(p, c)
        self.heuretic_evaluation(c)
        c.f = c.g + c.h

    def generate_successor_nodes(self, node):
        """ Given a node in the search tree this generates all possible succesor states to the node's state """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        successor_nodes = []

        for i in directions:
            x = node.state.coordinates[0]+i[0]
            y = node.state.coordinates[1]+i[1]
            value = self.map.get_cell_value((x, y))
            if value != -1:
                state = State((x, y))
                child = Node(state)
                self.heuretic_evaluation(child)
                child.g = node.g + self.arc_cost(node, child)
                child.f = child.g + child.h
                successor_nodes.append(child)
                self.nodes.append(child)
        return successor_nodes

    def heuretic_evaluation(self, node):
        """ Gives a heuretic evaluation of the distance to the goal using manhattan distance  """
        heuretic = abs(self.goal.coordinates[0]-node.state.coordinates[0]) + abs(
            self.goal.coordinates[1]-node.state.coordinates[1])
        node.h = heuretic
        return heuretic

    def check_solution(self, node):
        """ Compares the state of the nodes to the goal state """
        return node.state == self.goal

    def print_solution(self):
        child = self.solution_node
        parent = self.solution_node.parent
        solution_list = [self.solution_node.state.coordinates]

        print(self.solution_node)
        while parent != None:
            solution_list.append(parent.state.coordinates)
            print(parent)
            child = parent
            parent = child.parent
        self.map.show_solution(solution_list)


if __name__ == "__main__":
    astar = BestSearchFirst(4)
    found_solution, solution = astar.agenda_loop()
    # astar.map.print_map()
    print(found_solution)
    astar.print_solution()
