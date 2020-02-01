import socket
import json
import uuid
import threading
from state_handler import state_handler
import game_server

def client_job(client:socket , server:socket):
    state_machine = state_handler.get_instance()
    while True:
        data = client.recv(65525)
        if not data:
            pass
        else:
            print("server recv:",data)
            state_machine.recv(data)
            client.send("this is ser~~~~ver~~~OwO".encode())
    client.close()
def read_cfg():
    with open("settings.json","r") as fp:
        data = dict(json.loads(fp.read()))
        return data

def start_server():
    cfg=dict(read_cfg())
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((cfg["ip_addr"] , int(cfg["port"])))
    sock.listen(int(cfg["max_player"]))
    sock.settimeout(int(cfg["timeout"]))
    
    server = game_server.GameServer()
    while True:
        try:
            (client, _) = sock.accept()
            server.add_client(client)
        except socket.timeout:
            print("no new player :P")
        
        packets=server.recvall()
        for i in packets.keys():
            server.process(uuid.UUID(i) , data[i])
    
if __name__ == "__main__":
    start_server()