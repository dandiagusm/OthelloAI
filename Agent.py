from logic import logic
import random,copy

class Agent:
    #memilih secara random dari board yang diberikan
    def Dumb_Agent(self, board, row_size, col_size, side):
        search = logic()
        list = search.search_legal_move(board, row_size, col_size, side)
        if (len(list)==0):
            return 0
        else :
            rand = random.randint(0, len(list)-1)
            move = list[rand]
            return move

class AIAgent:

    def __init__(self,max_depth,row_size, col_size):
        self.max_depth = max_depth
        self.row_size = row_size
        self.col_size = col_size

    def draw(self,board):
        print(' ', end = '  ')
        for i in range (self.col_size) :
            print(i, end='  ')
        print()

        for row in range (self.row_size):
            print(row , end = '  ')
            for col in range (self.col_size):
                    print(board[row][col], end ='  ')
            print()


    def minimax(self,board,is_max_turn,current_depth):
        board_logic = logic()
        best_value = float('-inf') if is_max_turn else float('inf')
        best_move = ()
        side = 0
        isolate_board = copy.deepcopy(board)

        # print("Depth :",current_depth,"Is Max :",is_max_turn)
        # self.draw(isolate_board)

        if is_max_turn:
            side = 1
        else:
            side = 0

        if current_depth == self.max_depth:
            terminal_score = board_logic.score(isolate_board,self.row_size,self.col_size,0)
            # print("Depth Max:",current_depth,"Score : ",terminal_score)
            # self.draw(isolate_board)
            return (terminal_score,(0,0))

        if(is_max_turn):
            next_state = board_logic.search_legal_move(isolate_board,self.row_size,self.col_size,1)
            #print("Max Turn",next_state)

            if len(next_state) :

                for move in next_state:
                    new_board = board_logic.flip_now(isolate_board,move[0],move[1],self.row_size,self.col_size,1)
                    new_board[move[0]][move[1]] = 'B'
                    # print(move)

                    score_value,move_temp = self.minimax(new_board,False,current_depth)
                    if best_value < score_value:
                        best_value = score_value
                        best_move = move
                        # print(best_move,move)

            else:
                best_value = float('inf')

        else:
            next_state = board_logic.search_legal_move(isolate_board,self.row_size,self.col_size,0)

            #print("Min Turn",next_state)

            if len(next_state):

                for move in next_state:
                    new_board = board_logic.flip_now(isolate_board,move[0],move[1],self.row_size,self.col_size,0)
                    new_board[move[0]][move[1]] = 'W'
                    score_value,move_temp = self.minimax(new_board,True,current_depth+1)

                    if best_value > score_value:
                        best_value = score_value
                        best_move = move
                        # print(best_move)

            else:
                best_value = float('-inf')

        #print("Depth :",current_depth,"Is Max :",is_max_turn,"Score : ",best_value,"Move : ",best_move)
        return best_value,best_move





