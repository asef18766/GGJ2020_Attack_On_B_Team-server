import uuid
entities = []
MAX_HEALTH = {
    "building": 1000,
    "generator": 100,
    "player": 100,
    "arrow": 1,
    "wall": 1,
}
INIT_BUILDING_HEALTH = 100


class Entity():
    def __init__(self, type: str, team: str, x: float, y: float, z: float):
        self.type = type
        self.team = team
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
    def __init__(self, name: str, team: str, x: float, y: float, z: float):
        super(Player, self).__init__("player", team, x, y, z)
        self.name = name
        self.resource = 0
        self.weapon = 0


class Generator(Entity):
    def __init__(self, type: str, team: str, x: float, y: float, z: float):
        super(Generator, self).__init__(type, team, x, y, z)
        self.resource = 0


def kill(entity: Entity):
    pass


def on_damage(damager: Entity, victim: Entity):
    pass
