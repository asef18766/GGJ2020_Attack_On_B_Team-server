import random
from base_state import BaseState
from entity import *
import entity
from game_server import GameServer
from uuid import UUID
import json


class WaitingRoomState(BaseState):
    # team names
    TEAM1 = "yee"
    TEAM2 = "OwO"
    MAP_WIDTH
    MAP_HEIGHT
    BLOCK_WIDTH

    # the player that game requires
    MAX_PLAYER = 8

    # key: uuid
    # value: {"playerName":str , "ready":boolean , "team":int}
    players = {}
    players_ready = {}
    player_entered = {}
    server = GameServer.get_server_ins()

    STILL_WAITING = 0
    CLIENT_LOADING = 1
    ALL_READY = 2
    status_code = 0

    def __init__(self):
        pass

    # find wheather player existed
    def check_player(self, i: UUID, player_name: str)->bool:
        if i not in get_player_list():
            return False
        player = get_player(i)
        player.name = player_name
        self.players.update({
            player.uuid: player
        })
        self.players_ready.update({
            player.uuid: False
        })
        self.player_entered.update({
            player.uuid: False
        })
        return True

    # set one player's status
    def set_ready(self, uuid):
        self.players_ready[uuid] = True

    def set_enter(self, uuid):
        self.player_entered[uuid] = True
    # partition player into to team

    def partition(self):
        print("partitioning...")
        first_team = 0
        while first_team < self.MAX_PLAYER:
            choice = self.players.keys()[random.randint(0, 7)]
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
    def check_if_ready(self):
        for k in list(self.players_ready.keys()):
            if self.players_ready[k] == False:
                return False
        self.partition()
        print("able to entered!!")
        return True

    # aka
    def check_if_enter(self):
        for k in list(self.player_entered.keys()):
            if self.player_entered[k] == False:
                return False

        print("start!!")
        return True

    def dispatch(self, uuid: UUID, event: dict):
        if s["event"] == "connect":
            res = {}
            if self.check_player(uuid, s["playerName"]):
                res.update({
                    "event": "connect",
                    "playerName": s["playerName"],
                    "success": True,
                    "uuid": uuid.hex()
                })
            else:
                res.update({
                    "event": "connect",
                    "playerName": s["playerName"],
                    "success": False,
                    "uuid": ""
                })
            self.server.send(json.dumps(res), uuid)

        if s["event"] == "ready":
            self.set_ready(uuid)
        if s["event"] == "entered_game":
            self.set_enter(uuid)

    def send_waiting(self):
        msg = {
            "event": "waiting",
            "players": []
        }
        for i in get_player_list():
            msg["players"].append({
                "uuid": i.hex(),
                "playerName": get_player(i).name,
                "ready": self.players_ready[i]
            })
        self.server.broadcast(json.dumps(msg), None)

    def update(self, s: dict)->str:
        for k in s.keys():
            self.dispatch(k, s[k])

        # broadcast waiting event
        self.send_waiting()

        if self.status_code == self.STILL_WAITING:
            if self.check_if_ready():
                msg = {
                    "event": "enterGame"
                }
                self.server.broadcast(json.dumps(msg), None)
                self.status_code = self.CLIENT_LOADING

        elif self.status_code == self.CLIENT_LOADING:
            if self.check_if_enter():
                for i in get_player_list():
                    msg = {
                        "event": "start_game",
                        "team": get_player(i).team
                    }
                    self.server.send(json.dumps(msg), i)
                self.status_code = self.ALL_READY

        elif self.status_code == self.ALL_READY:
            print("entered stage")
            return "Stage"

    def generate_map():
        building1 = Entity("building", TEAM1,
                           -self.MAP_WIDTH//2*self.BLOCK_WIDTH, 0, 0)
        building1.send_spawn()
        entity.building1 = building1

        building2 = Entity("building", TEAM2,
                           self.MAP_WIDTH//2*self.BLOCK_WIDTH, 0, 0)
        building2.rotation = 180
        building2.send_spawn()
        building2.send_move()
        entity.building2 = building2

        for uuid in get_player_list:
            player = get_player(uuid)
            building = get_building(player.team)
            player.x = building.x
            player.y = building.y
            player.z = building.z
            player.send_spawn()

        for i in range(3):
            generator = Entity("generator", None, 0, self.BLOCK_WIDTH *
                               (self.MAP_HEIGHT//2-i*self.MAP_HEIGHT//2), 0)
            generator.send_spawn()

        for i in range(self.MAP_HEIGHT*self.MAP_WIDTH//4):
            x = random.randint(self.MAP_WIDTH*3//4, -self.MAP_WIDTH*3//4)
            y = random.randint(self.MAP_HEIGHT, -self.MAP_HEIGHT)
            wall = Entity("wall", None, x, y, 0)
            wall.send_spawn()

        for i in range(self.MAP_HEIGHT*2):
            x = i % self.MAP_HEIGHT - self.MAP_HEIGHT//2
            y = self.MAP_WIDTH*(1 if i < self.MAP_HEIGHT else -1)//2
            wall = Entity("wall", None, x, y, 0)
            wall.send_spawn()

        for i in range(self.MAP_WIDTH*2):
            x = i % self.MAP_WIDTH - self.MAP_WIDTH//2
            y = self.MAP_HEIGHT*(1 if i < self.MAP_WIDTH else -1)//2
            wall = Entity("wall", None, x, y, 0)
            wall.send_spawn()
