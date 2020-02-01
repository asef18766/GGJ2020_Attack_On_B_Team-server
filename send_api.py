

'''

* waiting(sender)
    update players
    ```json
    {
        "event":"waiting",
        "players":
        [
            {
                "uuid":"xxoo",
                "playerName":"ooxx",
                "ready":true/false
            }
        ],
        "time":1234
    }
    ```
* enter_game(sender)
    tell players to enter
    ```json
    {
        "event":"enterGame"
    }
    ```
'''


def enter_game():
    ret={
        "event": "enterGame"
    }
    broadcast(ret, None)


'''
    
* start_game(sender)
    tell players the game has started
    ```json
    {
        "event":"startGame",
        "team":"ooxx"
    }
    ```
    
* move
    ```json
    {
        "event":"move",
        "uuid":"xxoo",
        "position":
    }
    ```
'''



'''
* change_weapon
    ```json
    
    ```
* attack
    ```json
    {
        "event":"attack",
        "weapon":1,
    }
    ```
* damage
    when player's attack hit someone
    target:uuid of target 
    ```json
    {
        "event":"damage",
        "weapon":1,
        "uuid":"xxoo",
        "amount":87,
        "healthLeft":87
    }
    ```
* kill(sender)
    announce that a entity was dead
    ```json
    {
        "event":"kill",
        "uuid":"ooxx"
    }
    ```
* spawn
    announce to spawn an object
    ```json
    {
        "event":"spawn",
        "type":"player/arrow/generator/building/wall",
        "uuid":"ooxx",
        "team",
        "location":{
            "x":123,
            "y":456,
            "z":789
        }
    }
    ```
* resource(sender)
    when a generator change it's resource amount
    ```json
    {
        "event":"resource",
        "uuid":"ooxx",
        "amount":87
    }
    ```

* stats(sender)
    when a player's stats change
    ```json
    {
        "resource":87,
        "item":
        {
            "generator":87
        }
    }
    ```

* fix(sender)
    when a player fix his building
    ```json
    {
        "event":"fix",
        "uuid":"ooxx",
        "progress":87
    }
    ```

* win_game(sender)
    when a player win the game
    ```json
    {
        "event":"win_game",
        "uuid":"ooxx"
    }
'''
