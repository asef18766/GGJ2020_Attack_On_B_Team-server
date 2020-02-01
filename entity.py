import uuid
entities = {}
MAX_HEALTH = {
    "building": 10000,
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
        self.rotation=0
        self.uuid = uuid.uuid4()
        while self.uuid in entities
            self.uuid = uuid.uuid4()

        self.health = MAX_HEALTH[self.type]
        if self.type == "building":
            self.health = INIT_BUILDING_HEALTH

        entities[self.uuid]=self


class Player(Entity):
    def __init__(self, name: str, team: str, x: float, y: float, z: float):
        super(Player, self).__init__("player", team, x, y, z)
        self.name = name
        self.resource = 0
        self.weapon = 0
        self.alive = True


class Generator(Entity):
    def __init__(self, type: str, team: str, x: float, y: float, z: float):
        super(Generator, self).__init__(type, team, x, y, z)
        self.resource = 0



def get_player_list():
    return list(k in entities if entities[k].type=="player")

def get(uuid):
    return entities[uuid]

def get_player(uuid) -> Player:
    return entities[uuid]

def get_generator(uuid) -> Generator:
    return entities[uuid]

def kill(entity: Entity):
    if entity.type = "player":
        entity.alive = False
    else: 
        del entities[entity.uuid]


def damage(damager: Entity, victim: Entity, amount: int) -> bool:
    if victim.type == "wall" or victim.type == "arrow":
        amount = 0
    if victim.type == "generator" and victim.team is None:
        amount = 0
    if damager.team == victim.team:
        amount = 0

    victim.health -= amount
    if victim.health <= 0:
        kill(victim)

    if damager.type == "arrow":
        kill(damager)

    return amount > 0
