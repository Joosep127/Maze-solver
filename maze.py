import copy
import math

class Maze():
    def __init__(self, name):
        self.board = self.Init_Board(name)
        self.goal = self.Find_Goal(self.board)
        self.frontier = WeightedFrontier(self.Node(self.board, None, self.Actions))
        self.seen = [self.board]

    def Init_Board(self, file_name):
        board = []
        try:
            with open(file_name, "r") as f:
                for i in f:
                    board.append(list(i.replace("\n", "")))
                    
        except:
            raise Exception("Couldn't Find The File")
        
        return(board)

    def Find_Goal(self, board):
        return [[x.replace("A", " ").replace("B", "A") for x in i ] for i in board ]

    def Do_Action(self, board, action):
        player = self.Find_Player_Pos(board)
        temp_board = copy.deepcopy(board)
        temp_board[player[1]][player[0]] = " "
        a,b = 0,0
        if action == 1:
            a+=1
        elif action == 2:
            a-=1
        elif action == 3:
            b+=1
        else:
            b-=1
        temp_board[player[1]-a][player[0]+b] = "A"
        return(temp_board)
    
    def Find_Player_Pos(self, board):
        player_pos = None
        for y, j in enumerate(board):
            for x, i in enumerate(j):
                if i == "A":
                    player_pos = (x, y)
                    break
            if player_pos:
                break
            
        if player_pos == None:
            print(board)
            raise Exception("No player in maze.")
        
        return(player_pos)
    
    def Actions(self, board):
        player_pos = self.Find_Player_Pos(board)
        actions = []
        max_y = len(board) - 1
        max_x = len(board[0]) - 1

        if player_pos[1] != 0 and board[player_pos[1]-1][player_pos[0]] != "#":
                actions.append(1)
        if player_pos[1] != max_y and board[player_pos[1]+1][player_pos[0]] != "#":
            actions.append(2)

        if player_pos[0] != max_x and board[player_pos[1]][player_pos[0]+1] != "#":
            actions.append(3)
        if player_pos[0] != 0 and board[player_pos[1]][player_pos[0]-1] != "#":
            actions.append(4)

        return(actions)

    class Node():
        def __init__(self, state, parent_node, Actions_func):
            self.state = state
            self.parent = parent_node
            self.actions = Actions_func(state)
            self.weight = self.Weight_SmartBiased()

        def Find_x(self, board, X):
            player_pos = None
            for y, j in enumerate(board):
                for x, i in enumerate(j):
                    if i == X:
                        player_pos = (x, y)
                        break
                if player_pos:
                    break
            if player_pos == None:
                if X == "B":
                    player_pos = self.Find_x(board, "A")
                else:
                    raise Exception(f"No letter such as '{X}' in the Maze")
            
            return(player_pos)

        def Find_Distance_from_B(self, Bpos, Squarepos):
            return math.sqrt(((Bpos[1] - Squarepos[1]) ** 2 + (Bpos[0] - Squarepos[0]) ** 2))
        
        def Steps_away_from_Start(self):
            it = 0
            temp_parent = copy.deepcopy(self.parent)
            while temp_parent:
                it += 1
                temp_parent = temp_parent.parent
            return(it)
        
        def Weight_Biased(self):
            return(self.Find_Distance_from_B(self.Find_x(self.state, "B"), self.Find_x(self.state, "A")))
        
        def Weight_SmartBiased(self):
            """A* Algorithm."""
            return(self.Weight_Biased() + self.Steps_away_from_Start())

    def find_action(self, b1, b2):
        b1, b2 = self.Find_Player_Pos(b1), self.Find_Player_Pos(b2)
        pos = (b2[0]-b1[0], b2[1]-b1[1])
        if pos == (1,0):
            return(4)
        if pos == (-1,0):
            return(3)
        if pos == (0,1):
            return(1)
        if pos == (0,-1):
            return(2)
        raise Exception("Two nonlinear boards have been submitted.")

    def solve(self):
        Complexity = 0
        while True:
            Complexity += 1
            if self.frontier.nodes == []:
                raise Exception("No solution.")
            
            temp_node = self.frontier.remove()
            if temp_node.state == self.goal:
                actions = []
                all_states = []
                while temp_node.parent:
                    actions.append(self.find_action(temp_node.state, temp_node.parent.state))
                    all_states.append(temp_node.state)
                    temp_node = temp_node.parent
                all_states.append(temp_node.state)

                actions.reverse()
                all_states.reverse()

                return(actions, Complexity, self.seen)

            for i in temp_node.actions:
                
                if self.Do_Action(temp_node.state, i) in self.seen:
                    continue
                state = self.Do_Action(temp_node.state, i)
                self.seen.append(state)
                self.frontier.add(self.Node(state, temp_node, self.Actions))


class DepthFrontier():
    def __init__(self, node):
        self.nodes = [node]
    def remove(self):
        if self.nodes == []:
            raise Exception("No solution.")
        return self.nodes.pop(-1)
    def add(self, node):
        self.nodes.append(node)
        
class QueueFrontier(DepthFrontier):
    def remove(self):
        if self.nodes == []:
            raise Exception("No nodes.")
        return self.nodes.pop(0)

class WeightedFrontier(DepthFrontier):
    def remove(self):
        if self.nodes == []:
            raise Exception("No nodes.")
        self.nodes.sort(key= lambda x: x.weight)
        return self.nodes.pop(0)


Themaze = Maze("maze.txt")
stuff = Themaze.solve()

def display_matrices(matrices):

    for idx, matrix in enumerate(matrices):
        print(f"Matrix {idx + 1}:")
        for row in matrix:
            print(" ".join(map(str, row)))
        print()

print(stuff[0])
print(stuff[1])

all_mazes = stuff[2]

FinalMaze = copy.deepcopy(Themaze.board)

cords = {"A":(), "B":()}

for y,i in enumerate(Themaze.board):
    for x,j in enumerate(i):
        if j in "AB":
            cords[j] = (y,x)
        if j in " ":
            FinalMaze[y][x] = "."

for maze in all_mazes:
    for x, rank in enumerate(maze):
        for y, tile in enumerate(rank):
            if tile == " ":
                continue
            elif tile == "#":
                FinalMaze[x][y] = "#"
            elif tile == "A":
                FinalMaze[x][y] = ","
            elif tile == "B":
                FinalMaze[x][y] = "B"
            else:
                FinalMaze[x][y] = "?"


for a , yx in cords.items():
    FinalMaze[yx[0]][yx[1]] = a



display_matrices([FinalMaze])