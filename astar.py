from Map import Map_Obj
from enum import Enum


class State:
    def __init__(self, coordinates):
        # the coordinates in the map is used as a state for a given node in the search tree
        self.coordinates = coordinates

    def __eq__(self, other):
        """ Used to compare two States (or other) using == op """

        return other.coordinates[0] == self.coordinates[0] and other.coordinates[1] == self.coordinates[1]

    def __ne__(self, other):
        """ Used to compare two States (or other) using != op """

        if (other == None):
            return True
        return not self.__eq__(other)

    def __str__(self):
        """ String representation of a State using the coordinates"""

        return str(self.coordinates)

    def __repr__(self):
        """ Used to print a State using the coordinates"""

        return str(self.coordinates)


class Node:
    def __init__(self, state):
        self.state = state  # The state property of a search node is a representation of a particular configuration of the problem being solved
        # list of all successor nodes, whether or not this node is currently their best parent.
        self.childs = []
        self.parent = None  # best parent

        self.g = 0  # cost of getting to this node
        self.h = 0  # estimated cost to goal
        self.f = 0  # sum of both above

    def __ne__(self, other):
        """ Used to compare two Nodes (or other) using != op """

        if (other == None):
            return True
        return not self.__eq__(other)

    def __eq__(self, other):
        """ Used to compare two Nodes (or other) using == op """

        return self.state == other.state and self.g == other.g and self.h == other.h and self.f == other.f

    def __str__(self):
        """ String representation of a node """
        return str(self.state)

    def __repr__(self):
        """ Used to represent a node whenever it is printed (for debug purposes) """
        return f'Coordinates of state: {str(self.state)} g: {self.g} h: {self.h} f: {self.f}'


class BestSearchFirst:

    def __init__(self, task=1):
        self.state_dictionary = {}

        self.open = []  # Sorted by ascending f values, nodes with lot of promise popped early, contains unexpanded nodes
        self.closed = []  # no order, contains expanded nodes
        self.map = Map_Obj(task)  # the map
        # creates a new state with coordinates of the goal position from map
        self.goal = State(tuple(self.map.get_goal_pos()))
        # creates a new state as current state with the coordinates of the start position from map
        self.current_state = State(tuple(self.map.get_start_pos()))

        self.root_node = Node(self.current_state)  # root of the search tree
        self.root_node.g = 0
        self.heuretic_evaluation(self.root_node)
        # all of the f, g, h variables are taken from the appendix added to the task.
        self.root_node.f = self.root_node.g + self.root_node.h

        # adding the root node to the open list
        self.open.append(self.root_node)
        self.solution_node = None  # Hopefully the goal

    def arc_cost(self, p, c):
        """ This calculates the arc cost between two nodes (parent and child) using the cost of the child node (the one you are moving to)"""
        return self.map.get_cell_value(c.state.coordinates)

    def propagate_path_improvements(self, p):
        """ Goes through the children of a parent node and updates the cost of
        going to the child from the parent if it less than the current cost of going to the child.
        This is done recursively """
        for c in p.childs:
            if p.g + self.arc_cost(p, c) < c.g:
                c.parent = p
                c.g = p.g + self.arc_cost(p, c)
                c.f = c.g + c.h
                self.propagate_path_improvements(c)

    def agenda_loop(self):
        """ Agenda loop """
        it = 0
        solution = False
        while not solution:
            it += 1
            if not self.open:
                # in these tasks with obvious solutions something must be wrong with the implementation
                print("Something definitely went wrong!")
                return False
            x = self.open.pop()
            self.closed.append(x)
            solution_state = None
            if self.check_solution(x):
                solution = True
                self.solution_node = x
            else:
                # generating the successor nodes, expanding x
                successors = self.generate_successor_nodes(x)

                for s in successors:  # go through each of these children
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
                    # s is a child of x even though x might not be the best parent
                    x.childs.append(s)
                    if not in_open and not in_closed:
                        # attach the new succesor (it just got explored) with parent x
                        self.attach_and_eval(s, x)
                        self.open.append(s)  # we will expand this node later
                        self.open = sorted(
                            self.open, key=lambda val: val.f, reverse=True)
                        # sorting open list in descending based on f value, pop function takes from the back of the list
                        print(len(self.open))
                    elif x.g + self.arc_cost(x, s) < s.g:  # found cheaper path to s
                        # attaches s to a new parent x
                        self.attach_and_eval(s, x)
                        if in_closed:
                            # propagate the improved path to s through all of s children (and their children)
                            self.propagate_path_improvements(s)
        print("iter", it)
        return solution, solution_state

    def attach_and_eval(self, c, p):
        """ Simply attaches a child node to a node that is now considered its best parent (so far) """
        c.parent = p
        c.g = p.g + self.arc_cost(p, c)
        self.heuretic_evaluation(c)
        c.f = c.g + c.h

    # This should be changed, need to have a dictionary from coordinates to State
    def generate_successor_nodes(self, node):
        """ Given a node in the search tree this generates all possible succesor states to the node's state """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)
                      ]  # directions you are allowed to move in (up, right, left, down)
        successor_nodes = []  # all the successors

        for i in directions:
            x = node.state.coordinates[0]+i[0]
            y = node.state.coordinates[1]+i[1]
            if tuple((x, y)) in self.state_dictionary:
                successor_nodes.append(
                    self.state_dictionary.get(tuple((x, y))))
                print("oki")
            else:
                value = self.map.get_cell_value((x, y))
                if value != -1:  # if it isn't a wall we will add the new node and state to the successors
                    state = State((x, y))
                    child = Node(state)
                    self.state_dictionary[tuple((x, y))] = child
                    self.heuretic_evaluation(child)
                    child.g = node.g + self.arc_cost(node, child)
                    child.f = child.g + child.h
                    successor_nodes.append(child)
        return successor_nodes

    def heuretic_evaluation(self, node):
        """ Gives a heuretic evaluation of the distance to the goal using manhattan distance  """
        heuretic = abs(self.goal.coordinates[0]-node.state.coordinates[0]) + abs(
            self.goal.coordinates[1]-node.state.coordinates[1])
        node.h = heuretic
        return heuretic

    def check_solution(self, node):
        """ Compares the state of the nodes to the goal state (by comparing coordinates) """
        return node.state == self.goal

    def print_solution(self):
        """ Finds the given solution path by going through the parent of the solution node and going backwards to the root node, then shows the solution using the map """
        child = self.solution_node
        parent = self.solution_node.parent
        solution_list = [self.solution_node.state.coordinates]

        while parent != None:
            solution_list.append(parent.state.coordinates)
            child = parent
            parent = child.parent
        self.map.show_solution(solution_list)


if __name__ == "__main__":
    task = 1
    astar = BestSearchFirst(task)
    found_solution, solution = astar.agenda_loop()
    astar.print_solution()
