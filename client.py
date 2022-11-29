#------------------------version-2----------------------------
import socket
import threading

nickname = input("Choose Your Nickname:")
if nickname == 'admin':
    password = input("Enter Password for Admin:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect to a host
client.connect(('127.0.0.1',9999))

stop_thread = False

def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break    
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection is Refused !! Wrong Password")
                        stop_thread = True
                # Clients those are banned can't reconnect
                elif next_message == 'BAN':
                    print('Connection Refused due to Ban')
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            print('Error Occured while Connecting')
            client.close()
            break
        
def write():
    while True:
        if stop_thread:
            break
        #Getting Messages
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    # 2 for : and whitespace and 6 for /KICK_
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    # 2 for : and whitespace and 5 for /BAN
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
            else:
                print("Commands can be executed by Admins only !!")
        else:
            client.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()

# ------------------------version-1----------------------------
# import socket
# import threading
# import re

# with open('cred_chatroom.txt' , 'r')  as f:
#     lcred = []
#     txt = f.read()
#     pattern_cred = re.compile(r'\'.*\'')
#     searches = re.finditer(pattern_cred,str(txt))
#     for search in searches:
#         cred = search.group().strip('\'')
#         lcred.append(cred)

# nickname = input("Choose your nickname: ")
# client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
# client.connect((lcred[0] , int(lcred[1])))      

# def receive():
#     while True:
#         try:
#             # Receive Message From Server
#             # If 'NICK' Send Nickname
#             message = client.recv(1024).decode('utf-8')
#             if message == 'NICK':
#                 client.send(nickname.encode('utf-8'))
#             else:
#                 print(message)
#         except:
#             # Close Connection When Error
#             print("An error occured!")
#             client.close()
#             break
# def write():
#     while True:
#         message = f'[{nickname}]: {input("")}'
#         client.send(message.encode('utf-8'))
# # Starting Threads For Listening And Writing
# receive_thread = threading.Thread(target=receive )
# receive_thread.start()

# write_thread = threading.Thread(target=write )
# write_thread.start()