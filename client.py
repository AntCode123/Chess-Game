#importing modules
import socket, threading, pygame, sys, pickle
from pieces import *

#window setup
pygame.init()
WN = pygame.display.set_mode((600, 600))
CLOCK = pygame.time.Clock()


#Client class
class Client:
    def __init__(self):
        self.HOST_NAME = socket.gethostname()
        self.SERVER_IP_ADDRESS = "localhost"
        self.PORT = 12349
        self.ENCODER = "ascii"

    #creating client socket
    def create(self):
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.socket.connect((self.SERVER_IP_ADDRESS, self.PORT))
        print(f"Connected to {self.SERVER_IP_ADDRESS}")

    #receiving piece coordinates from server
    def receive_coordinates(self):
        while True:
            message = client.socket.recv(1024)
            message = pickle.loads(message)
            if len(message) == 5:
                a, b, c, d = int(message[0]), int(message[1]), int(message[2]), int(message[3])
                player.board[a][b],  player.board[c][d] = '-',  player.board[a][b] 
                player.turn = "player"
            elif len(message) == 4:
                a, b, check = int(message[0]), int(message[1]), bool(message[2])
                player.check_coords = (a, b)
                player.in_check = check
            else: game.result, game.state = message[0], message[1]
            game.check_mate()

            
#Player class
class Player:
    def __init__(self):
        self.username = ""
        self.username_size = 0
        self.username_x = 0
        self.select_piece = False
        self.coords = []
        self.possible_coords = []
        self.piece = None
        self.in_check = False
        self.turn = None
        self.valid_castle = True
        self.board_orientation = [[[Rook("rook", "opponent", 4), Knight("knight", "opponent", 3), Bishop("bishop", "opponent", 3), Queen("queen", "opponent", 9), King("king", "opponent", None), Bishop("bishop", "opponent", 3), Knight("knight", "opponent", 3), Rook("rook", "opponent", 4)],
                                   [Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1)],
                                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                                   [Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1)],
                                   [Rook("rook", "player", 4), Knight("knight", "player", 3), Bishop("bishop", "player", 3), Queen("queen", "player", 9), King("king", "player", None), Bishop("bishop", "player", 3), Knight("knight", "player", 3), Rook("rook", "player", 4)]],
                                  
                                  [[Rook("rook", "opponent", 4), Knight("knight", "opponent", 3), Bishop("bishop", "opponent", 3), King("king", "opponent", None), Queen("queen", "opponent", 9), Bishop("bishop", "opponent", 3), Knight("knight", "opponent", 3), Rook("rook", "opponent", 4)],
                                   [Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1), Pawn("pawn", "opponent", 1)],
                                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                                   [Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1), Pawn("pawn", "player", 1)],
                                   [Rook("rook", "player", 4), Knight("knight", "player", 3), Bishop("bishop", "player", 3), King("king", "player", None), Queen("queen", "player", 9), Bishop("bishop", "player", 3), Knight("knight", "player", 3), Rook("rook", "player", 4)]]]

    #receiving data from server
    def receive_data(self):
        buffer = int(client.socket.recv(10).decode(client.ENCODER))
        data = client.socket.recv(buffer).decode(client.ENCODER)
        return data

    #initialising player attributes received from server
    def initialise_attributes(self):
        self.colour = self.receive_data()
        self.board = self.board_orientation[int(self.receive_data())]
        self.ID = self.receive_data()
        self.turn = self.receive_data()

    #moving a piece and sending the coordinates to the server
    def move(self, i, j):
        self.send_coordinates(self.coords[0], self.coords[1], i, j)
        a, b, c, d = self.coords[0], self.coords[1], i, j
        self.board[a][b],  self.board[c][d] = '-',  self.board[a][b]
        self.turn = "opponent"
        if player.piece.name == "pawn": player.piece.first_move_complete = True
        elif  player.piece.name == "king": player.valid_castle = False
        elif player.piece.name == "rook": player.valid_castle = False
        if self.in_check: self.in_check = False
        self.select_piece = False
        self.piece = None
        game.find_check()

    #sending the server coordinate data
    def send_coordinates(self, a, b, c, d):
        coords = [a, b, c, d, player.ID]
        message = pickle.dumps(coords)
        client.socket.send(message)

    #display check
    def display_check(self):
        if self.in_check:
            x = self.check_coords[1] * 75
            y = self.check_coords[0] * 75
            pygame.draw.rect(WN, (255, 0, 0), (x, y, 75, 75), 4)

    #selecting a piece
    def select(self, mx, my):
        if mx >= 0 and mx <= 600 and my >= 0 and my <= 600:
            i, j = game.convert_index(mx, my)
            if self.board[i][j] != "-" and self.board[i][j].type == "player" and not self.select_piece:
                self.coords.clear()
                self.select_piece = True
                self.coords.append(i)
                self.coords.append(j)
                self.select_coords = (mx, my)
                self.piece = self.board[i][j]
                self.possible_coords = self.piece.check_possible_placements(self.coords[0], self.coords[1], self.board)

    #castling
    def castle(self, i, j):
        if self.colour == "white":
            if j == 7 and self.board[7][6] == "-" and self.board[7][5] == "-": a, b, c, d, e, f, g, h = 7, 4, 7, 6, 7, 7, 7, 5
            if j == 0 and self.board[7][1] == "-" and self.board[7][2] == "-" and self.board[7][3] == "-":
                print("yes")
                a, b, c, d, e, f, g, h = 7, 4, 7, 2, 7, 0, 7, 3
        else:
            if j == 7 and self.board[7][6] == "-" and self.board[7][5] == "-" and self.board[7][4] == "-": a, b, c, d, e, f, g, h = 7, 3, 7, 5, 7, 7, 7, 4
            if  j == 0 and self.board[7][1] == "-" and self.board[7][2] == "-": a, b, c, d, e, f, g, h = 7, 3, 7, 1, 7, 0, 7, 2
        self.send_coordinates(a, b, c, d)
        self.send_coordinates(e, f, g, h)
        self.board[a][b], self.board[c][d] = self.board[c][d], self.board[a][b]
        self.board[e][f], self.board[g][h] = self.board[g][h], self.board[e][f]
        self.turn = "opponent"
        self.select_piece = False
        self.piece = None
        self.valid_castle = False

#Game class
class Game:
    def __init__(self):
        self.state = "waiting"
        self.f1 = pygame.font.SysFont("consolas", 120, True)
        self.f2 = pygame.font.SysFont("consolas", 50, True)
        self.f3 = pygame.font.SysFont("consolas", 40, True)
        self.board = [[1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1]]

    #rendering text
    def render_text(self, font, text, x, y):
        text = font.render(f"{text}", True, (255, 255, 255))
        WN.blit(text, (x, y))

    #displaying text
    def display_text(self):
        self.render_text(self.f1, "Welcome To", 80, 40)
        self.render_text(self.f1, "Chess", 200, 120)
        self.render_text(self.f2, "Enter Username", 135, 240)
        self.render_text(self.f3, "Press Enter to connect", 115, 400)
        self.render_text(self.f3, player.username, player.username_x, 320)

    #displaying text box
    def display_box(self):
        pygame.draw.rect(WN, (255, 255, 255), (150, 300, 300, 75), 5)

    #starting the game
    def start(self):
        self.state = player.receive_data()

    #getting mouse coordinates
    def get_mouse(self):
        mouse = pygame.mouse.get_pos()
        return mouse[0], mouse[1]

    #converting to index positions
    def convert_index(self, mx, my):
        mx = mx // 75 * 75
        my = my // 75 * 75
        return my // 75, mx // 75

    #displaying result
    def display_result(self):
        if self.result == "winner":
            game.render_text(game.f1, "You Won", 60, 230)
        else: game.render_text(game.f1, "Defeated", 40, 230)

    #event handler
    def events(self):
        mx, my = self.get_mouse()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game.state != "game over":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and player.turn == "player": player.select(mx, my)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and player.turn == "player":
                        i, j = self.convert_index(mx, my)
                        self.check_valid_placement(i, j)
                    
    #checking for valid piece placement
    def check_valid_placement(self, i, j):
        if (i, j) in player.possible_coords: player.move(i, j)
        elif player.board[i][j] != "-" and player.board[i][j].name == "rook" and player.board[i][j].type == "player" and player.valid_castle: player.castle(i, j)
        else:
            player.select_piece = False
            player.piece = None

    #checking for a 'check'
    def find_check(self):
        check = False
        for i in range(8):
            if check: break
            for j in range(8):
                if check: break
                elif player.board[i][j] != "-" and player.board[i][j].type == "player":
                    coords = player.board[i][j].check_possible_placements(i, j, player.board)
                    for coord in coords:
                        if player.board[coord[0]][coord[1]] != "-" and player.board[coord[0]][coord[1]].name == "king" and player.board[coord[0]][coord[1]].type == "opponent":
                            print("Opponent is in check")
                            coords = [i, j, True, player.ID]
                            message = pickle.dumps(coords)
                            client.socket.send(message)
                            check = True
                            break
    #checkmate
    def check_mate(self):
        check_mate = True
        for i in range(8):
            for j in range(8):
                if player.board[i][j] != "-" and player.board[i][j].name == "king" and player.board[i][j].type == "player":
                    check_mate = False
        if check_mate:
            message = ("winner", "game over", player.ID)
            message = pickle.dumps(message)
            client.socket.send(message)
            self.result = "loser"
            self.state = "game over"
            

    #displaying the board
    def display_board(self):
        for i in range(8):
            for j in range(8):
                x = j * 75
                y = i * 75
                if self.board[i][j] == 1: colour = (251, 214, 172)
                else: colour = (122, 40, 6)
                pygame.draw.rect(WN, colour, (x, y, 75, 75))

    #displaying the pieces
    def display_pieces(self):
        for i in range(8):
            for j in range(8):
                x = 37.5 + j * 75
                y = 37.5 + i * 75
                self.load_image(x, y, i, j)

    #loading the piece image
    def load_image(self, x, y, i, j):
        filename, piece = self.get_file_name(x, y, i, j)
        if filename != None:
            if piece != player.piece:
                image = pygame.image.load(filename)
                width = image.get_width()
                height = image.get_height()
                x -= width / 2
                y -= width / 2 
                WN.blit(image, (x, y))

    #getting the filename of a piece image
    def get_file_name(self, x, y, i, j):
        filename = ""
        if player.board[i][j] != '-':
            if player.board[i][j].type == "player":
                if player.colour == "white": filename += "w"
                else: filename += "b"
            else:
                if player.colour == "white": filename += "b"
                else: filename += "w"     
            if player.board[i][j].name == "king": filename += "k"
            elif player.board[i][j].name == "queen": filename += "q"
            elif player.board[i][j].name == "rook": filename += "r"
            elif player.board[i][j].name == "bishop": filename += "b"
            elif player.board[i][j].name == "pawn": filename += "p"
            elif player.board[i][j].name == "knight": filename += "n"
            return filename + ".png", player.board[i][j]
        else: return None, None

    #displaying the selected piece
    def display_selected_piece(self, mx, my):
        if player.select_piece:
            i, j = self.convert_index(mx, my)
            pygame.draw.rect(WN, (170, 170, 170), (j * 75, i * 75, 75, 75), 4)
            if player.colour == "white":
                if player.piece.name == "pawn": image = pygame.image.load("wp.png")
                elif player.piece.name == "knight": image = pygame.image.load("wn.png")
                elif player.piece.name == "bishop": image = pygame.image.load("wb.png")
                elif player.piece.name == "rook": image = pygame.image.load("wr.png")
                elif player.piece.name == "queen": image = pygame.image.load("wq.png")
                elif player.piece.name == "king": image = pygame.image.load("wk.png")
            else:
                if player.piece.name == "pawn": image = pygame.image.load("bp.png")
                elif player.piece.name == "knight": image = pygame.image.load("bn.png")
                elif player.piece.name == "bishop": image = pygame.image.load("bb.png")
                elif player.piece.name == "rook": image = pygame.image.load("br.png")
                elif player.piece.name == "queen": image = pygame.image.load("bq.png")
                elif player.piece.name == "king": image = pygame.image.load("bk.png")

            width = image.get_width()
            height = image.get_height()
            WN.blit(image, (mx - width/2, my - width/2))
        
    #displaying all possible positions where a selected piece can go
    def display_possible_positions(self):
        if player.select_piece:
            for coords in player.possible_coords:
                x = coords[1] * 75
                y = coords[0] * 75
                if player.board[coords[0]][coords[1]] != "-" and player.board[coords[0]][coords[1]].type == "opponent":
                    pygame.draw.rect(WN, (118, 231, 45), (x, y, 75, 75), 4)
                else:
                    pygame.draw.rect(WN, (227, 243, 69), (x, y, 75, 75))
        
    #rendering objects to the screen
    def render(self):
        mx, my = self.get_mouse()
        pygame.draw.rect(WN, (180, 100, 20), (0, 0, 600, 600), 4)
        self.display_board()
        self.display_pieces()
        player.display_check()
        self.display_possible_positions()
        self.display_selected_piece(mx, my)
        if game.state == "game over": self.display_result()
        
    #updating the window
    def update(self):
        pygame.display.update()
        WN.fill((0, 0, 0))
        CLOCK.tick(30)

    #main game loop
    def mainloop(self):
        while True:
            self.events()
            self.render()
            self.update()

#start screen
game = Game()
image = pygame.image.load("background.jpg")
WN.blit(image, (-200, 0))
game.render_text(game.f1, "CHESS.PY", 30, 50)
game.render_text(game.f3, "WAITING FOR CONNECTION...", 25, 400)
pygame.display.update()

player = Player()
client = Client()
client.create()
player.initialise_attributes()
game.start()


#checking to start the game
if game.state == "playing":
    thread = threading.Thread(target=client.receive_coordinates, args=())
    thread.start()
    game.mainloop()

#closing the client socket
client.socket.close()

