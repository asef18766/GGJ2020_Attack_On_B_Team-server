import socket
import json
import threading
def client_job(client:socket):
    while True:
        data = client.recv(65525)
        if not data:
            pass
        else:
            print("server recv:",data)
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

    while True:
        try:
            (client, _) = sock.accept()
            print("client connected!")
            th = threading.Thread(target=client_job , args=(client , ))
            th.setDaemon(True)
            th.start()
        except socket.timeout:
            print("no new player :P")
        
if __name__ == "__main__":
    ready_dict={}
    enter_dict={}
    start_server()