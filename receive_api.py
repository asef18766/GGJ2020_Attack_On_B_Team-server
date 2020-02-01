from server import *
import entity
import send_api
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
        pass


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
    e = entity.get(data['uuid'])
    e.x = data['location']['x']
    e.y = data['location']['x']
    e.z = data['location']['x']
    e.rotation = data['rotation']
    send_api.move(entity)


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
    get_player(sender).weapon = data['choice']


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
    send_api.attack(entity)


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
    entity.damage(entity.get(data['damager']),
                  entity.get(data['target']), data['amount'])
    send_api.damage(entity)


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
* purchase(sender)
    when player buy something
    ```json
    {
        "event":"purchase",
        "item":"generator"
    }
'''
