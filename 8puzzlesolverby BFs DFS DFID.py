from collections import deque
import time
from memory_profiler import memory_usage
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

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
        """Check if the puzzle is solvable using inversion count."""
        flattened = flatten(state)
        inversions = 0
        for i in range(len(flattened)):
            for j in range(i + 1, len(flattened)):
                if flattened[i] and flattened[j] and flattened[i] > flattened[j]:
                    inversions += 1
        return inversions % 2 == 0

    def find_space(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    return (i, j)

    def find_moves(self, pos):
        x, y = pos
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def is_valid(self, move):
        """Check if a move is within the puzzle bounds."""
        return 0 <= move[0] < 3 and 0 <= move[1] < 3

    def play_move(self, node, move, space):
        new_state = [row[:] for row in node.state]
        x, y = move
        x1, y1 = space
        new_state[x][y], new_state[x1][y1] = new_state[x1][y1], new_state[x][y]
        #print("previous")
        #print(state)
        #print("new")
        #print(new_state)
        return Node(new_state, parent=node)

    def generate_children(self, node):
        """Generate valid children nodes."""
        children = []
        space = self.find_space(node.state)
        for move in self.find_moves(space):
            if self.is_valid(move):
                children.append(self.play_move(node, move, space))
        return children
    
    def solve_puzzle_dfs(self):
        open_list = [self.start]
        closed_list = set()
        nodes=0
        while open_list:
            cs = open_list.pop() 
            nodes=nodes+1
            if cs.state == self.goal:
                return ("Number of nodes",nodes)
                #return self.disp_path(cs)
            state_tuple = tuple(map(tuple, cs.state))
            if state_tuple in closed_list:
                continue 
            closed_list.add(state_tuple)  
            children = self.generate_children(cs)
            open_list.extend(children)
        return "FAIL" 
    def solve_puzzle_bfs(self):
        open_list = [self.start]
        closed_list = set()
        nodes_visited=0
        while open_list:
            cs = open_list.pop(0) 
            nodes_visited=nodes_visited+1
            if cs.state == self.goal:
                self.disp_path(cs)
                print("number of nodes",nodes_visited)
                return True
            state_tuple = tuple(map(tuple, cs.state))
            if state_tuple in closed_list:
                continue 
            closed_list.add(state_tuple)  
            children = self.generate_children(cs)
            open_list.extend(children)
        return "FAIL"  
    def disp_path(self, final_node): #for dfs,bfs
        if not final_node:
            return False
        path = []
       
        while final_node:
            path.append(final_node)
            final_node = final_node.parent
        
        print("Number of moves",len(path))
        path.reverse() 
        moves=0
        for state in path:
            print(state)
            moves=moves+1
        print("NUMber of moves",moves)
    def dfid(self, max_depth):
        total_nodes_visited = 0  # Counter for total nodes expanded

        for depth in range(max_depth):  # Increase depth limit step by step
            closed = set()  # Reset visited states for the current depth limit
            nodes_visited_at_depth = 0  # Counter for this depth iteration

            result, nodes_visited_at_depth = self.dls(self.start, depth, closed, 0)  

            total_nodes_visited += nodes_visited_at_depth  # Accumulate total nodes visited

            if result:  # If a solution is found
                 # Count number of moves
                print(f"Solution found at depth {depth}")
                print(f"Total nodes visited: {total_nodes_visited}")
                #print(f"Number of moves: {moves}")
                return self.disp_path(result), total_nodes_visited  # Return solution, nodes visited, moves

        return "FAIL", total_nodes_visited # If no solution is found

    def dls(self, node, limit, closed, nodes_visited):
        nodes_visited += 1  # Increment count when visiting a node

        if node.state == self.goal:
            return node, nodes_visited  # Return goal node and count
        
        if limit <= 0:
            return None, nodes_visited  # Stop if depth limit is reached

        closed.add(tuple(map(tuple, node.state)))  # Mark node as visited

        for child in self.generate_children(node):
            if tuple(map(tuple, child.state)) not in closed:  # Avoid revisiting in this depth limit
                child.parent = node  # Store parent for backtracking
                result, new_nodes_visited = self.dls(child, limit - 1, closed, nodes_visited)
                nodes_visited = new_nodes_visited  # Update total count
                if result:
                    return result, nodes_visited  # Return solution

        return None, nodes_visited  # Return if no solution found



    
    def dfid1(self, max_depth):
        total_nodes_visited = 0  # Counter for total nodes expanded

        for depth in range(max_depth):  # Increase depth limit step by step
            closed = set()  # Reset visited states for the current depth limit
            nodes_visited_at_depth = [0]  # List to hold count (mutable to update inside recursion)
            
            result = self.dls1(self.start, depth, closed, nodes_visited_at_depth)  

            total_nodes_visited += nodes_visited_at_depth[0]  # Accumulate total nodes visited

            if result:  # If a solution is found
                #moves = self.count_moves(result)  # Count number of moves
                print(f"Solution found at depth {depth}")
                print(f"Total nodes visited: {total_nodes_visited}")
                #print(f"Number of moves: {moves}")
                return self.disp_path(result), total_nodes_visited# Return solution, nodes visited, moves

        return "FAIL", total_nodes_visited, -1  # If no solution is found

    def dls1(self, node, limit, closed, nodes_visited_at_depth):
        nodes_visited_at_depth[0] += 1  # Increment count when visiting a node

        if node.state == self.goal:
            return node  # Return goal node
        
        if limit <= 0:
            return None  # Stop if depth limit is reached

        closed.add(tuple(map(tuple, node.state)))  # Mark node as visited

        for child in self.generate_children(node):
            if tuple(map(tuple, child.state)) not in closed:  # Avoid revisiting in this depth limit
                child.parent = node  # Store parent for backtracking
                result = self.dls1(child, limit - 1, closed, nodes_visited_at_depth)
                if result:
                    return result  # Return solution

        return None  # Return if no solution found



    def disp_solution(self, final_state):
        opposite = [n for n in final_state if n is not None]
        for i in range(len(opposite)-1,-1,-1):
            print(opposite[i])
    
def main():
    start_state = [[4, 7, 8], [3, 6, 5], [1, 2, 0]]
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    start_node = Node(start_state)
    solver = PuzzleSolver(start=start_node, goal=goal_state)

    
       
        
    
   
main()

