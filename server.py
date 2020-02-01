import socket
import json
import uuid
import game_server
from state_handler import *

def read_cfg():
    with open("settings.json","r") as fp:
        data = dict(json.loads(fp.read()))
        return data

def game_tick():
    if 

def start_server():
    cfg=dict(read_cfg())
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((cfg["ip_addr"] , int(cfg["port"])))
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
        
        packets=server.recvall()
        for i in packets.keys():
            server.process(data[i])
        game_tick()
    
if __name__ == "__main__":
    ready_dict={}
    enter_dict={}
    start_server()