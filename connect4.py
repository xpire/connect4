import random
import sys, time
import itertools as it

#game mechanics:
#7 columns, 6 rows board. Choose one column that is not filled to put ur counter
ncol = 7
nrow = 6
winLen = 4

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
            if self.player == 0:
                self.player = 1
            elif self.player == 1:
                self.player = 0
        return


    #update the boards value (give an evaluation of current state of game)
    #1 for player0 win
    #-1 for player1 win
    #0 for draw
    #a fraction will give an indicator of who is more likely to win atm
    def update_value(self):
        #check the state of 0s (any 4s, 3s, 2s and 1s that could potentially be winning)

        for k in range(ncol):
            for j in range(nrow):
                if not self.board[j][k] == '':
                    #1 check vertical
                    if j >= winLen-1:
                        win_v = True
                        for check in range(j-winLen+1,j):
                            if not self.board[check][k] == self.board[j][k]:
                                win_v = False
                                break
                    else:
                        win_v = False

                    #2 check horizontal
                    if k >= winLen-1:
                        win_h = True
                        for check in range(k-winLen+1,k):
                            if not self.board[j][check] == self.board[j][k]:
                                win_h = False
                                break
                    else:
                        win_h = False

                    #3 check diagonals
                    if j >= winLen-1:
                        win_d1 = True
                        win_d2 = True
                        for diff in range(winLen):
                            if not k >= winLen-1 or not self.board[j-diff][k-diff] == self.board[j][k]:
                                win_d1 = False

                            if not k + winLen-1 < ncol or not self.board[j-diff][k+diff] == self.board[j][k]:
                                win_d2 = False

                            if not win_d1 and not win_d2:
                                break
                    else:
                        win_d1 = False
                        win_d2 = False
                    if win_h or win_v or win_d1 or win_d2:
                        if self.board[j][k] == 1:
                            self.value = -1
                        elif self.board[j][k] == 0:
                            self.value = 1
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
    g.show()

    while abs(g.value) != 1:
        #get move, ask game.player for move

        player_move = player_input()
        if (g.valid(player_move)):
            if player_move in ['l','L','r','R', ' ']:
                g.make_move(player_move)
                g.show()
                g.update_value()

        else:
            print("Sorry, invalid move, try again.")
            g.show()
            continue
        #apply move
        #clean up
        #g.player = (g.player+1)%2
    print("The game ended with {}, player {} won!".format(g.value, 0.5*g.value + 0.5))
