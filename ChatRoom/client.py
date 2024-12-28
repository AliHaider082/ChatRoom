import socket
import threading

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('10.0.0.164', 55555)) #connecting to the server

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii') # Allows client to recieve messages from server
            if message == 'NICK': #if the server is asking for a nickname
                client.send(nickname.encode('ascii'))
            else:
                print(message) #if not asking for a nickname, the server will print the other message
        except:
            print("An error has occurred!")# if it is nothing other than what was listed before, it prints an error message
            client.close()# closes connection of the client and the server
            break           

def write():
    while True:
        message = f'{nickname}: {input("")}' #Constantly displays this, if a client sends a message, this will come up again, allowing another message to send.
        client.send(message.encode('ascii')) 

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()