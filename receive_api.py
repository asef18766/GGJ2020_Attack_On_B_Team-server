from server import *
from state_handler import *
import entity
from entity import *
import send_api
import json
import game_server


def broadcast(msg: dict, broadcaster: uuid.UUID):
    game_server.GameServer.get_server_ins().broadcast(json.dumps(msg), broadcaster)


def send(msg: dict, id: uuid.UUID)):
    game_server.GameServer.get_server_ins().send(json.dumps(msg), id)
'''
* connect(sender)
    create connection
    ```json
    {
        "event":"connect"
        "playerName":"xxoo"
    }
    ```
'''


def connect(sender, data):
    if success:
        ret={
            "event": "connect",
            "playerName": player.name
            "success": True
            "uuid": player.uuid
        }
        send(ret,player.uuid)
    else:
        ret={
            "event": "connect",
            "playerName": ""
            "success": False
            "uuid": None
        }
        send(ret,player.uuid)

'''
* ready(sender)
    announce player is ready
    ```json
    {
        "event":"ready"
    }
    ```
'''


def ready(sender, data):
    ready_dict[sender] = True
    if all(ready_dict.items):
        send_api.ready()


'''
* entered_game
    announce player entered game scence
    ```json
    {
        "event":"entered_game"
    }
    ```
'''


def entered_game(sender, data):
    enter_dict['sender'] = True
    if all(enter_dict.items):
        pass


'''
* move
    move a specify entity
    location: the location of entity
    rotation: the facing orientation of player
    ```json
    {
        "event":"move",
        "uuid":"ooxx",
        "location":{
            "x":123,
            "y":456,
            "z":789
        },
        "rotation":87
    }
    ```
'''


def move(sender, data):
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


'''
* change_weapon
    player change his weapon
    ```json
    {
        "event":"change_weapon",
        "choice":87
    }
    ```
'''


def change_weapon(sender, data):
    player=get_player(sender)
    player.weapon = data['choice']
    ret={
        "event":"change_weapon",
        "uuid":player.uuid,
        "choice":player.weapon
    }
    broadcast(ret,None)


'''
* attack
    player use his weapon
    ```json
    {
        "event":"attack",
        "weapon":1,
    }
    ```
'''


def attack(sender, data):
    ret={
        "event":"attack",
        "weapon":get_player(sender).weapon,
    }
    broadcast(ret,None)


'''
* damage
    when player's attack hit someone
    target:uuid of target 
    ```json
    {
        "event":"damage",
        "weapon":1,
        "damager":"xxoo",
        "target":"xxoo",
        "amount":87
    }
    ```
'''


def damage(sender, data):
    entity.damage(get(data['damager']),
                  get(data['target']), data['amount'])

    ret={
        "event":"damage",
        "uuid":data['target'],
        "amount":data['amount'],
        "healthLeft":get(data['target']).health
    }
    broadcast(ret,None)
'''
* spawn
    when player spawn an object
    ```json
    {
        "event":"spawn",
        "type":"player/arrow/generator/building",
        "location":{
            "x":123,
            "y":456,
            "z":789
        }
    }
    ```
'''


def spawn(sender, data):
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
'''
* purchase(sender)
    when player buy something
    ```json
    {
        "event":"purchase",
        "item":"generator"
    }
'''
def purchase(sender, data):
    player=get_player(sender)
    if player.resource>=GENERATOR_PRICE:
        player.resource-=GENERATOR_PRICE
        player.item['generator']+=1
    
    ret={
        "resource":player.resource,
        "item":player.item
    }
    send(ret,sender)
