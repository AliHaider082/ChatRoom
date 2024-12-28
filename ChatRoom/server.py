import threading #multithreading-allows two things to happen once
import socket #network communication- end-point for sending and recieving data. Allows communication between server and client.

host = '10.0.0.164' #localhost
port = 55555 #unused port 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPV4, TCP Connection
server.bind((host,port)) #Binds the host "10.0.0.164" to the port "55555"
server.listen() #Since the host and port is binded, it opens and starts looking for any connections. 

clients = []
nicknames = []

#Broadcast function which will broadcast a message to every client on the server.
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024) #while the client is connected
            broadcast(message) #broadcast clients message
        except: #if we recieve an error while broadcasting | cuts connection from client and terminates loops
            index = client.index(client) #index needed to remove client's nickname from list
            client.remove(client) #removes client's connection status from the server
            client.close() #cuts connection between server and client
            nickname = nicknames[index] 
            nicknames.remove(nickname) #removes the client nickname from itself, to allow someone else to have it or for the client to reconnect and use it.
            broadcast(f'{nickname} has left the chat'.encode('ascii')) #self-explanatory
            break #terminates function

def receive():
    while True:
        client, address = server.accept() #allow the client to connect to the server and displays its IP address to server console
        print(f"Connected with {str(address)}") #Sent on the server console

        client.send('NICK'.encode('ascii')) #Allows client to choose a nickname
        nickname = client.recv(1024).decode('ascii') # Server receives client nickname
        nicknames.append(nickname) # Adds clients nickname to nickname list
        clients.append(client) # Adds the client to the client list

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} has joined the chat!'.encode('ascii')) #Broadcast message that client has joined the chatroom with its nickname
        client.send('Connected to the Server'.encode('ascii')) #Sends message to client from server
        
        thread = threading.Thread(target = handle, args =(client,)) #Starts thread to handle connection with client
        thread.start()

print("Server is listening for connections...")
receive()