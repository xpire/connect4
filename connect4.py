import random
import sys, time
import itertools as it

import connect_player

#game mechanics:
#7 columns, 6 rows board. Choose one column that is not filled to put ur counter
ncol = 7
nrow = 6
connect = 4

P1 = 1
P2 = 2

WIN_P1 = 1
WIN_P2 = -1
DRAW = 0
CONTINUE = 2

#An instance of the game, which holds the board, (and heights), cursor position
#player, and the game's current value (denoted as a 1 for p0 win, -1 for p1 win, and inbetween)
class game(object):
    '''docstring for board.'''
    def __init__(self):
        super(game, self).__init__()
        self.board = [[' ' for x in range(ncol)] for y in range(nrow)]
        self.heights = [0 for x in range(ncol)]
        self.cursor = 0 #possible positions: [0,...,ncol-1]
        self.turn = 0   #the current turn
        self.player = P1 #alternates between player 0 and player 1
        self.value = CONTINUE  #1 for a win (player 0), -1 for a win (player 1)

    #show game state
    def show(self):
        print('Turn:{} '.format(self.turn) ,end='')

        if self.player == P1:
            print('\033[1;31m', end='')
        elif self.player == P2:
            print('\033[1;93m', end='')

        print('Player_{}\'s\033[0m move:'.format(self.player))
        print('Heights:{}'.format(self.heights))
        print("Value:{}".format(self.value))

        for k in range(self.cursor):
            print('  ', end='')
        print(' v', end='')
        for k in range(ncol-self.cursor):
            print(' ', end='')
        print(' ')
        print('*' + '-'*(2*ncol-1) + '*')
        for y in range(nrow-1,-1,-1):
            print('|',end='')
            for x in range(ncol):
                if self.board[y][x] == P1:
                    print('\033[1;31m', end='')
                elif self.board[y][x] == P2:
                    print('\033[1;93m', end='')
                print('{}'.format(self.board[y][x]), end='\033[0m|')
            print(' ')
        print('*' + '-'*(2*ncol-1) + '*')

    #sanity check for possible input of moves
    def possible(self, move):
        if move in ['l','L','r','R',' ']: #left, right, space
            return True
        elif move in ['1','2','3','4','5','6','7',1,2,3,4,5,6,7]: #column number
            return True
        return False

    #validity check if the current move is allowed in the game
    def valid(self, move):
        if self.possible(move):
            if move in ['l','L','r','R']:
                return True
            # TODO Should be in range(cols) for better flexibility
            elif move in ['1','2','3','4','5','6','7',1,2,3,4,5,6,7]:
                return True
            elif move == ' ':
                #place counter here
                if self.heights[self.cursor] >= nrow:
                    return False
                else:
                    return True
        return False

    #makes the move happen and increments turn
    def make_move(self, m):
        if m in ['l','L']:
            self.cursor-=1
            self.cursor = self.cursor%ncol
            return #does not iterate self.turn
        elif m in ['r','R']:
            self.cursor+=1
            self.cursor = self.cursor%ncol
            return #does not iterate self.turn
        elif m in ['1','2','3','4','5','6','7',1,2,3,4,5,6,7]:
            self.cursor = int(m)-1
            return #does not iterate self.turn
        else:# m == ' ':
            y = self.heights[self.cursor]
            self.board[y][self.cursor] = self.player
            self.heights[self.cursor] += 1
            if self.player == P1:
                self.player = P2
            elif self.player == P2:
                self.player = P1
        self.turn += 1


    #update the boards value (give an evaluation of current state of game)
    #1 for player1 win
    #-1 for player2 win
    #0 for draw
    #2 if the game is still in motion
    def update_value(self):
        #check the state of winning 4 in a rows and update value accordingly

        #draw check, if game is filled and not winning
        draw = True
        for k in range(ncol):
            for j in range(nrow):
                if self.board[j][k] == ' ':
                    draw = False
        if draw:
            self.value = DRAW

        #checking for 4 in a rows
        for k in range(ncol):
            for j in range(nrow):
                if not self.board[j][k] == ' ':
                    #1 check vertical
                    if j >= connect-1:
                        win_v = True
                        for check in range(j-connect+1,j):
                            if not self.board[check][k] == self.board[j][k]:
                                win_v = False
                                break
                    else:
                        win_v = False

                    #2 check horizontal
                    if k >= connect-1:
                        win_h = True
                        for check in range(k-connect+1,k):
                            if not self.board[j][check] == self.board[j][k]:
                                win_h = False
                                break
                    else:
                        win_h = False

                    #3 check diagonals
                    if j >= connect-1:
                        win_d1 = True
                        win_d2 = True
                        for diff in range(connect):
                            if not k >= connect-1 or not self.board[j-diff][k-diff] == self.board[j][k]:
                                win_d1 = False

                            if not k + connect-1 < ncol or not self.board[j-diff][k+diff] == self.board[j][k]:
                                win_d2 = False

                            if not win_d1 and not win_d2:
                                break
                    else:
                        win_d1 = False
                        win_d2 = False

                    if win_h or win_v or win_d1 or win_d2:
                        if self.board[j][k] == 2:
                            self.value = WIN_P2
                        elif self.board[j][k] == 1:
                            self.value = WIN_P1
        return

#player input
def player_input():
    move = input('What Move? ')
    #move = connect_player.move()
    if not move:
        return 'x' #dummy variable coz i keep accidentally not returning a value
    return move[0]

#Actual Game part:
if __name__ == '__main__':
    g = game()
    g.show()

    while abs(g.value) == CONTINUE:
        #get move, ask game.player for move

        player_move = player_input()
        if (g.valid(player_move)):
            g.make_move(player_move)
            g.show()
            g.update_value()

        else:
            print('Sorry, invalid move, try again.')
            g.show()
            continue
        #apply move
        #clean up
        #g.player = (g.player+1)%2
    if g.value == WIN_P1 or g.value == WIN_P2:
        print('The game ended with {}, '.format(g.value),end="")

        if g.value == WIN_P1:
            print('\033[1;31m', end='')
        elif g.value == WIN_P2:
            print('\033[1;93m', end='')

        print('player {}\033[0m'.format(int(-0.5*g.value + 1.5)),end="")
        print(' won!')
    if g.value == DRAW:
        print('The game ended with a draw!')
