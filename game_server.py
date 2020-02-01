import socket
import uuid
import entity
class GameServer():
    server_ins = None
    clients = {}
    BUFSIZE = 65525

    @staticmethod
    def get_server_ins():
        if GameServer.server_ins == None:
            GameServer.server_ins = GameServer()
        return GameServer.server_ins
    
    def add_client(self,client:socket.socket):
        player=entity.Player("","",0,0,0)
        print(f"add client with uuid:{player.uuid.hex()}")
        self.clients.update({
            player.uuid:client
        })
    
    def recvall(self)->dict:
        data = {}
        for k in self.clients.keys():
            l = socket.socket(self.clients[k]).recv(4)
            if l == "":
                continue
            print("========== packet ===========")
            print(f"receiver uuid:{k.hex()}")
            print(f"l:{l}")
            l = int.from_bytes(l,byteorder="litte")
            req = socket.socket(self.clients[k]).recv(l)
            print(f"req:{req}")
            print("=============================")
            data.update({k:req})
        return data
    
    def broadcast(self , msg:str , broadcaster: uuid.UUID):
        for k in self.clients.keys():
            if broadcaster != None:
                if k == broadcaster:
                    continue
            self.send(msg , k)

    def send(self , msg:str , id:uuid.UUID):
        b_msg = msg.encode()
        len_msg = len(b_msg).to_bytes(length=4,byteorder="little")
        socket.socket(self.clients[id]).send(len_msg+b_msg)
    
    def process(self,events:dict):
        self.state_processor.recv(events)
