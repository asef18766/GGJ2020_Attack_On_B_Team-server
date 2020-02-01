



    





'''


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
