import time
import brainflow
from brainflow import BoardIds
from brainflow.board_shim import BoardShim, BrainFlowInputParams

def main():
    board_id = BoardIds.CROWN_BOARD.value
    params = BrainFlowInputParams()
    # optionally set ip_port here if needed
    BoardShim.enable_dev_board_logger()
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()

    time.sleep(5)  # wait 5 seconds to collect data

    data = board.get_board_data()
    print(data)

    board.stop_stream()
    board.release_session()

if __name__ == "__main__":
    main()