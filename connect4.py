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

    def player_sign(self, player):
        if player == P1:
            return 1
        if player == P2:
            return -1

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
        P = self.board[y][x]
        # count horizontal change
        l = 0
        r = 0
        print('x: {} y: {}'.format(x,y))
        alone_f = True
        remE = False
        remW = False
        remS = False
        remRFD = False
        remLFD = False
        remLBD = False
        remRBD = False

        # cells relative to the current cell
        statC = self.statBoard[y][x]
        cellC = self.board[y][x]
        if x-1 < 0:
            statE = None
            cellE = None
        else:
            cellE = self.board[y][x-1]
            statE = self.statBoard[y][x-1]
        if x+1 >= ncol:
            statW = None
            cellW = None
        else:
            statW = self.statBoard[y][x+1]
            cellW = self.board[y][x+1]

        if y-1 < 0:
            statS = None
            cellS = None
        else:
            statS = self.statBoard[y-1][x]
            cellS = self.board[y-1][x]

        # lengths of existing lines in surrounding directions
        def lenFind(curCell, comCell, stat):
            if stat == None:
                return 0
            else:
                if curCell == comCell:
                    return stat.horz
                else:
                    return 0

        lenE = lenFind(cellC, cellE, statE)
        lenW = lenFind(cellC, cellW, statW)
        lenS = lenFind(cellC, cellS, statS)
        '''
        if statE == None:
            lenE = 0
        else:
            if cellC == cellE:
                lenE = statE.horz
            else:
                lenE = 0

        if statW == None:
            lenW = 0
        else:
            if cellC == cellW:
                lenW = statW.horz
            else:
                lenW = 0
        '''

        # check left line
        if cellC == cellE:
            if not lenE == 0:
                alone_f = False
            print('horz = {}, vert = {}, fdia = {}, bdia = {}'.format(lenE, statE.vert, statE.fdia, statE.bdia))
            #if not(lenL < 1 and lenL > -1 and cellL.vert < 1 and cellL.vert > -1 and cellL.fdia < 1 and cellL.fdia > -1 and cellL.bdia < 1 and cellL.bdia > -1):
            if not( lenE == 0 and statE.vert == 0 and statE.fdia == 0 and statE.bdia == 0):
                remE = True

        # check right line
        if cellC == cellW:
            if not lenW == 0:
                alone_f = False
            if not(lenW < 1 and lenW > -1 and statW.vert < 1 and statW.vert > -1 and statW.fdia < 1 and statW.fdia > -1 and statW.bdia < 1 and statW.bdia > -1):
                remW = True

        newHorzLen = lenW + lenE + self.player_sign(P)

        print('left = {}, right = {}, total length = {}'.format(lenE, lenW, newHorzLen))
        print('player = {}'.format(self.player_sign(P)))
        # update statboard
        if not lenE == 0:
            for i in range(abs(lenE)):
                self.statBoard[y][x-i].horz = newHorzLen
        if not lenW == 0:
            for i in range(abs(lenW)):
                self.statBoard[y][x+i].horz = newHorzLen

        # modify stat for horizontal line
        if remE:
            self.stat[connect + lenE] -= 1
        if remW:
            self.stat[connect + lenW] -= 1
        if not (lenW == 0 and lenE == 0):
            if abs(newHorzLen) >= connect:
                self.stat[connect + self.player_sign(P)*connect] += 1
            else:
                self.stat[connect + newHorzLen] += 1

        # check bottom line
        if cellC == cellS:
            if not lenS == 0:
                alone_f = False
            if not( lenS == 0 and statS.vert == 0 and statS.fdia == 0 and statS.bdia == 0):
                remS = True

        newVertLen = lenS + self.player_sign(P)

        # update statboard
        if not lenS == 0:
            for i in range(abs(lenS)):
                self.statBoard[y-i][x].horz = newVertLen

        # modify stat for horizontal line
        if remS:
            self.stat[connect + lenS] -= 1
        if not lenS == 0 :
            if abs(newVertLen) >= connect:
                self.stat[connect + self.player_sign(P)*connect] += 1
            else:
                self.stat[connect + newVertLen] += 1
        '''
        # check down line
        cellD = self.statBoard[y-1][x]
        lenD = cellD.vert
        if self.board[y][x] == cellD:
            if not lenD == 0:
                alone_f = False
            if not(lenD <= 1 and lenD >= -1 and cellD.horz <= 1 and cellD.horz >= -1 and cellD.fdia <= 1 and cellD.fdia >= -1 and cellD.bdia <= 1 and cellD.bdia >= -1):
                remD = True
            newVertLen = lenD + self.player_sign(P)
        else:
            newVertLen = 0

        # update statboard
        if not lenD == 0:
            for i in range(abs(lenD)):
                self.statBoard[y-i][x].vert = newVertLen

        # modify stat for vertical line
        if remD:
            self.stat[connect + lenD] -= 1
        if not lenD == 0:
            if abs(newVertLen) >= connect:
                self.stat[connect + self.player_sign(P)*connect] += 1
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
            newFDiaLen = lenRFD + lenLFD + self.player_sign(P)
        else:
            newFDiaLen = 1

        # update statboard
        if not lenRFD == 0:
            for i in range(abs(lenRFD)):
                self.statBoard[y+i][x+i].fdia = newFDiaLen

        if not lenLFD == 0:
            for i in range(abs(lenLFD)):
                self.statBoard[y-i][x-i].fdia = newFDiaLen

        # modify stat for forward diagonal line
        if remRFD:
            self.stat[connect + lenRFD] -= 1
        if remLFD:
            self.stat[connect + lenLFD] -= 1
        if not (lenRFD == 0 and lenLFD == 0):
            if abs(newFDiaLen) >= connect:
                self.stat[connect + self.player_sign(P)*connect] += 1
            else:
                self.stat[connect + newFDiaLen] += 1

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
            newBDiaLen = lenRBD + lenRBD + self.player_sign(P)
        else:
            newBDiaLen = self.player_sign(P)

        # update statboard
        if not lenRBD == 0:
            for i in range(abs(lenRBD)):
                self.statBoard[y-i][x+i].bdia = newBDiaLen

        if not lenLBD == 0:
            for i in range(abs(lenLBD)):
                self.statBoard[y+i][x-i].fdia = newBDiaLen

        # modify stat for forward diagonal line
        if remRBD:
            self.stat[connect + lenRBD] -= 1
        if remLBD:
            self.stat[connect + lenLBD] -= 1
        if not (lenRBD == 0 and lenLBD == 0):
            if abs(newBDiaLen) >= connect:
                self.stat[connect + self.player_sign(P)*connect] += 1
            else:
                self.stat[connect + newBDiaLen] += 1
        '''
        # check for lonely cell
        if alone_f:
            print('LONELY')
            self.stat[connect + self.player_sign(P)] += 1
            soleCell = self.cellStat()
            ps = self.player_sign(P)
            soleCell.vert = ps
            soleCell.horz = ps
            soleCell.fdia = ps
            soleCell.bdia = ps
            self.statBoard[y][x] = soleCell
        # always one less available cell
        self.stat[connect] -= 1


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
