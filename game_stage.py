from base_state import BaseState
from entity import *
from game_server import GameServer


def broadcast(msg: dict, broadcaster: uuid.UUID):
    game_server.GameServer.get_server_ins().broadcast(json.dumps(msg), broadcaster)


def send(msg: dict, id: uuid.UUID):
    game_server.GameServer.get_server_ins().send(json.dumps(msg), id)

class GameStage(BaseState):

    def move(self, sender, data):
        entity=get(data['uuid'])
        entity.x=data['x']
        entity.y=data['y']
        entity.z=data['z']
        entity.rotation=data['rotation']

        ret={
            "event": "move",
            "uuid": entity.uuid,
            "x": entity.x,
            "y": entity.y,
            "z": entity.z,
            "rotation": entity.rotation
        }
        broadcast(ret, entity.uuid)


    def change_weapon(self, sender, data):
        player=get_player(sender)
        player.weapon = data['choice']
        ret={
            "event":"change_weapon",
            "uuid":player.uuid,
            "choice":player.weapon
        }
        broadcast(ret,None)


    def attack(self, sender, data):
        ret={
            "event":"attack",
            "weapon":get_player(sender).weapon,
        }
        broadcast(ret,None)


    def damage(self, sender, data):
        entity.damage(get(data['damager']),
                    get(data['target']), data['amount'])

        ret={
            "event":"damage",
            "uuid":data['target'],
            "amount":data['amount'],
            "healthLeft":get(data['target']).health
        }
        broadcast(ret,None)


    def spawn(sef, sender, data):
        e=Entity(data['type'],get(sender).team,data['x'],data['y'],data['z'])

        ret={
            "event":"spawn",
            "type":e.type,
            "uuid":e.uuid,
            "team":e.team,
            "x":e.x,
            "y":e.y,
            "z":e.z
        }
        broadcast(ret,sender)

    def purchase(self, sender, data):
        player=get_player(sender)
        if player.resource>=GENERATOR_PRICE:
            player.resource-=GENERATOR_PRICE
            player.item['generator']+=1
        
        ret={
            "resource":player.resource,
            "item":player.item
        }
        send(ret,sender)

    def update(self, s:dict)->str:
        for k in s.keys():
            getattr(self, s["event"])(k,s[k])
