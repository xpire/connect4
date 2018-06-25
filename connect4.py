import random
import sys, time
import itertools as it

#game mechanics:
#7 columns, 6 rows board. Choose one column that is not filled to put ur counter
ncol = 7
nrow = 6
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

    def show(self):
        print("Turn:{}, Player_{}'s move:".format(self.turn,self.player))
        print("heights:{}".format(self.heights))
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

    def possible(self, move):
        if move in ['l','L','r','R',' ']: #left, right, space
            return 1
        return 0

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

    def update_value(self):
        #check the state of 0s (any 4s, 3s, 2s and 1s that could potentially be winning)
        #1 check vertical
        for k in range(ncols):
            for j in range(0,ncols-4):
                
        #2 check horizontal
        #3 check diagonals
        return

def player_input():
    move = input("What Move?")
    if not move:
        return 'x'
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
