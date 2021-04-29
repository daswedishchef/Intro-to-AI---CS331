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
    
    def get_actions(self, board, symbol):
        actions = list()
        for col in range(4):
            for row in range(4):
                if(board.is_legal_move(col, row, symbol)):
                    actions.append((col, row))
        return actions

    #parent get_move should not be called
    # def get_move(self, board):
    #     #get available actions and successor states
    #     s = list()
    #     a = self.get_actions(board, self.symbol)
    #     for ch in a:
    #         tb = board.cloneOBoard()
    #         tb.play_move(ch[0], ch[1], self.symbol)
    #         s.append(tb.count_score(self.symbol))
    #     r = np.argmin(s)
    #     return a[r]
            
    def get_move(self, board):
        #get available actions and successor states
        rs = list()
        #find successor states of bot actions
        a = self.get_actions(board, self.symbol)
        for ch in a:
            s = list()
            tb = board.cloneOBoard()
            tb.play_move(ch[0], ch[1], self.symbol)
            #if terminal, return action
            if not tb.has_legal_moves_remaining(tb.p1_symbol):
                return ch
            #find successor states of p1 actions for each bot successor
            sa = self.get_actions(tb, board.p1_symbol)
            for act in sa:
                ts = board.cloneOBoard()
                ts.play_move(act[0], act[1], board.p1_symbol)
                s.append(ts.count_score(board.p1_symbol))
            rs.append(np.argmax(s))
        r = np.argmin(rs)
        return a[r]
           

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
       
        





