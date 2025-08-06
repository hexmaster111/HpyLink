import brainflow
import keyboard
from pprint import pprint


from brainflow import BoardIds
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
import time



board_id = BoardIds.CROWN_BOARD.value; # or BoardIds.NOTION_2_BOARD.value or BoardIds.NOTION_1_BOARD.value
params = BrainFlowInputParams();
params.board_id = board_id;
BoardShim.enable_dev_board_logger();
board = BoardShim(board_id, params);

BoardShim.get_board_descr(board_id);

board.prepare_session();
board.start_stream();



while True:
    while board.get_board_data_count() < 250:
        time.sleep(0.005);
    
    data = board.get_board_data();
    pprint(data);
    DataFilter.write_file(data, 'data.csv', 'w');
    if(keyboard.is_pressed('q')):
        print("Quitting");
        break;


board.stop_stream();
board.release_session();

