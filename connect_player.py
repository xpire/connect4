#given a board, we will compute using DeepLearning or AlphaBeta pruning of
#Minimax Search, to compute the best move, and return it.
#game mechanics and variables
ncol = 7
nrow = 6
connect = 4

P1 = 1
P2 = 2

WIN_P1 = 1
WIN_P2 = -1
DRAW = 0
CONTINUE = 2

#checking a connect_row given as a string, and seeing who won
def check(string):
    score = 0
    if P1 in string and P2 in string:
        pass
    else:
        for k in range(len(string)):
            if string[k] == P2:
                score -=1
            elif string[k] == P1:
                score +=1
    return score

#node class
class node(object):
    """docstring for node."""
    def __init__(self, board):
        super(node, self).__init__()
        self.board = board
        self.value = 0
        self.move = 0 #a number in [1,7]

    # update the boards value (give an evaluation of current state of game)
    #1 for player1 win
    #-1 for player2 win
    #0 for draw
    #a fraction will give an indicator of who is more likely to win atm
    def update_value(self):
        #check the state of 0s (any 4s, 3s, 2s and 1s that could potentially be winning)
        values = [ 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #          4, 3, 2, 1, 0,-1,-2,-3,-4
        #          p1          -          p2
        #1 check vertical
        i = 0
        print("VERTICAL")
        for k in range(ncol): #vary x
            for j in range(0,nrow-3): #vary y
                # print("checking 4 in a row {} ({},{}) to ({},{})".format(i,k,j,k,j+3))
                #check
                connect_n = []
                for l in range(connect):
                    connect_n.append(self.board[j+l][k])
                val = check(connect_n)
                # print("connect_n:{}, val:{}".format(connect_n,val))
                values[4-val]+=1
                i+=1
        #2 check horizontal
        print("HORIZONTAL")
        for j in range(nrow): #vary y
            for k in range(0,ncol-3): #vary x
                # print("checking 4 in a row {} ({},{}) to ({},{})".format(i,k,j,k+3,j))
                #check
                connect_n = []
                for l in range(connect):
                    connect_n.append(self.board[j][k+l])
                val = check(connect_n)
                # print("connect_n:{}, val:{}".format(connect_n,val))
                values[4-val]+=1
                i+=1
        #3 check diagonals
        print("DIAGONALS")
        for j in range(0,nrow-3): #vary y
            for k in range(0,ncol-3): #vary x
                # print("checking 4 in a row first {} ({},{}) to ({},{})".format(i,k,j,k+3,j+3))
                #check
                connect_n = []
                for l in range(connect):
                    connect_n.append(self.board[j+l][k+l])
                val = check(connect_n)
                # print("connect_n:{}, val:{}".format(connect_n,val))
                values[4-val]+=1
                i+=1
                # print("checking 4 in a row second {} ({},{}) to ({},{})".format(i,k,j+3,k+3,j))
                #check
                connect_n = []
                for l in range(connect):
                    connect_n.append(self.board[j+connect-1-l][k+l])
                val = check(connect_n)
                # print("connect_n:{}, val:{}".format(connect_n,val))
                values[4-val]+=1
                i+=1
        print("final values:")
        print("player 1: ",end="")
        for k in range(connect):
            print("{:2}: {:2}|".format(connect-k,values[k]),end = "")
        print(" ")
        print("player 2: ",end="")
        for k in range(connect,0,-1):
            print("{:2}: {:2}|".format(-k,values[connect+k]),end = "")
        print()
        print("nothing:  {}| {}".format(connect+1-k,values[connect]))
        return

#compute next move
def compute(board):
    #extract information from board
    curr = node(board)
    curr.update_value()
    return


#player code

#old:
#
# #inside the game class:
#
#
# #player input
# def player_input():
#     move = input("What Move?")
#     #move = connect_player.move()
