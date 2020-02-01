import uuid
# from game_server import *
# from server import *
import json
entities = {}
building1 = None
building2 = None
MAX_HEALTH = {
    "building": 10000,
    "generator": 100,
    "player": 100,
    "arrow": 1,
    "wall": 1,
}
INIT_BUILDING_HEALTH = 100
GENERATOR_PRICE = 100


class Entity():
    def __init__(self, type: str, team: str, x: float, y: float, z: float):
        self.type = type
        self.team = team
        self.x = x
        self.y = y
        self.z = z
        self.rotation = 0
        self.uuid = uuid.uuid4()
        while self.uuid in entities:
            self.uuid = uuid.uuid4()

        self.health = MAX_HEALTH[self.type]
        if self.type == "building":
            self.health = INIT_BUILDING_HEALTH

        entities[self.uuid] = self

    def kill(self):
        if self.type == "player":
            self.alive = False
            self.respawn()

        else:
            del entities[self.uuid]

        ret = {
            "event": "kill",
            "uuid": self.uuid
        }
        GameServer.get_server_ins().broadcast(json.dumps(ret), None)

    def damage(self, victim: Entity, amount: int) -> bool:
        if victim.type == "wall" or victim.type == "arrow":
            amount = 0
        if victim.type == "generator" and victim.team is None:
            amount = 0
        if self.team == victim.team:
            amount = 0

        victim.health -= amount
        if victim.health <= 0:
            victim.kill()

        if self.type == "arrow":
            self.kill()

        return amount > 0

    def send_spawn(self):
        ret = {
            "event": "spawn",
            "type": self).type,
            "uuid": self).uuid,
            "team": self).team,
            "x": self).x,
            "y": self).y,
            "z": self).z
        }
        GameServer.get_server_ins().broadcast(json.dumps(ret), None)

    def send_move(self):
        ret={
            "event": "move",
            "uuid": self.uuid,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "rotation": self.rotation
        }
        GameServer.get_server_ins().broadcast(json.dumps(ret), sender)


class Player(Entity):
    def __init__(self, name: str, team: str, x: float, y: float, z: float):
        super(Player, self).__init__("player", team, x, y, z)
        self.name=name
        self.resource=0
        self.weapon=0
        self.alive=True
        self.item={
            "generator": 0
        }

    def respawn(self):
        self.alive=True

        ret={
            "event": "spawn",
            "type": "player",
            "uuid": self.uuid,
            "team": self.team,
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
        GameServer.get_server_ins().broadcast(json.dumps(ret), None)

    def send_stats(self):
        ret={
            "event": "stats",
            "resource": self.resource,
            "item": self.item
        }
        GameServer.get_server_ins().broadcast(json.dumps(ret), None)


class Generator(Entity):
    def __init__(self, type: str, team: str, x: float, y: float, z: float):
        super(Generator, self).__init__(type, team, x, y, z)
        self.resource=0


def get_player_list():
    return list(k for k in entities if entities[k].type == "player")


def get(uuid) -> Entity:
    return entities[uuid]


def get_player(uuid) -> Player:
    return entities[uuid]

def get_building(team: str) -> Entity:
    return building1 if building1.team == team else building2


def get_generator(uuid) -> Generator:
    return entities[uuid]
