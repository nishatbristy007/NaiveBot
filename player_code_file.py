import time
import random
import sys
from timeit import default_timer as timer

grid_size = 8
maxdepth = 10
start = 0
timetostop = 2.9
def get_no_neighbour(i, j, len):
    if (i == 0 or i == len) and (j == 0 or j == len):
        return 2
    elif i == 0 or j == 0 or i == len or j == len:
        return 3
    else:
        return 4

def copyboard(board):
    newboard=[]
    for i in range(8):
        newrow = []
        for j in range(8):
            newrow.append(board[i][j])
        newboard.append(newrow)
    return newboard

class Node:
    def __init__(self,board,player_color):
        self.board =  board
        self.children =  []
        self.player_color =  player_color
        self.utility = -99999
        self.i = -1
        self.j = -1
        self.map = str(''.join(str(f) for e in self.board for f in e))

    def __lt__(self, other):
        return self.utility > other.utility
    def __hash__(self):
        return hash(self.map)

    def getChildren(self):
        successor  = []
        for i in range(8):
            for j in range(8):
                copy = copyboard(self.board)
                if self.board[i][j][0] == self.player_color and (int(self.board[i][j][1]) >= get_no_neighbour(i,j,7)-1):
                    #Explosion
                    copy[i][j] = str('No')
                    if i-1 >=0:
                        if copy[i-1][j]=='No':
                            copy[i-1][j] = str('R0')
                        copy[i-1][j] = str(self.player_color) + str(int(copy[i-1][j][1]) + 1)
                    if i+1<=7:
                        if copy[i+1][j]=='No':
                            copy[i+1][j] = str('R0')
                        copy[i + 1][j] = str(self.player_color) + str(int(copy[i + 1][j][1]) + 1)
                    if j-1 >=0:
                        if copy[i][j-1]=='No':
                            copy[i][j-1] = str('R0')
                        copy[i][j -1] = str(self.player_color) + str(int(copy[i][j-1][1]) + 1)
                    if j+1 <=7:
                        if copy[i][j+1]=='No':
                            copy[i][j+1] = str('R0')
                        copy[i][j+1] = str(self.player_color) + str(int(copy[i][j+1][1]) + 1)

                    if self.player_color == 'R':
                        nextPlayer = 'G'
                    else:
                        nextPlayer = 'R'
                    potentialChild = Node(copy, nextPlayer)
                    potentialChild.i = i
                    potentialChild.j = j
                    potentialChild.utility = naive_heuristic(potentialChild.board, potentialChild.player_color)
                    # print(naive_heuristic(potentialChild.board,potentialChild.player_color))
                    successor.append(potentialChild)
                    self.children.append(potentialChild)
                elif self.board[i][j][0] == self.player_color and (int(self.board[i][j][1]) < get_no_neighbour(i,j,7)):
                    copy[i][j] = str(self.player_color)+str(int(copy[i][j][1]) + 1)
                    if self.player_color == 'R':
                        nextPlayer = 'G'
                    else:
                        nextPlayer = 'R'
                    potentialChild = Node(copy, nextPlayer)
                    potentialChild.i = i
                    potentialChild.j = j
                    potentialChild.utility = naive_heuristic(potentialChild.board, potentialChild.player_color)
                    # print(naive_heuristic(potentialChild.board,potentialChild.player_color))
                    successor.append(potentialChild)
                    self.children.append(potentialChild)
        return successor



class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search

    def __init__(self, game_tree):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.board  # GameNode
        return

    def iterative_deepening(self,node):
        global start
        global timetostop
        start =  timer()
        wentto = 0
        for i in range(maxdepth):
            bestmove = self.alpha_beta_search(node, i)
            if((timer()-start)>=timetostop):
                wentto = i
                break
        return bestmove




    def alpha_beta_search(self, node,depth):
        global maxdepth
        global timetostop
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors = self.getSuccessors(node)
        successors.sort()

        best_state = None
        for state in successors:
            value = self.min_value(depth,state, best_val, beta)
            if value > best_val or (timer()-start)>=timetostop:
                best_val = value
                best_state = state
        return best_state

    def max_value(self, depth,node, alpha, beta):
        global maxdepth
        global timetostop
        #print("AlphaBeta-->MAX: Visited Node :: " , node.board)
        if depth == maxdepth  or ((timer()-start)>timetostop):
            return node.utility
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node)
        successors.sort()

        for state in successors:
            value = max(value, self.min_value(depth+1,state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self,depth, node, alpha, beta):
        global maxdepth
        global timetostop
       # print("AlphaBeta-->MIN: Visited Node :: " , node.board)
        if depth == maxdepth  or ((timer()-start)>timetostop):
            return node.utility
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        successors.sort()

        for state in successors:
            value = min(value, self.max_value(depth+1,state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node):
        return node.getChildren()

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        return len(node.children) == 0

    def getUtility(self, node):
        return naive_heuristic(node.board,node.player_color)

def read_file(player_color):
    with open("shared_file.txt") as f:
        lines = f.readlines()
    if len(lines) == 0:
        return None
    if lines[0].strip('\n') == str(player_color):
        temp_grid = []
        for line in lines[1:]:
            temp_grid.append(line.strip('\n').split(" "))

        return temp_grid

    return None



def naive_heuristic(grid,player_color):
    myplaces = 0
    hisplaces = 0
    explosive = 0
    for i in range(8):
        for j in range(8):
            neighbour = get_no_neighbour(i,j,len(grid)-1)
            if grid[i][j][0] == player_color:
                myplaces = myplaces + 1
                if int(grid[i][j][1])==neighbour-1 :
                    explosive = explosive + 1
            elif grid[i][j] != 'No' and grid[i][j][0]!=player_color :
                hisplaces = hisplaces + 1
                if int(grid[i][j][1]) == neighbour-1:
                    explosive = explosive - 1
    tempo = []
    tempo.append(myplaces)
    tempo.append(hisplaces)
    return myplaces - hisplaces +explosive
    return tempo

#================================================================================================
#           NEW HEURISTIC
#================================================================================================
def neighbours(board,i,j):
    neighbours = []
    if i-1>=0 :
        neighbours.append([i-1,j])
    if i+1<=7:
        neighbours.append([i+1,j])
    if j-1>=0:
        neighbours.append([i,j-1])
    if j+1<=7:
        neighbours.append([i,j+1])
    return neighbours

def critical_mass(board,i,j):
    return len(neighbours(board,i,j))

def a_better_heuristic(board, player_color):
    sc = 0
    my,his = 0,0

    if player_color == 'R':
        opponent_color = 'G'
    else:
        opponent_color = 'R'

    for pos in [[x, y] for x in range(8) for y in range(8)]:
        if board[pos[0]][pos[1]][0] == player_color:
            my = my + int(board[pos[0]][pos[1]][1])
            flag = True
            for i in neighbours(board,pos[0],pos[1]):
                if board[i[0]][i[1]][1] == opponent_color and int(board[i[0]][i[1]]) == critical_mass(board,i[0],i[1]) -1 :
                    sc = sc - (5 - critical_mass(board,pos[0],pos[1]))
                    flag = False
                if flag :
                    if critical_mass(board,pos[0],pos[1]) == 3 :
                        sc = sc+2
                    elif critical_mass(board,pos[0],pos[1]) == 2:
                        sc = sc + 3
                    if int(board[pos[0]][pos[1]][1]) == critical_mass(board,pos[0],pos[1]) -1 :
                        sc =  sc + 2
        elif board[pos[0]][pos[1]][0] == opponent_color:
                    his = his + int(board[pos[0]][pos[1]][1])
            # The number of Orbs Heuristic
        sc = sc + my
            # You win when the enemy has no orbs
        if his == 0 and my > 1:
            return 10000
            # You loose when you have no orbs
        elif my == 0 and his > 1:
                return -10000
            # The chain Heuristic
        sc += sum([2 * i for i in chains(board, player_color) if i > 1])
        return sc

def chains(board2,player):
    board = copyboard(board2)
    lengths = []
    for pos in [[x,y] for x in range(8) for y in range(8)]:
        if board[pos[0]][pos[1]][0] == player and int(board[pos[0]][pos[1]][1]) == (critical_mass(board,pos[0],pos[1]) - 1) :
            l = 0
            visiting_stack = []
            visiting_stack.append(pos)
            while visiting_stack:
                pos = visiting_stack.pop()
                board[pos[0]][pos[1]] = 'No'
                l += 1
                for i in neighbours(board,pos[0],pos[1]):
                    if board[i[0]][i[1]][0] == player and int(board[i[0]][i[1]][1] == critical_mass(board,i[0],i[1]) - 1):
                        visiting_stack.append(i)
            lengths.append(l)
    return lengths

#================================================================================================
#           NEW HEURISTIC
#================================================================================================


def select_move(x,y,grid,player_color,count):#grid, player_color):
    while True:
    #    x = random.randint(0, 7)
    #    y = random.randint(0, 7)

        if (grid[x][y] == 'No' or grid[x][y][0] == player_color) and count <5:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if grid[x][y] == 'No' or grid[x][y][0] == player_color:
                return x, y
            else:
                continue
            #        return x, y

        elif grid[x][y] == 'No' or grid[x][y][0] == player_color:
            return x,y
        else :
            x = random.randint(0, 7)
            y = random.randint(0, 7)

def write_move(move):
    str_to_write = '0\n' + str(move[0]) + " " + str(move[1])
    with open("shared_file.txt", 'w') as f:
        f.write(str_to_write)

def printgrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j],end == ' ')
        print("\n")

def main():
    player_color = sys.argv[1]
    count = 0
    while True:

        while True:
        # grid = read_file(player_color)
            if count >=100:
                count = 2
            grid = read_file(player_color)
            if grid is None:
                break
            heu = naive_heuristic(grid,player_color)

            time.sleep(.01)
            if count <= 5 :
                move = select_move(0, 0, grid, player_color, count)  # grid, player_color)

                write_move(move)
                count =  count +1
                continue
            node = Node(grid,player_color)
            a = AlphaBeta(node)
            movenode = a.iterative_deepening(node)
            node.getChildren()
            count =  count+1
            move = select_move(movenode.i,movenode.j,grid,player_color,count)#grid, player_color)

            write_move(move)


if __name__ == "__main__":
    main()