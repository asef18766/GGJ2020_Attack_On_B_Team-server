import random
from base_state import BaseState
from entity import Player
from entity import get_player_list
from entity import get_player
from game_server import GameServer
from uuid import UUID

class WaitingRoomState(BaseState):
    # team names
    TEAM1 = "yee"
    TEAM2 = "OwO"
    
    # the player that game requires
    MAX_PLAYER = 8

    # key: uuid
    # value: {"playerName":str , "ready":boolean , "team":int}
    players = {}
    players_ready = {}
    server = GameServer.get_server_ins()
    def __init__(self):
        pass

    # find wheather player existed
    def check_player(self , i:UUID ,player_name:str)->bool:
        if i not in get_player_list():
            return False
        player = get_player(i)
        player.name = player_name
        self.players.update({
            player.uuid:player
        })
        self.players_ready.update({
            player.uuid:False
        })
    
    # set one player's status
    def set_ready(self , uuid):
        self.players_ready[uuid] = True

    # partition player into to team
    def partition(self):
        print("partitioning...")
        first_team = 0
        while first_team < self.MAX_PLAYER:
            choice = self.players.keys()[random.randint(0,7)]
            if self.players[choice].team != "":
                continue
            first_team += 1
            self.players[choice].team = self.TEAM1
         
        for k in list(self.players.keys()):
            if self.players[k].team != "":
                continue
            self.players[k].team = self.TEAM2
        print("partition done , ready to start game")

    # aka
    def check_if_start(self):
        for k in list(self.players_ready.keys()):
            if self.players_ready[k]["ready"] == False:
                return False     
        print("able to start!!")
        self.partition()
        return True

    def dispatch(self , uuid:UUID , event:dict):
        if s["event"] == "connect":
            self.check_player(uuid , s["playerName"])
        if s["event"] == "ready":
            self.set_ready(uuid)
    
    def update(self, s:dict)->str:
        for k in s.keys():
            self.dispatch(k,s[k])
        
        