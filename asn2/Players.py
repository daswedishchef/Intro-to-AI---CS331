'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''
import numpy as np

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol

    #get possible actions
    def get_actions(self, board, symbol):
        actions = list()
        for col in range(4):
            for row in range(4):
                if(board.is_legal_move(col, row, symbol)):
                    actions.append((col, row))
        return actions

    #utility functions
    def get_score(self, board):
        s = board.count_score('O') - board.count_score('X')
        return s
    
    def has_won(self, board):
        s = board.count_score('O') + board.count_score('X')
        return s == 16 and self.get_score(board) > 0

    #successor function
    def get_succ(self, board, symbol, depth = 0):
        scores = dict()
        actions = self.get_actions(board, symbol)
        if len(actions) == 0:
            tsc = self.get_score(board)
            if not board.has_legal_moves_remaining(board.p1_symbol) or self.has_won(board):
                tsc += 100
            if not board.has_legal_moves_remaining(board.p2_symbol):
                tsc -= 100
            return tsc
        for a in actions:
            tb = board.cloneOBoard()
            tb.play_move(a[0],a[1],symbol)
            score = self.get_score(tb)
            if symbol == 'X':
                res = self.get_succ(tb, 'O', depth + 1)
            else:
                res = self.get_succ(tb, 'X', depth + 1)
            if type(res) == int:
                s_score = res
            else:
                s_score = 0
                for k in res:
                    s_score += res[k][0]
            scores[(a,symbol)] = (s_score + score, res)
        return scores

    #minimax function
    def get_move(self, board):
        #get available actions and successor states
        rs = self.get_succ(board, self.symbol)
        scores = -100000000000000000000
        for state in rs:
            if(scores < rs[state][0]):
                scores = rs[state][0]
                move = state[0]
        return move


class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
       
        





