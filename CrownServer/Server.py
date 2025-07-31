import sys;
import socket;
import struct;
import array;
import time;

PORT = 0xD457;

CROW_CHANNELS = int(10); ## Change me to what reality is

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

print("Client Connected!{}".format(client));

tmp = CROW_CHANNELS.to_bytes(4, "little");

client.sendall(tmp);

# First element in the array is time sence the program started in sec 
sample_array = array.array('d', [0, 1.123, 2.123, 3.123, 4.123, 5.123, 6.123, 7.123, 8.123, 9.123, 10.123]);

## Server... i dont handle closing or anything.... try catch this and then close after? ##
try:

    while True:
        client.sendall(sample_array.tobytes());    
        sample_array[0] += .001; # hacky, use some time method to get the time sence program start
        time.sleep(.001); # likely not needed for real thing.

except:
    print(""); 
finally:
    client.close();


# todo: shutdown the stuff needed to talk to the crow device 
