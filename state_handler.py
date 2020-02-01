from base_state import BaseState
from waiting_room import WaitingRoomState
from stage import Stage
from uuid import UUID
import json
class StateHandler():
    state = None
    state_lib = {
        "WaitingRoom":WaitingRoomState(),
        "Stage":Stage()
    }
    __ins__ = None

    @staticmethod
    def get_instance():
        if StateHandler.__ins__ == None:
            StateHandler.__ins__ = StateHandler("WaitingRoom")
        return StateHandler.__ins__

    def __init__(self , init:str):
        self.transition_to(init)

    def transition_to(self , state:str):
        self.state = self.state_lib[state]
    
    def recv(self ,events:dict):
        tran = str(self.state.update(event))
        if tran != "":
            print("transit to " ,tran)
            self.transition_to(self.state_lib[tran])
        