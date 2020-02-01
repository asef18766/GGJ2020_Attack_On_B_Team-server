import uuid
entities = []
MAX_HEALTH = {
    "building": 1000,
    "generator": 100,
    "player": 100,
    "wild_generator": 1,
    "arrow": 1,
    "wall": 1,
}
INIT_BUILDING_HEALTH = 100


class Entity():
    def __init__(self, type: str, x: float, y: float, z: float):
        self.type = type
        self.x = x
        self.y = y
        self.z = z
        self.uuid = uuid.uuid4()
        while self.uuid in (e.uuid for e in entities):
            self.uuid = uuid.uuid4()

        self.health = MAX_HEALTH[self.type]
        if self.type == "building":
            self.health = INIT_BUILDING_HEALTH

        entities.append(self)


class Player(Entity):
    def __init__(self, name: str, x: float, y: float, z: float):
        super(Player, self).__init__("player", x, y, z)
        self.name = name
        self.resource = 0
