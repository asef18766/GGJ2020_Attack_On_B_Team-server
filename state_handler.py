from base_state import BaseState
from waiting_room import WaitingRoomState
<<<<<<< HEAD
from stage import Stage
=======
from game_stage import GameStage
>>>>>>> 85f9773fb3fb20d90265df33fbb0bfd50f594530
from uuid import UUID
import json
class StateHandler():
    state = None
    state_lib = {
        "WaitingRoom":WaitingRoomState(),
<<<<<<< HEAD
        "Stage":Stage()
=======
        "GameStage":GameStage()
>>>>>>> 85f9773fb3fb20d90265df33fbb0bfd50f594530
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
        