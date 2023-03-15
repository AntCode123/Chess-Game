#importing modules
import socket, threading, random, pickle


#Server class
class Server:
    def __init__(self):
        self.HOST_NAME = socket.gethostname()
        self.IP_ADDRESS = "localhost"
        self.PORT = 12349
        self.ENCODER = "ascii"
        self.number_of_clients = 0
        self.MAX_CLIENTS = 2
        self.clients = []
        self.sides = [("white", "0"), ("black", "1")]

    #creating the server socket
    def create(self):
        print("Server is running and waitng for connections...")
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.socket.bind((self.IP_ADDRESS, self.PORT))
        self.socket.listen()

    #handling client communication (thread)
    def client_communication(self, client):
        while True:
            try:
                message = client["socket"].recv(1024)
                self.send_client(message)
            except:
                print(f"Client {client['id']} lost.")
                break
            
    #braodcast data to all clients
    def broadcast(self, message):
        for client in self.clients:
            self.transmit(client["socket"], message)

    #sending data to the other client
    def send_client(self, message):
        message = pickle.loads(message)
        for client in self.clients:
            if len(message) == 5 and message[4] != client["id"]:
                message[0] = str(7-(int(message[0])))
                message[1] = str(7-(int(message[1])))
                message[2] = str(7-(int(message[2])))
                message[3] = str(7-(int(message[3])))
                message = pickle.dumps(message)
                client["socket"].send(message)
                break
            elif len(message) == 4 and message[3] != client["id"]:
                message[0] = str(7-(int(message[0])))
                message[1] = str(7-(int(message[1])))
                message = pickle.dumps(message)
                client["socket"].send(message)
                break
            elif len(message) == 3 and message[2] != client["id"]:
                message = pickle.dumps(message)
                client["socket"].send(message)

    #clients establishig a connection with the server
    def establish_connection(self):
        while self.number_of_clients < self.MAX_CLIENTS:
            client, address = self.socket.accept()
            self.number_of_clients += 1
            self.clients.append({"socket":client, "id":str(self.number_of_clients)})
            self.send_player_attributes(client, self.number_of_clients)
            print(f"Connected client: {address}")
        self.start_game()

    #transmitting data
    def transmit(self, client, data):
        header = str(len(data))
        while len(header) < 10:
            header += " "
        client.send(header.encode(self.ENCODER))
        client.send(data.encode(self.ENCODER))

    #sending the players their attibutes
    def send_player_attributes(self, client, ID):
        side = random.choice(self.sides)
        if side[0] == "white": turn = "player"
        else: turn = "opponent"
        self.transmit(client, side[0])
        self.transmit(client, side[1])
        self.transmit(client, str(ID))
        self.transmit(client, turn)
        self.sides.remove(side)

    #starting the game
    def start_game(self):
        message = "playing"
        self.broadcast(message)
        for client in self.clients:
            thread = threading.Thread(target=self.client_communication, args=(client, ))
            thread.start()
            

server = Server()
server.create()
server.establish_connection()





    
