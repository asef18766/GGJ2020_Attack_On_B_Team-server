from base_state import BaseState
from entity import *
from game_server import GameServer

GENERATOR_COOLDOWN = 10
WILD_GENERATOR_COOLDOWN = 20
MAX_COLLECT = 10


def broadcast(msg: dict, broadcaster: uuid.UUID):
    game_server.GameServer.get_server_ins().broadcast(json.dumps(msg), broadcaster)


def send(msg: dict, id: uuid.UUID):
    game_server.GameServer.get_server_ins().send(json.dumps(msg), id)


class GameStage(BaseState):

    def move(self, sender, data):
        entity = get(data['uuid'])
        entity.x = data['x']
        entity.y = data['y']
        entity.z = data['z']
        entity.rotation = data['rotation']

        ret = {
            "event": "move",
            "uuid": entity.uuid,
            "x": entity.x,
            "y": entity.y,
            "z": entity.z,
            "rotation": entity.rotation
        }
        broadcast(ret, entity.uuid)

    def change_weapon(self, sender, data):
        player = get_player(sender)
        player.weapon = data['choice']
        ret = {
            "event": "change_weapon",
            "uuid": player.uuid,
            "choice": player.weapon
        }
        broadcast(ret, None)

    def attack(self, sender, data):
        ret = {
            "event": "attack",
            "weapon": get_player(sender).weapon,
        }
        broadcast(ret, None)

    def damage(self, sender, data):
        entity.damage(get(data['damager']),
                      get(data['target']), data['amount'])

        ret = {
            "event": "damage",
            "uuid": data['target'],
            "amount": data['amount'],
            "healthLeft": get(data['target']).health
        }
        broadcast(ret, None)

    def spawn(sef, sender, data):
        e = Entity(data['type'], get(sender).team,
                   data['x'], data['y'], data['z'])

        ret = {
            "event": "spawn",
            "type": e.type,
            "uuid": e.uuid,
            "team": e.team,
            "x": e.x,
            "y": e.y,
            "z": e.z
        }
        broadcast(ret, sender)

    def purchase(self, sender, data):
        player = get_player(sender)
        if player.resource >= GENERATOR_PRICE:
            player.resource -= GENERATOR_PRICE
            player.item['generator'] += 1

        ret = {
            "resource": player.resource,
            "item": player.item
        }
        send(ret, sender)

    def update(self, s: dict)->str:
        for k in s.keys():
            getattr(self, s["event"])(k, s[k])

        changed_generator = set()
        changed_player = set()
        changed_building = set()
        server = game_server.GameServer.get_server_ins()

        if timer % GENERATOR_COOLDOWN == 0:
            for e in entities.items():
                if e.type == "generator" and e.team is not None:
                    changed_generator.add(e.uuid)
                    e.resource += 1

        if timer % WILD_GENERATOR_COOLDOWN == 0:
            for e in entities.items():
                if e.type == "generator" and e.team is None:
                    changed_generator.add(e.uuid)
                    e.resource += 1

        for uuid in get_player_list:
            player = get_player(uuid)
            for e in entities.items():
                if e.type == "generator" and (player.x-e.y)**2+(player.y-e.y)**2 < MAX_COLLECT:
                    e.resource -= 1
                    player.resource += 1
                    changed_generator.add(e.uuid)
                    changed_player.add(player.uuid)

                if e.type == "building" and (player.x-e.y)**2+(player.y-e.y)**2 < MAX_FIX_RANGE:
                    e.health += 1
                    player.resource -= 1
                    changed_building.add(e.uuid)
                    changed_player.add(player.uuid)

        for uuid in changed_generator:
            ret = {
                "event": "resource",
                "uuid": uuid,
                "amount": get(uuid).resource
            }
            server.broadcast(json.dumps(ret), None)

        for uuid in changed_player:
            ret = {
                "resource": get_player(uuid).resource,
                "item": get_player(uuid).item()
            }
            server.send(json.dumps(ret), uuid)

        for uuid in changed_building:
            ret = {
                "event": "fix",
                "uuid": uuid,
                "progress": get(uuid).health
            }
            server.broadcast(json.dumps(ret), None)

            if get(uuid).health >= MAX_HEALTH['bulding']:
                ret = {
                    "event": "win_game",
                    "uuid": uuid
                }
                server.broadcast(json.dumps(ret), None)
                return "WaitingRoom"

        return ""
