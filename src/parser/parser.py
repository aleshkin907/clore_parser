from typing import List
from pydantic import BaseModel
import requests
from models.gpu import Gpu
from models.server import Server
from parser.consts import CLORE_SERVERS_URL
from schemas.server import ServerSchema
from services.gpu_service import GpuService
from services.server_service import ServerService


class Parser:
    gpu_service: GpuService
    server_service: ServerService


    # def __init__(self, key: str, gpu_service: GpuService, server_service: ServerService) -> None:
    #     self.gpu_service = gpu_service
    #     self.server_service = server_service
    #     self.key = key
    key: str

    def __init__(self, key: str, gpu_service: GpuService, server_service: ServerService) -> None:
        self.key = key
        self.gpu_service = gpu_service
        self.server_service = server_service

    def parse(self) -> None:
        response = requests.get(url=CLORE_SERVERS_URL, headers={"auth": self.key})
        if response.status_code != 200:
            print("gg bet status code not 200")
            return
        servers = response.json().get("servers")

        if not servers:
            print("gg bet no servers")
            return
        
        # преобразование в схемы серверов
        len_servers = len(servers)

        servers_schema: List[ServerSchema] = [None]*len_servers
        for i in range(len_servers):
            servers_schema[i] = ServerSchema(**servers[i])
        
        gpu_models: List[Gpu] = [None]*len_servers
        server_models: List[Server] = [None]*len_servers

        for i in range(len_servers):
            gpu_models[i] = servers_schema[i].to_gpu_model()
            server_models[i] = servers_schema[i].to_server_model()
        

        gpu_ids = self.gpu_service.get_or_create_all(gpu_models)

        for i in range(len_servers):
            server_models[i].gpu_id = int(gpu_ids[i])
            
        self.server_service.update_or_create_all(server_models)
