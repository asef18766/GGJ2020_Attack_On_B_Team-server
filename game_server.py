import socket
import uuid
import entity
import send_api
import receive_api
class GameServer():
    server_ins = None
    clients = {}

    BUFSIZE = 65525

    @staticmethod
    def get_server_ins():
        if GameServer.server_ins == None:
            GameServer.server_ins = GameServer()
        return GameServer.server_ins
    
    def add_client(self,client:socket.socket,name:str):
        player=entity.Player(name,"",0,0,0)
        self.clients.update({
            player.uuid:client
        })
    
    def recvall(self)->dict:
        data = {}
        for k in self.clients.keys():
            req = socket.socket(self.clients[k]).recv(65525).decode()
            data.update({k:req})
        return data
    
    def broadcast(self , msg:str , broadcaster: uuid.UUID):
        for k in self.clients.keys():
            if broadcaster != None:
                if k == broadcaster:
                    continue
            socket.socket(self.clients[k]).send(msg.encode())

    def send(self , msg:str , id:uuid.UUID):
        socket.socket(self.clients[id]).send(msg.encode())
    
    @staticmethod
    def process(sender:uuid.UUID , data:dict):
        getattr(receive_api, data['event'])(sender,data)