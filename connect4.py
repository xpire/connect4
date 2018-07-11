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
    class cellStat(object):
        def __init__(self):
            # |
            self.vert = 0
            # -
            self.horz = 0
            # /
            self.fdia = 0
            # \
            self.bdia = 0
            # length of longest line in each direction
            self.n = 0
            self.ne = 0
            self.e = 0
            self.se = 0
            self.s = 0
            self.sw = 0
            self.w = 0
            self.nw = 0


    '''docstring for board.'''
    def __init__(self):
        super(game, self).__init__()
        self.board = [[' ' for x in range(ncol)] for y in range(nrow)]
        self.statBoard = [[self.cellStat() for x in range(ncol)] for y in range(nrow)]
        self.heights = [0 for x in range(ncol)]
        self.cursor = 0         #possible positions: [0,...,ncol-1]
        self.turn = 0           #the current turn
        self.player = P1        #alternates between player 0 and player 1
        self.value = CONTINUE   #1 for a win (player 0), -1 for a win (player 1)
        self.stat = [0 for i in range(2*connect+1)]
        self.stat[connect] = ncol*nrow

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


    def update_stat(self):
        x = self.cursor
        y = self.heights[x] -1
        cellC = self.statBoard[y][x]
        P = self.board[y][x]
        # count horizontal change
        l = 0
        r = 0
        print('x: {} y: {}'.format(x,y))
        alone_f = True
        remL = False
        remR = False
        remD = False
        remRFD = False
        remLFD = False
        remLBD = False
        remRBD = False
        # check left line
        cellL = self.statBoard[y][x-1]
        lenL = cellL.horz

        if self.board[y][x] == self.board[y][x-1]:
            if not lenL == 0:
                alone_f = False
            if not(lenL <= 1 and lenL >= -1 and cellL.vert <= 1 and cellL.vert >= -1 and cellL.fdia <= 1 and cellL.fdia >= -1 and cellL.bdia <= 1 and cellL.bdia >= -1):
                remL = True
        else:
            print(self.board[y][x])
            print(self.board[y][x-1])
        # check right line
        cellR = self.statBoard[y][x+1]
        lenR = cellR.horz
        if self.board[y][x] == self.board[y][x+1]:
            if not lenR == 0:
                alone_f = False
            if not(lenR <= 1 and lenR >= -1 and cellR.vert <= 1 and cellR.vert >= -1 and cellR.fdia <= 1 and cellR.fdia >= -1 and cellR.bdia <= 1 and cellR.bdia >= -1):
                remR = True
            newHorzLen = lenR + lenL + 1
        else:
            newHorzLen = 1
        print('left = {}, right = {}, total length = {}'.format(lenL, lenR, newHorzLen))

        # update statboard
        if not lenL == 0:
            for i in lenL:
                self.statBoard[y][x-i].horz = newHorzLen
        if not lenR == 0:
            for i in lenR:
                self.statBoard[y][x+i].horz = newHorzLen

        # modify stat for horizontal line
        if remL:
            self.stat[connect + lenL] -= 1
        if remR:
            self.stat[connect + lenR] -= 1
        if not (lenR == 0 and lenL == 0):
            if newHorzLen >= connect:
                self.stat[connect + connect] += 1
            else:
                self.stat[connect + newHorzLen] += 1

        # check down line
        cellD = self.statBoard[y-1][x]
        lenD = cellD.vert
        if self.board[y][x] == cellD:
            if not lenD == 0:
                alone_f = False
            if not(lenD <= 1 and lenD >= -1 and cellD.horz <= 1 and cellD.horz >= -1 and cellD.fdia <= 1 and cellD.fdia >= -1 and cellD.bdia <= 1 and cellD.bdia >= -1):
                remD = True
            newVertLen = lenD + 1
        else:
            newVertLen = 0

        # update statboard
        if not lenD == 0:
            for i in lenD:
                self.statBoard[y-i][x].vert = newVertLen

        # modify stat for vertical line
        if remD:
            self.stat[connect + lenD] -= 1
        if not lenD == 0:
            if newVertLen >= connect:
                self.stat[connect + connect] += 1
            else:
                self.stat[connect + newVertLen] += 1

        # check forward diagonal line (up-right)
        cellRFD = self.statBoard[y+1][x+1]
        lenRFD = cellRFD.fdia
        if self.board[y][x] == self.board[y+1][x+1]:
            if not lenRFD == 0:
                alone_f = False
            if not(lenRFD <= 1 and lenRFD >= -1 and cellRFD.horz <= 1 and cellRFD.horz >= -1 and cellRFD.vert <= 1 and cellRFD.vert >= -1 and cellRFD.bdia <= 1 and cellRFD.bdia >= -1):
                remRFD = True

        cellLFD = self.statBoard[y-1][x-1]
        lenLFD = cellLFD.fdia
        if self.board[y][x] == self.board[y-1][x-1]:
            if not lenLFD == 0:
                alone_f = False
            if not(lenLFD <= 1 and lenLFD >= -1 and cellLFD.horz <= 1 and cellLFD.horz >= -1 and cellLFD.vert <= 1 and cellLFD.vert >= -1 and cellLFD.bdia <= 1 and cellLFD.bdia >= -1):
                remLFD = True
            newFDiaLen = lenRFD + lenLFD + 1
        else:
            newFDiaLen = 0

        # update statboard
        if not lenRFD == 0:
            for i in lenRFD:
                self.statBoard[y+i][x+i].fdia = newFDiaLen

        if not lenLFD == 0:
            for i in abs(lenLFD):
                self.statBoard[y-i][x-i].fdia = newFDiaLen

        # modify stat for forward diagonal line
        if remRFD:
            self.stat[connect + lenRFD] -= 1
        if remLFD:
            self.stat[connect + lenLFD] -= 1
        if not (lenRFD == 0 and lenLFD == 0):
            if newRDiaLen >= connect:
                self.stat[connect + connect] += 1
            else:
                self.stat[connect + newRDiaLen] += 1

        # check backward diagonal line (up-left)
        cellLBD = self.statBoard[y+1][x-1]
        lenLBD = cellLBD.bdia
        if self.board[y][x] == self.board[y+1][x-1]:
            if not lenLBD == 0:
                alone_f = False
            if not(lenLBD <= 1 and lenLBD >= -1 and cellLBD.horz <= 1 and cellLBD.horz >= -1 and cellLBD.vert <= 1 and cellLBD.vert >= -1 and cellLBD.fdia <= 1 and cellLBD.fdia >= -1):
                remLBD = True

        cellRBD = self.statBoard[y-1][x+1]
        lenRBD = cellRBD.bdia
        if self.board[y][x] == self.board[y-1][x+1]:
            if not lenRBD == 0:
                alone_f = False
            if not(lenRBD <= 1 and lenRBD >= -1 and cellRBD.horz <= 1 and cellRBD.horz >= -1 and cellRBD.vert <= 1 and cellRBD.vert >= -1 and cellRBD.fdia <= 1 and cellRBD.fdia >= -1):
                remRBD = True
            newBDiaLen = lenRBD + lenRBD + 1
        else:
            newBDiaLen = 0

        # update statboard
        if not lenRBD == 0:
            for i in lenRBD:
                self.statBoard[y-i][x+i].bdia = newBDiaLen

        if not lenLBD == 0:
            for i in abs(lenLBD):
                self.statBoard[y+i][x-i].fdia = newBDiaLen

        # modify stat for forward diagonal line
        if remRBD:
            self.stat[connect + lenRBD] -= 1
        if remLBD:
            self.stat[connect + lenLBD] -= 1
        if not (lenRBD == 0 and lenLBD == 0):
            if newBDiaLen >= connect:
                self.stat[connect + connect] += 1
            else:
                self.stat[connect + newBDiaLen] += 1
        # check for lonely cell
        if alone_f:
            if P == P1:
                player_sign = 1
            if P == P2:
                player_sign = -1
            self.stat[connect + player_sign*1] += 1
        # always one less available cell
        self.stat[connect] -= 1
        for i in range(nrow):
            for j in range(ncol):
                print(self.statBoard[i][j], end='')
            print('')

    #update the boards value (give an evaluation of current state of game)
    #1 for player1 win
    #-1 for player2 win
    #0 for draw
    #2 if the game is still in motion
    def update_value(self):
        #check the state of winning 4 in a rows and update value accordingly

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
                        if self.board[j][k] == P2:
                            self.value = WIN_P2
                        elif self.board[j][k] == P1:
                            self.value = WIN_P1

        #draw check, if game is filled and not winning
        draw = True
        for k in range(ncol):
            for j in range(nrow):
                if self.board[j][k] == ' ':
                    draw = False
        if draw:
            self.value = DRAW

        #else, self.value is unchanged (assert that it is 2?)

        return

#player input
def player_input(board):
    move = input('What Move? ')
    fake_move = connect_player.compute(board)
    if not move:
        return 'x' #dummy variable coz i keep accidentally not returning a value
    return move[0]

#Actual Game part:
if __name__ == '__main__':
    g = game()
    g.show()

    while abs(g.value) == CONTINUE:
        #get move, ask game.player for move

        player_move = player_input(g.board)
        if (g.valid(player_move)):
            #apply move
            g.make_move(player_move)
            g.show()
            if player_move == ' ':
                g.update_stat()
                print(g.stat)
            g.update_value()
        else:
            print('Sorry, invalid move, try again.')
            g.show()
            continue
        #clean up
    if g.value == WIN_P1 or g.value == WIN_P2:
        #GAME WON
        print('The game ended with {}, '.format(g.value),end="")

        if g.value == WIN_P1:
            print('\033[1;31m', end='')
        elif g.value == WIN_P2:
            print('\033[1;93m', end='')

        print('player {}\033[0m'.format(int(-0.5*g.value + 1.5)),end="")
        print(' won!')
    if g.value == DRAW:
        print('The game ended with a draw!')
