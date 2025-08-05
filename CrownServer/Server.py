import sys;
import socket;
import struct;
import array;
import time;

import brainflow

from brainflow import BoardIds
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

PORT = 0xD457;

CROW_CHANNELS = int(10); ## Change me to what reality is

## Crow Device Setup here ##
board_id = BoardIds.CROWN_BOARD.value # or BoardIds.NOTION_2_BOARD.value or BoardIds.NOTION_1_BOARD.value
params = BrainFlowInputParams ()
params.board_id = board_id
BoardShim.enable_dev_board_logger ()
board = BoardShim (board_id, params)
board.prepare_session ()
board.start_stream ()

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



## Server... i dont handle closing or anything.... try catch this and then close after? ##
try:
    while True:
        data = board.get_board_data()
        #data is now 
        # [
        #   sample1[Sensor a, sensor b, sensor c], 
        #   sample2[Sensor a, sensor b, sensor c], 
        #   sample3[Sensor a, sensor b, sensor c], 
        # ]

        # Flatten the data and prepend the current time
        current_time = time.time()
        flat_data = data.flatten()
        sample_array = array.array('d', [current_time] + flat_data.tolist())



        client.sendall(sample_array.tobytes());    
        sample_array[0] += .001; # hacky, use some time method to get the time sence program start
        time.sleep(.001); # likely not needed for real thing.

except:
    print(""); 
finally:
    client.close();

board.stop_stream();
board.release_session();