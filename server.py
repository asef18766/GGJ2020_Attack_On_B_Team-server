import socket
import json
import uuid
import game_server
from entity import *
from state_handler import *

GENERATOR_COOLDOWN = 10
WILD_GENERATOR_COOLDOWN = 20


def read_cfg():
    with open("settings.json", "r") as fp:
        data = dict(json.loads(fp.read()))
        return data


def game_tick():
    timer += 1

    for task in tasks:
        if task[time] <= timer:
            tasks.remove(task)
            task["function"](*task['args'])

    changed=set()

    if timer % GENERATOR_COOLDOWN == 0:
        for e in entities.items():
            if e.type == "generator" and e.team is not None:
                changed.add(e.uuid)
                e.resource += 1

    if timer % WILD_GENERATOR_COOLDOWN == 0:
        for e in entities.items():
            if e.type == "generator" and e.team is None:
                changed.add(e.uuid)
                e.resource += 1


def do_later(func, args, sec):
    task.append({"function": func, "time"=timer+sec*20})


def start_server():
    cfg = dict(read_cfg())
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((cfg["ip_addr"], int(cfg["port"])))
    sock.listen(int(cfg["max_player"]))
    sock.settimeout(float(cfg["timeout"]))
    server = game_server.GameServer.get_server_ins()
    while True:
        try:
            (client, _) = sock.accept()
            client.setblocking(False)
            server.add_client(client)
        except socket.timeout:
            print("no new player :P")

        packets = server.recvall()
        for i in packets.keys():
            server.process(data[i])
        game_tick()


if __name__ == "__main__":
    ready_dict = {}
    enter_dict = {}
    start_server()
    timer = 0
    tasks = []
