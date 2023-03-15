class Piece:
    def __init__(self, name, typ, rank):
        self.name = name
        self.type = typ
        self.rank = rank

class Pawn:
    def __init__(self, name, typ, rank):
        Piece.__init__(self, name, typ, rank)
        self.first_move_complete = False

    def check_possible_placements(self, a, b, board):
        coords = []
        if not self.first_move_complete:
            if b >= 1 and board[a-1][b-1] != "-" and board[a-1][b-1].type == "opponent": coords.append((a-1, b-1))
            if b < 7 and board[a-1][b+1] != "-" and board[a-1][b+1].type == "opponent": coords.append((a-1, b+1))
            if a >= 1 and board[a-1][b] == "-": coords.append((a-1, b))
            if a >= 2 and board[a-2][b] == "-": coords.append((a-2, b))
        else:
            if b >= 1 and board[a-1][b-1] != "-" and board[a-1][b-1].type == "opponent": coords.append((a-1, b-1))
            if b < 7 and board[a-1][b+1] != "-" and board[a-1][b+1].type == "opponent": coords.append((a-1, b+1))
            if a >= 1 and board[a-1][b] == "-": coords.append((a-1, b))
        return coords

class Knight:
    def __init__(self, name, typ, rank):
        Piece.__init__(self, name, typ, rank)
        
    def check_possible_placements(self, a, b, board):
        coords = []
        increments = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        for i in range(8):
            row = a + increments[i][0]
            col = b + increments[i][1]
            try:
                if board[row][col] == "-": coords.append((row, col))
                elif board[row][col] != "-" and board[row][col].type == "opponent": coords.append((row, col))
            except: continue
        return coords


class Bishop:
    def __init__(self, name, typ, rank):
        Piece.__init__(self, name, typ, rank)

    def check_possible_placements(self, a, b, board, ):
        coords = []
        increments = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for i in range(4):
            row, col = a, b
            while True:
                row += increments[i][0]
                col += increments[i][1]
                if row >= 0 and col >= 0 and row <= 7 and col <= 7:
                    if board[row][col] == "-": coords.append((row, col))
                    else:
                        if board[row][col].type == "opponent":
                            coords.append((row, col))
                            break
                        elif board[row][col].type == "player": break
                else: break
        return coords
    

class Rook:
    def __init__(self, name, typ, rank):
        Piece.__init__(self, name, typ, rank)

    def check_possible_placements(self, a, b, board):
        coords = []
        increments = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for i in range(4):
            row, col = a, b
            while True:
                row += increments[i][0]
                col += increments[i][1]
                if row >= 0 and col >= 0 and row <= 7 and col <= 7:
                    if board[row][col] == "-": coords.append((row, col))
                    else:
                        if board[row][col].type == "opponent":
                            coords.append((row, col))
                            break
                        elif board[row][col].type == "player": break
                else: break
        return coords
    
class Queen:
    def __init__(self, name, typ, rank):
        Piece.__init__(self, name, typ, rank)

    def check_possible_placements(self, a, b, board, ):
        coords = []
        increments = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for i in range(8):
            row, col = a, b
            while True:
                row += increments[i][0]
                col += increments[i][1]
                if row >= 0 and col >= 0 and row <= 7 and col <= 7:
                    if board[row][col] == "-": coords.append((row, col))
                    else:
                        if board[row][col].type == "opponent":
                            coords.append((row, col))
                            break
                        elif board[row][col].type == "player": break
                else: break
        return coords

class King:
    def __init__(self, name, typ, rank):
        Piece.__init__(self, name, typ, rank)
        
    def check_possible_placements(self, a, b, board):
        coords = []
        if b >= 1 and a >= 1 and board[a-1][b-1] == "-": coords.append((a-1, b-1))
        if b < 7 and a >= 1 and board[a-1][b+1] == "-": coords.append((a-1, b+1))
        if b >= 1 and a < 7 and board[a+1][b-1] == "-": coords.append((a+1, b-1))
        if b < 7 and a < 7 and board[a+1][b+1] == "-": coords.append((a+1, b+1))
        if a >= 1 and board[a-1][b] == "-": coords.append((a-1, b))
        if a < 7 and board[a+1][b] == "-": coords.append((a+1, b))
        if b >= 1 and board[a][b-1] == "-": coords.append((a, b-1))
        if b < 7 and board[a][b+1] == "-": coords.append((a, b+1))
        
        if b >= 1 and a >= 1 and board[a-1][b-1] != "-" and board[a-1][b-1].type == "opponent": coords.append((a-1, b-1))
        if b < 7 and a >= 1 and board[a-1][b+1] != "-" and board[a-1][b+1].type == "opponent": coords.append((a-1, b+1))
        if b >= 1 and a < 7 and board[a+1][b-1] != "-" and board[a+1][b-1].type == "opponent": coords.append((a+1, b-1))
        if b < 7 and a < 7 and board[a+1][b+1] != "-" and board[a+1][b+1].type == "opponent": coords.append((a+1, b+1))
        if a >= 1 and board[a-1][b] != "-" and board[a-1][b].type == "opponent": coords.append((a-1, b))
        if a < 7 and board[a+1][b] != "-" and board[a+1][b].type == "opponent": coords.append((a+1, b))
        if b >= 1 and board[a][b-1] != "-" and board[a][b-1].type == "opponent": coords.append((a, b-1))
        if b < 7 and board[a][b+1] != "-" and board[a][b+1].type == "opponent": coords.append((a, b+1))
        
        return coords

