from base_state import base_state
from waiting_room import WaitingRoomState
class state_handler():
    state = None
    state_lib = {
        "WaitingRoom":WaitingRoomState()
    }
    __ins__ = None

    @staticmethod
    def get_instance():
        if state_handler.__ins__ == None:
            state_handler.__ins__ = state_handler("WaitingRoom")
        return state_handler.__ins__

    def __init__(self , init:str):
        self.transition_to(init)

    def transition_to(self , state:str):
        self.state = self.state_lib[state]
    
    def recv(self , s:str)->str:
        tran = str(self.state.update(s))
        if tran != "":
            self.transition_to(self.state_lib[tran])
        