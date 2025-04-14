#class Game board for othello
from logic import logic
from Agent import Agent,AIAgent

class Game :
    def __init__(self, row, col):
        self.__cols_size = col
        self.__rows_size = row
        self.__turn = 0
        self.__numb_of_skip = 0 #jika skip dua kali berturut2, maka game stuck dan harus diterminate
        self.__side = 0 #sisi yang akan melangkah
        # side = 0 giliran sisi putih untuk melangkah
        # side = 1 giliran sisi hitam untuk melangkah
        self.__legal_move = []
        self.__flip = []
        self.__board = []
        # W = white
        # B = Black
        # - = Empty
        # ? = Suggested move

        for i in range(self.__rows_size):
            self.__board.append([])
            for j in range(self.__cols_size):
                self.__board[i].append('-')


        #inisiasi  4 kotak pertama pada awal permainan othello
        self.__board[self.__rows_size//2 -1][self.__cols_size//2 -1] = 'W'
        self.__board[self.__rows_size//2 -1][self.__cols_size//2] = 'B'
        self.__board[self.__rows_size//2][self.__cols_size//2 - 1] = 'B'
        self.__board[self.__rows_size//2][self.__cols_size//2] = 'W'

    def get_cols_size(self):
        return self.__cols_size

    def get_rows_size(self):
        return self.__rows_size

    def set_rows_size(self, value):
        self.__rows_size = value

    def set_cols_size(self, value):
        self.__cols_size = value

    def get_element(self, row, col):
        return self.__board[row][col]

    #set element board = W atau B berdasarkan state side game saat itu
    def set_element(self, row, col, value):
        self.__board[row][col]=value

    def get_board(self):
        return self.__board

    def get_numb_of_skip(self):
        return self.__numb_of_skip

    def Add_numb_of_skip(self):
        self.__numb_of_skip = self.__numb_of_skip+1

    def reset_numb_of_skip(self):
        self.__numb_of_skip=0

    def get_side(self):
        return self.__side

    #Untuk mengganti sisi yang akan melangkah
    def change_side(self):
        if (self.__side ==0 ):
            self.__side = 1
        elif (self.__side == 1) :
            self.__side =0

    def get_turn(self):
        return self.__turn

    def Add_turn(self):
        self.__turn=self.__turn+1

    #Untuk mengecek apabila permainan telah berakhir
    def is_end(self):
        if(self.__turn == self.__cols_size*self.__rows_size -4 or self.__numb_of_skip==2):
            return True
        else :
            return False

    #Menghasilkan banyaknya keping dari White dan Black dalam bentuk tuple : (White, Black)
    def score(self):
        score_W = 0
        score_B = 0
        for row in range (self.__rows_size):
            for col in range (self.__cols_size):
                if (self.__board[row][col]=='W'):
                    score_W = score_W +1
                elif (self.__board[row][col]=='B'):
                    score_B = score_B +1
        return (score_W, score_B)

    def winner(self):
        if(self.is_end() or self.__numb_of_skip == 2):
            hasil = self.score()
            putih = hasil[0]
            hitam = hasil[1]
            if(putih>hitam):
                return 'WHITE WIN'
            elif(putih<hitam):
                return  'BLACK WIN'
            elif(putih==hitam):
                'DRAW'

    #untuk validasi apakah move (row,col) adalah valid
    def is_valid(self, row, col):
        if ((row,col) in self.get_legal_move() ):
            return True
        else :
            return False

    def generate_legal_move(self):
        search = logic()

        self.__legal_move = search.search_legal_move(self.get_board(), self.get_rows_size(), self.get_cols_size(), self.get_side())


    def generate_list_to_flip(self, row, col):
        search = logic()
        self.__flip = search.search_list_to_be_flipped(self.get_board(), row, col, self.get_rows_size(), self.get_cols_size(), self.get_side())

    def get_legal_move(self):
        return self.__legal_move

    def get_list_flip(self):
        return self.__flip

    #Meletakan keping pada board
    def make_move(self, row, col):
        if(self.get_side() == 0):
            self.set_element(row,col,"W")
            self.make_flip(row,col, "W")
            self.Add_turn()
            self.change_side()

        else :
            self.set_element(row,col,"B")
            self.make_flip(row,col, "B")
            self.Add_turn()
            self.change_side()

    #untuk memutar keping setelah melangkah pada (row,col)
    def make_flip(self, row, col, value):
        putar = self.get_list_flip()
        if (len(putar)>0):
            for coor in putar:
                self.set_element(coor[0],coor[1], value)

    #Untuk mengecek apakah sudah tidak ada langkah yang valid. jika bernilai true, maka "side" saat ini tidak melangkah
    def skip(self):
        if(len(self.get_legal_move()) == 0):
            return True
        else:
            return False

    #Membentuk papan permainan
    def draw(self):
        print(' ', end = '  ')
        for i in range (self.get_cols_size()) :
            print(i, end='  ')
        print()

        for row in range (self.get_rows_size()):
            print(row , end = '  ')
            for col in range (self.get_cols_size()):
                legal = self.get_legal_move()
                if( (row ,col) in legal) :
                    print("?", end = '  ')
                else :
                    print(self.get_element(row,col), end ='  ')
            print()


    def main_DumbAgent_and_withoutGUI(self):
        while(not self.is_end() and not self.get_numb_of_skip() >=2):
            self.generate_legal_move()
            self.draw()
            score = self.score()
            print("Score :")
            print("WHITE = ", score[0] )
            print("BLACK = ", score[1])
            if(self.get_side() == 0):
                if(not self.skip()):
                    print ("PLAYER move")
                    r = int(input("ROW = "))
                    c = int(input("COL = "))
                    while ( not self.is_valid(r, c)):
                        print("Input tidak valid")
                        r = int (input("ROW = "))
                        c = int (input("COL = "))
                    self.generate_list_to_flip(r,c)
                    self.make_move(r, c)
                    self.reset_numb_of_skip()

                else :
                    print("PLAYER SKIP")
                    self.change_side()
                    self.Add_numb_of_skip()
            else :
                if (not self.skip() ):
                    # AI = Agent()
                    # agent_move = AI.Dumb_Agent(self.get_board(), self.get_rows_size(), self.__cols_size, self.get_side())
                    AI = AIAgent(2,self.__rows_size,self.__cols_size)
                    value,agent_move = AI.minimax(self.get_board(),True,0)
                    print("AI MOVE = ", end ='')
                    print(agent_move)
                    self.generate_list_to_flip(agent_move[0],agent_move[1])
                    self.make_move(agent_move[0], agent_move[1])
                    self.reset_numb_of_skip()
                else :
                    print("AGENT SKIP")
                    self.change_side()
                    self.Add_numb_of_skip()

            print()
            print("-------------------------------------------------------------------")
        self.generate_legal_move()
        print("GAME OVER")
        self.draw()
        score = self.score()
        print("Score :")
        print("WHITE = ", score[0] )
        print("BLACK = ", score[1])

    def TEST_DumbAGENT_VS_AI(self):
        while(not self.is_end() and not self.get_numb_of_skip() >=2):
            self.generate_legal_move()
            self.draw()
            score = self.score()
            print("Score :")
            print("WHITE = ", score[0] )
            print("BLACK (AI) = ", score[1])
            if(self.get_side() == 0):
                if(not self.skip()):
                    Dumb = Agent()
                    Dumb_move = Dumb.Dumb_Agent(self.get_board(), self.get_rows_size(), self.__cols_size, self.get_side())
                    print("Dumb MOVE = ", end ='')
                    print(Dumb_move)
                    self.generate_list_to_flip(Dumb_move[0],Dumb_move[1])
                    self.make_move(Dumb_move[0], Dumb_move[1])
                    self.reset_numb_of_skip()
                else :
                    print("AGENT DUMB SKIP")
                    self.change_side()
                    self.Add_numb_of_skip()

            else :
                if (not self.skip() ):
                    # AI = Agent()
                    # agent_move = AI.Dumb_Agent(self.get_board(), self.get_rows_size(), self.__cols_size, self.get_side())
                    AI = AIAgent(1,self.__rows_size,self.__cols_size)
                    value,agent_move = AI.minimax(self.get_board(),True,0)
                    print("AI MOVE = ", end ='')
                    print(agent_move)
                    if(len(agent_move) ==0):
                        print("AGENT SKIP")
                        self.change_side()
                        self.Add_numb_of_skip()
                    else :
                        self.generate_list_to_flip(agent_move[0],agent_move[1])
                        self.make_move(agent_move[0], agent_move[1])
                        self.reset_numb_of_skip()
                else :
                    print("AGENT SKIP")
                    self.change_side()
                    self.Add_numb_of_skip()

            print()
            print("-------------------------------------------------------------------")
        self.generate_legal_move()
        print("GAME OVER")
        self.draw()
        score = self.score()
        print("Score :")
        print("WHITE = ", score[0] )
        print("BLACK (AI)= ", score[1])
test = Game(8,8)
test.TEST_DumbAGENT_VS_AI()