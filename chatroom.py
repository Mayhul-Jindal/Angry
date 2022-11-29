#------------------------version-2----------------------------
import threading
import socket
# Now this Host is the IP address of the Server, over which it is running.
# I've user my localhost.
host = "127.0.0.1"
port = 9999 # Choose any random port which is not so common (like 80)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Bind the server to IP Address
server.bind((host, port))
#Start Listening Mode
server.listen()
#List to contain the Clients getting connected and nicknames
clients = []
nicknames = []

# 1.Broadcasting Method
def broadcast(message):
    for client in clients:
        client.send(message)

# 2.Recieving Messages from client then broadcasting
def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)  
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command Refused!'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt','a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned by the Admin!')
                else:
                    client.send('Command Refused!'.encode('ascii'))
            else:
                broadcast(message)   # As soon as message recieved, broadcast it.
        
        except:
            if client in clients:
                index = clients.index(client)
                #Index is used to remove client from list after getting diconnected
                client.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(f'{nickname} left the Chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break
# Main Recieve method
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        # Ask the clients for Nicknames
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        # If the Client is an Admin promopt for the password.
        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            # I know it is lame, but my focus is mainly for Chat system and not a Login System
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the Chat'.encode('ascii'))
        client.send('Connected to the Server!'.encode('ascii'))

        # Handling Multiple Clients Simultaneously
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You Were Kicked from Chat !'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked from the server!'.encode('ascii'))

#Calling the main method
print('Server is Listening ...')
recieve()

#------------------------version-1----------------------------
# import socket
# import threading    
# import re

# # reading file contents and getting credentials
# with open('cred_chatroom.txt' , 'r')  as f:
#     lcred = []
#     txt = f.read()
#     pattern_cred = re.compile(r'\'.*\'')
#     searches = re.finditer(pattern_cred,str(txt))
#     for search in searches:
#         cred = search.group().strip('\'')
#         lcred.append(cred)

# # making a server socket
# s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
# s.bind((lcred[0] , int(lcred[1])))
# s.listen(4)

# # Lists For Clients and Their Nicknames
# clients = []
# nicknames = []
# # Sending Messages To All Connected Clients
# def broadcast(message):
#     for client in clients:
#         client.send(message)

# def message_reciever(client):
#     while True:

#         try:
#             # recieving  messages
#             message = client.recv(1024)
#             broadcast(message)
#         except:
#             # Removing And Closing Clients
#             index = clients.index(client)
#             clients.remove(client)
#             client.close()
#             nickname = nicknames[index]
#             broadcast('{} left!'.format(nickname).encode('utf-8'))
#             nicknames.remove(nickname)
#             break
# def connection():
#     while True:
#         client , address = s.accept()
#         print(f'Connection with {address[0]} is established.....')
#         # appending nicknames  and clients
#         client.send('NICK'.encode('utf-8'))
#         nickname = client.recv(1024).decode('utf-8')
#         nicknames.append(nickname)
#         clients.append(client)
#         # broadcasting who has joined our server
#         print(f'{nickname} is connected to  the server')
#         broadcast(f'{nickname} has joined  the room!!'.encode('utf-8'))
#         client.send('Welcome in the group!!'.encode('utf-8'))
#         # threading-----have to  learn yet
#         thread = threading.Thread(target=message_reciever, args=(client,))
#         thread.start()
# print(f'{lcred[0]} is listening....')
# connection()
