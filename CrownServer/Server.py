import sys;
import socket;

PORT = 0xD457;

## Crow Device Setup here ##

# Server setup
print("Server starting on port {}".format(PORT));
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server.bind(("0.0.0.0", PORT));
server.listen(1); # 1 connection
print("Server listening, waiting for a connection....");

####### server.accept() Object ########
# (<socket.socket fd=5,
# family=2, type=1, proto=0, 
# laddr=('127.0.0.0', 54359),
# raddr=('127.0.0.1', 43080)>, 
# ('127.0.0.1', 43080))
#######################################

####### client Object #########
# <socket.socket fd=4,
# family=2, type=1, proto=0,
# laddr=('127.0.0.0', 54359),
# raddr=('127.0.0.1', 44680)>
###############################

client, address = server.accept();

print("client:{}".format(client));

print("Waiting for handshake msg!");
client.sendall(b'Nickname?\n>');
clientNickname = client.recv(1024);
print("Connection from user {}".format(clientNickname))
client.sendall("welcome, {}\n>".format(clientNickname).encode('ascii'))

## Server ##
while True:
    data = client.recv(1024);
    if(not data):
        break;
    
    datastr = data.decode("ascii").replace("\n", "");
    
    print(datastr);

    if(datastr == "quit"):
        break;

    print("got " + datastr);

    client.sendall(b">");


client.close();