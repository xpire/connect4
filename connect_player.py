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

#inside the game class:
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

"""
