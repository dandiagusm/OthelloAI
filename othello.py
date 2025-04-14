#AI for Othello with minimax
#ABAIKAN
#ABAIKAN
#ABAIKAN
#ABAIKAN

import random

class othello:
    def __init__(self, row, col):
        self.cols = col
        self.rows = row
        self.turn = 0
        self.numb_of_skip = 0 #jika skip dua kali berturut2, maka game stuck dan harus diterminate
        self.side = 0
        # side = 0 giliran sisi putih untuk melangkah
        # side = 1 giliran sisi hitam untuk melangkah

        self.board = []
        # W = white
        # B = Black
        # - = Empty
        # ? = Suggested move

        self.legal_move = []
        #Daftar langkah yang diperbolehkan berdasarkan state board saat ini

        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[i].append('-')


        #inisiasi  4 kotak pertama pada awal permainan othello
        self.board[self.rows//2 -1][self.cols//2 -1] = 'W'
        self.board[self.rows//2 -1][self.cols//2] = 'B'
        self.board[self.rows//2][self.cols//2 - 1] = 'B'
        self.board[self.rows//2][self.cols//2] = 'W'

    #Untuk mengganti sisi yang akan melangkah
    def change_side(self):
        if (self.side ==0 ):
            self.side = 1
        elif (self.side == 1) :
            self.side =0

    def is_valid_coordinate(self, row,col):
        if(col>=0 and col<self.cols and row>=0 and row<self.rows):
            return True
        else :
            return False



    #menghasilkan posisi-posisi yang dapat diambil oleh side yang akan melangkah
    def search_legal_move(self):
        temp_array = []
        for row in range (self.rows):
            for col in range (self.cols):
                if (self.board[row][col] == '-'):
                    check_again_around = True
                    if (self.side == 0):
                        #look around
                        for delta_row in range (-1,2):
                            for delta_col in range (-1,2):
                                if self.is_valid_coordinate(row+delta_row, col+delta_col) and not (delta_col == 0 and delta_row == 0):
                                    if (self.board[row+delta_row][col + delta_col]=='B'):
                                        if self.is_valid_coordinate(row+2*delta_row, col + 2*delta_col) and self.board[row+2*delta_row][col + 2*delta_col] =='W':
                                            temp_array.append((row,col))
                                            check_again_around = False
                                            break

                            if (not check_again_around):
                                break

                    elif (self.side ==1):
                        #look around
                        for delta_row in range (-1,2):
                            for delta_col in range (-1,2):
                                if self.is_valid_coordinate(row+delta_row, col+delta_col) and not (delta_col == 0 and delta_row == 0):
                                    if (self.board[row+delta_row][col + delta_col]=='W'):
                                        if self.is_valid_coordinate(row+2*delta_row, col + 2*delta_col) and self.board[row+2*delta_row][col + 2*delta_col] =='B':
                                            temp_array.append((row,col))
                                            check_again_around = False
                                            break

                            if (not check_again_around):
                                break

        return temp_array


    #Meletakan keping pada board
    def move(self, row, col):
        if self.side == 0:
            self.board[row][col]='W'
        elif self.side == 1:
            self.board[row][col]='B'
        self.flip(row,col)
        self.turn = self.turn+1


    #untuk memutar keping setelah melangkah
    def flip(self, row, col):
        if (self.side == 0):
            #flip around
            for delta_row in range (-1,2):
                for delta_col in range (-1,2):
                    if self.is_valid_coordinate(row+delta_row, col+delta_col) and not (delta_col == 0 and delta_row == 0):
                        if (self.board[row+delta_row][col + delta_col]=='B'):
                            if self.is_valid_coordinate(row+2*delta_row, col + 2*delta_col) and self.board[row+2*delta_row][col + 2*delta_col] =='W':
                                self.board[row+delta_row][col + delta_col] ='W'

        elif (self.side ==1):
            #flip around
            for delta_row in range (-1,2):
                for delta_col in range (-1,2):
                    if self.is_valid_coordinate(row+delta_row, col+delta_col) and not (delta_col == 0 and delta_row == 0):
                        if (self.board[row+delta_row][col + delta_col]=='W'):
                            if self.is_valid_coordinate(row+2*delta_row, col + 2*delta_col) and self.board[row+2*delta_row][col + 2*delta_col] =='B':
                                self.board[row+delta_row][col + delta_col] ='B'


    #Untuk mengecek apakah sudah tidak ada langkah yang valid. jika bernilai true, maka "side" saat ini tidak melangkah
    def skip(self):
        if(len(self.legal_move) == 0):
            self.numb_of_skip = self.numb_of_skip + 1
            return True
        else:
            return False

    #Untuk mengecek apabila permainan telah berakhir
    def end(self):
        if(self.turn == self.cols*self.rows -4):
            return True
        else :
            return False

    #Menghasilkan banyaknya keping dari White dan Black dalam bentuk tuple : (White, Black)
    def score(self):
        score_W = 0
        score_B = 0
        for row in range (self.rows):
            for col in range (self.cols):
                if (self.board[row][col]=='W'):
                    score_W = score_W +1
                elif (self.board[row][col]=='B'):
                    score_B = score_B +1
        return (score_W, score_B)


    #untuk validasi apakah move (row,col) adalah valid
    def is_valid(self, row, col):
        langkah = (row,col)
        if (langkah in self.legal_move ):
            return True
        else :
            return False

    #Membentuk papan permainan
    def draw(self):
        print(' ', end = '  ')
        for i in range (self.cols) :
            print(i, end='  ')
        print()

        for row in range (self.rows):
            print(row , end = '  ')
            for col in range (self.cols):
                if( (row ,col) in self.legal_move) :
                    print("?", end = '  ')
                else :
                    print(self.board[row][col], end ='  ')
            print()

    #Mengembalikan langkah yang diambil agent secara random
    def Dumb_agent(self):
        rand = random.randint(0, len(self.legal_move)-1)
        move = self.legal_move[rand]
        return move


    def winner(self):
        if(self.end() or self.numb_of_skip == 2):
            hasil = self.score()
            putih = hasil[0]
            hitam = hasil[1]
            if(putih>hitam):
                return 'WHITE WIN'
            elif(putih<hitam):
                return  'BLACK WIN'
            elif(putih==hitam):
                'DRAW'

    def main_withoutGUI(self):
        while(not self.end() and not self.numb_of_skip >=2):
            moves = self.search_legal_move()
            self.legal_move = moves
            self.draw()
            score = self.score()
            print("Score :")
            print("WHITE = ", score[0] )
            print("BLACK = ", score[1])
            if(self.side == 0):
                if(not self.skip()):
                    print ("PLAYER move")
                    r = int(input("ROW = "))
                    c = int(input("COL = "))
                    while ( not self.is_valid(r, c)):
                        print("Input tidak valid")
                        r = int (input("ROW = "))
                        c = int (input("COL = "))
                    self.move(r, c)
                    self.numb_of_skip = 0
                    self.change_side()
                else :
                    print("PLAYER SKIP")
                    self.change_side()
            else :
                if (not self.skip() ):
                    agent_move = self.Dumb_agent()
                    print("AI MOVE = ", end ='')
                    print(agent_move)
                    self.move(agent_move[0], agent_move[1])
                    self.numb_of_skip = 0
                    self.change_side()
                else :
                    print("AGENT SKIP")
                    self.change_side()

            print()
            print("-------------------------------------------------------------------")
        print()
        print("GAME OVER")
        print((self.winner()))


test = othello(8,8)
test.main_withoutGUI()

