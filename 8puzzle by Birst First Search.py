import heapq
import time 
from copy import deepcopy
from memory_profiler import memory_usage
class PriorityQueue:
    def __init__(self):
        self.q = []
    
    def enqueue(self, node):
        heapq.heappush(self.q, (node.h, node))

    def dequeue(self):   
        if not self.is_empty():     
            return heapq.heappop(self.q)[1]
        
    def is_empty(self):
        return len(self.q) == 0

def dictionaryy(lst):
    coordinate_dict = {}
    for x, row in enumerate(lst):
        for y, value in enumerate(row):
            if value not in coordinate_dict: 
                coordinate_dict[value] = (x, y)  
    return coordinate_dict

class Node:
    def __init__(self, state, goal, parent=None):
        self.state = state
        self.parent = parent
        self.h = self.heuristic(goal)

    def __lt__(self, other):
        return self.h < other.h

    def heuristic(self, goal):
        value = 0
        state_dict = dictionaryy(self.state)
        goal_dict = dictionaryy(goal)
       
        for key in state_dict:
            if key!=" ":
               
                value += abs(state_dict[key][0] - goal_dict[key][0]) + abs(state_dict[key][1] - goal_dict[key][1])
        
        return value 

    def __str__(self):
        if not hasattr(self, "state") or not isinstance(self.state, list):
            return "Invalid Node"
        result = ''
        for row in self.state:
            result += ' '.join(map(str, row)) + '\n'
        return result

    def __repr__(self):
        return self.__str__()

def flatten(state):
    return [num for row in state for num in row]

class PuzzleSolver:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def is_solvable(self, state):
        
        flattened = flatten(state)
        inversions = 0
        for i in range(len(flattened)):
            for j in range(i + 1, len(flattened)):
                if flattened[i] != " " and flattened[j] != " " and flattened[i] > flattened[j]:
                    inversions += 1
        return inversions % 2 == 0

    def find_space(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == " ":
                    return (i, j)

    def find_moves(self, pos):
        x, y = pos
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def is_valid(self, move):
        
        return 0 <= move[0] < 3 and 0 <= move[1] < 3

    def play_move(self, node, move, space):
        
        new_state = [row[:] for row in node.state]
        x, y = move
        x1, y1 = space
        new_state[x][y], new_state[x1][y1] = new_state[x1][y1], new_state[x][y]
        return Node(new_state, self.goal, parent=node)  

    def generate_children(self, node):
        
        children = []
        space = self.find_space(node.state)
        for move in self.find_moves(space):
            if self.is_valid(move):
                children.append(self.play_move(node, move, space))
        return children

    def best_first_search(self):
        pq = PriorityQueue()
        pq.enqueue(self.start)
        path = []
        close = set()
        nodes_visited=0
        if not self.is_solvable(self.start.state):
            return "Not solvable"
        while not pq.is_empty():
            children = []
            node = pq.dequeue()
            nodes_visited+=1
            if node.state == self.goal:
                while node:
                    path.append(node)  
                    node = node.parent

                print("Number of nodes",nodes_visited)
                return path[::-1]
            children = self.generate_children(node)
            for child in children:
                state_tuple = tuple(map(tuple, child.state))  
                if state_tuple not in close:
                    close.add(state_tuple)
                    pq.enqueue(child)

        #return "Goal not found"

    def print_solution(self, path):
        print("number of moves:")
        print(len(path))
        move=1
        for state in path:
            print("Move no :" ,move)
            print(state)
            move+=1
def main():
    goal = [[1, 2, 3], [4, 5, 6], [7,8, " "]]
    ps = PuzzleSolver(Node([[4, 7, 8], [3, 6, 5], [1, 2, " "]], goal), goal)
    solution = ps.best_first_search()
    if solution:
        ps.print_solution(solution)  
    else:
        print("solution not exist") 
main()

