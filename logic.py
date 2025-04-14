#Game logic for othello
#Import ini aja untuk buat agent

import copy

class logic :

    def is_valid_coordinate(self, row,col,rows_size, cols_size):
        if(col>=0 and col<cols_size and row>=0 and row< rows_size):
            return True
        else :
            return False

    #untuk mengecek apabila terdapat sebuah line dari keping opponent side yang dapat diflip dari koordinat (row,col)
    def checK_lineblock(self, board, row, col, rows_size, cols_size, direction, opponent):

        list_temp = []
        list = []
        r = direction[0] + row
        c = direction[1] + col
        found_end = False
        if(opponent == 0):
            tile = 'W'
        elif(opponent == 1):
            tile = 'B'

        while self.is_valid_coordinate(r, c, rows_size, cols_size)  and not (found_end) and not (board[r][c]=="-"):

            if(board[r][c]!=tile):
                found_end = True
            elif (board[r][c]==tile):
                list_temp.append((r,c))
                #print(row, end=" ")
                #print(col, end=" ")
                #print(direction, end = " ")
                #print(list_temp)

            r = direction[0] + r
            c = direction[1] + c

        if(found_end):
            list = list_temp
        return list

    # input (array papan game, size row, size col, sisi yang akan melangkah)
    # output -> daftar koordinat yang dapat ditempati oleh side yang akan melangkah
    def search_legal_move(self, board, size_row, size_col, side):
        list = []

        for row in range (size_row):
            for col in range (size_col):
                if (board[row][col] == '-'):
                    check_again_around = True
                    if (side == 0):
                        #look around
                        for delta_row in range (-1,2):
                            for delta_col in range (-1,2):
                                if  not (delta_col == 0 and delta_row == 0):
                                    check = self.checK_lineblock(board, row, col, size_row, size_col, (delta_row,delta_col), 1)

                                    if(len(check) > 0):
                                        list.append((row,col))
                                        check_again_around = False
                                        break

                            if (not check_again_around):
                                break

                    if (side == 1):
                        #look around
                        for delta_row in range (-1,2):
                            for delta_col in range (-1,2):
                                if  not (delta_col == 0 and delta_row == 0):
                                    check = self.checK_lineblock(board, row, col, size_row, size_col, (delta_row,delta_col), 0)
                                    if(len(check) > 0):
                                        list.append((row,col))
                                        check_again_around = False
                                        break

                            if (not check_again_around):
                                break

        return list


    # input (array papan game, row, col, size row, size col, sisi yang akan melangkah)
    # output -> daftar koordinat yang dapat diflip oleh side yang akan melangkah
    def search_list_to_be_flipped(self, board, row, col, size_row, size_col, side):
        location = []
        if (side == 0):
            #look around
            for delta_row in range (-1,2):
                for delta_col in range (-1,2):
                    if  not (delta_col == 0 and delta_row == 0):
                        check = self.checK_lineblock(board, row, col, size_row, size_col, (delta_row,delta_col), 1)
                        if(len(check) > 0):
                            location.extend((check))

        if (side == 1):
            #look around
            for delta_row in range (-1,2):
                for delta_col in range (-1,2):
                    if  not (delta_col == 0 and delta_row == 0):
                        check = self.checK_lineblock(board, row, col, size_row, size_col, (delta_row,delta_col), 0)
                        if(len(check) > 0):
                            location.extend((check))

        return location


    #side = sisi yang akan melangkah, row dan col = coordinat keping akan ditempatkan
    def flip_now(self, board, row, col, size_row, size_column, side):
        location = []
        location = self.search_list_to_be_flipped(board, row, col, size_row, size_column, side)
        if (len(location)>0):
            for coor in location:
                if (side == 0):
                    board[coor[0]][coor[1]] = "W"
                elif (side == 1) :
                    board[coor[0]][coor[1]] = "B"

        return copy.deepcopy(board)

    def score(self,board,size_row, size_column,side):
        
        n_score = 0
        check = 'B'

        if (side == 0):
            check = 'W'
        else:
            check = 'B'

        for row in range (size_row):
            for col in range (size_column):
                if (board[row][col]==check):
                    n_score = n_score +1

        return n_score
