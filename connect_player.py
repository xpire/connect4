#given a board, we will compute using DeepLearning or AlphaBeta pruning of
#Minimax Search, to compute the best move, and return it.
#game mechanics and variables
ncol = 7
nrow = 6
connect = 4

#compute next move
def compute(board):
    #extract winning information from board


#player code
"""
def update_value(self):
    #check the state of 0s (any 4s, 3s, 2s and 1s that could potentially be winning)
    #1 check vertical
    i = 0
    print("VERTICAL")
    for k in range(ncol): #vary x
        for j in range(0,nrow-3): #vary y
            print("checking 4 in a row {} ({},{}) to ({},{})".format(i,k,j,k,j+3))
            #check
            connect_n = []
            for l in range(connect):
                connect_n.append(self.board[j+l][k])
            val = check(connect_n)
            print("connect_n:{}, val:{}".format(connect_n,val))
            i+=1
    #2 check horizontal
    print("HORIZONTAL")
    for j in range(nrow): #vary y
        for k in range(0,ncol-3): #vary x
            print("checking 4 in a row {} ({},{}) to ({},{})".format(i,k,j,k+3,j))
            #check
            connect_n = []
            for l in range(connect):
                connect_n.append(self.board[j][k+l])
            val = check(connect_n)
            print("connect_n:{}, val:{}".format(connect_n,val))
            i+=1
    #3 check diagonals
    print("DIAGONALS")
    for j in range(0,nrow-3): #vary y
        for k in range(0,ncol-3): #vary x
            print("checking 4 in a row first {} ({},{}) to ({},{})".format(i,k,j,k+3,j+3))
            #check
            connect_n = []
            for l in range(connect):
                connect_n.append(self.board[j+l][k+l])
            val = check(connect_n)
            print("connect_n:{}, val:{}".format(connect_n,val))
            i+=1
            print("checking 4 in a row second {} ({},{}) to ({},{})".format(i,k,j+3,k+3,j))
            #check
            connect_n = []
            for l in range(connect):
                connect_n.append(self.board[j+connect-1-l][k+l])
            val = check(connect_n)
            print("connect_n:{}, val:{}".format(connect_n,val))
            i+=1
    return
"""


"""
old:
import random
import sys, time
import itertools as it

#game mechanics:
#7 columns, 6 rows board. Choose one column that is not filled to put ur counter
ncol = 7
nrow = 6
connect = 4
import connect_player

#checking a connect_row given as a string, and seeing who won
def check(string):
    score = 0
    if 0 in string and 1 in string:
        pass
    else:
        for k in range(len(string)):
            if string[k] == 0:
                score -=1
            elif string[k] == 1:
                score +=1
    return score

#An instance of the game, which holds the board, (and heights), cursor position
#player, and the game's current value (denoted as a 1 for p0 win, -1 for p1 win, and inbetween)
class game(object):
    """docstring for board."""
    def __init__(self):
        super(game, self).__init__()
        self.board = [[' ' for x in range(ncol)] for y in range(nrow)]
        self.heights = [0 for x in range(ncol)]
        self.cursor = 0 #possible positions: [0,...,ncol-1]
        self.turn = 0   #the current turn
        self.player = 0 #alternates between player 0 and player 1
        self.value = 0  #1 for a win (player 0), -1 for a win (player 1)

    #show game state
    def show(self):
        print("Turn:{}, Player_{}'s move:".format(self.turn,self.player))
        print("heights:{}".format(self.heights))
        print("value:{}".format(self.value))
        for k in range(self.cursor):
            print("  ", end="")
        print(" v", end="")
        for k in range(ncol-self.cursor):
            print(" ", end="")
        print(" ")
        print("*" + "-"*(2*ncol-1) + "*")
        for y in range(nrow-1,-1,-1):
            print("|",end="")
            for x in range(ncol):
                print("{}|".format(self.board[y][x]), end="")
            print(" ")
        print("*" + "-"*(2*ncol-1) + "*")

    #sanity check for possible input of moves
    def possible(self, move):
        if move in ['l','L','r','R',' ']: #left, right, space
            return 1
        return 0

    #validity check if the current move is allowed in the game
    def valid(self, move):
        if self.possible(move):
            if move in ['l','L']:
                #move cursor left
                # if self.cursor <= 0:
                #     return 0
                # else:
                return 1
            elif move in ['r','R']:
                #move cursor right
                # if self.cursor >= nrow:
                #     return 0
                # else:
                return 1
            elif move == ' ':
                #place counter here
                if self.heights[self.cursor] >= nrow:
                    return 0
                else:
                    return 1
        return 0

    #makes the move happen
    def make_move(self, m):
        if m in ['l','L']:
            self.cursor-=1
            self.cursor = self.cursor%ncol
        elif m in ['r','R']:
            self.cursor+=1
            self.cursor = self.cursor%ncol
        else:# m == ' ':
            y = self.heights[self.cursor]
            self.board[y][self.cursor] = self.player
            self.heights[self.cursor] += 1


    #update the boards value (give an evaluation of current state of game)
    #1 for player0 win
    #-1 for player1 win
    #0 for draw
    #a fraction will give an indicator of who is more likely to win atm
    def update_value(self):
        #check the state of 0s (any 4s, 3s, 2s and 1s that could potentially be winning)
        #1 check vertical
        i = 0
        print("VERTICAL")
        for k in range(ncol): #vary x
            for j in range(0,nrow-3): #vary y
                print("checking 4 in a row {} ({},{}) to ({},{})".format(i,k,j,k,j+3))
                #check
                connect_n = []
                for l in range(connect):
                    connect_n.append(self.board[j+l][k])
                val = check(connect_n)
                print("connect_n:{}, val:{}".format(connect_n,val))
                i+=1
        #2 check horizontal
        print("HORIZONTAL")
        for j in range(nrow): #vary y
            for k in range(0,ncol-3): #vary x
                print("checking 4 in a row {} ({},{}) to ({},{})".format(i,k,j,k+3,j))
                #check
                connect_n = []
                for l in range(connect):
                    connect_n.append(self.board[j][k+l])
                val = check(connect_n)
                print("connect_n:{}, val:{}".format(connect_n,val))
                i+=1
        #3 check diagonals
        print("DIAGONALS")
        for j in range(0,nrow-3): #vary y
            for k in range(0,ncol-3): #vary x
                print("checking 4 in a row first {} ({},{}) to ({},{})".format(i,k,j,k+3,j+3))
                #check
                connect_n = []
                for l in range(connect):
                    connect_n.append(self.board[j+l][k+l])
                val = check(connect_n)
                print("connect_n:{}, val:{}".format(connect_n,val))
                i+=1
                print("checking 4 in a row second {} ({},{}) to ({},{})".format(i,k,j+3,k+3,j))
                #check
                connect_n = []
                for l in range(connect):
                    connect_n.append(self.board[j+connect-1-l][k+l])
                val = check(connect_n)
                print("connect_n:{}, val:{}".format(connect_n,val))
                i+=1
        return

#player input
def player_input():
    move = input("What Move?")
    #move = connect_player.move()
    if not move:
        return 'x' #dummy variable coz i keep accidentally not returning a value
    return move[0]

#Actual Game part:
if __name__ == "__main__":
    g = game()
    while abs(g.value) != 1:
        #get move, ask game.player for move
        g.show()
        player_move = player_input()
        if (g.valid(player_move)):
            if player_move in ['l','L','r','R']:
                g.make_move(player_move)
                continue
            pass
        else:
            print("Sorry, invalid move, try again.")
            continue
        #apply move
        g.make_move(player_move)
        #clean up
        g.player = (g.player+1)%2
        g.update_value()
    print("The game ended with {}, player {} won!".format(g.value, 0.5*g.value + 0.5))
"""
