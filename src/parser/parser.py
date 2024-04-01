from typing import List
from pydantic import BaseModel
import requests
from models.gpu import Gpu
from models.server import Server
from parser.consts import CLORE_SERVERS_URL, HASHRATE_COINS_URL, HASHRATE_GPUS_URL, BTC, CLORE
from schemas.server import ServerSchema
from services.gpu_service import GpuService
from services.server_service import ServerService
from schemas.hashrate import *


class Parser:
    gpu_service: GpuService
    server_service: ServerService
    clore_key: str
    hashrate_key: str


    def __init__(self, clore_key: str, hashrate_key: str, gpu_service: GpuService, server_service: ServerService) -> None:
        self.clore_key = clore_key
        self.gpu_service = gpu_service
        self.server_service = server_service
        self.hashrate_key = hashrate_key


    def parse(self) -> None:
        response = requests.get(url=CLORE_SERVERS_URL, headers={"auth": self.clore_key})
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
    

    def update_prices(self):
        response = requests.get(HASHRATE_GPUS_URL, params={"apiKey": self.hashrate_key})
        if response.status_code != 200:
            print("gg bet hashrate status code not 200")
            return
        gpus_hashrate = response.json()
        gpus_schemas = from_dict_to_revenue_schemas(gpus_hashrate)
        
        response_btc = requests.get(HASHRATE_COINS_URL, params={"apiKey": self.hashrate_key, "coin": BTC})
        if response_btc.status_code != 200:
            print("gg bet response_btc status code not 200")
            return

        response_clore = requests.get(HASHRATE_COINS_URL, params={"apiKey": self.hashrate_key, "coin": CLORE})
        if response_clore.status_code != 200:
            print("gg bet response_clore status code not 200")
            return
        
        price_bitcoin = round(float(response_btc.json().get("usdPrice")), 2)
        price_clore = round(float(response_clore.json().get("usdPrice")), 2)

        gpu_revenue_dict = self.gpu_service.update_prices(gpus_schemas)
        
        self.server_service.update_servers_profit(gpu_revenue_dict, price_clore, price_bitcoin)
