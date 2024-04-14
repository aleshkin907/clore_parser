from typing import List

import requests
from bs4 import BeautifulSoup as s

from schemas.hashrate import *
from logging_loguru.loguru import get_logger
from models.gpu import Gpu
from models.server import Server
from parser.consts import CLORE_SERVERS_URL, COIN_CLASS_NAME, COIN_MARKET_URL, HASHRATE_COINS_URL, HASHRATE_GPUS_URL, BTC, CLORE
from schemas.server import ServerSchema
from services.gpu_service import GpuService
from services.server_service import ServerService


logger = get_logger()


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

    @logger.catch
    def parse(self) -> None:
        response = requests.get(url=CLORE_SERVERS_URL, headers={"auth": self.clore_key})
        if response.status_code != 200:
            logger.warning(f"Clore response status code: {response.status_code}, text: {response.text}")
            return
        servers = response.json().get("servers")

        if not servers:
            logger.warning(f"Clore parser: zero servers from clore parser")
            return
        
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
    
    @logger.catch
    def update_servers_profit(self):
        bitcoin_price = get_coin_price(COIN_MARKET_URL+BTC, COIN_CLASS_NAME)
        if not bitcoin_price:
            return
        
        clore_price = get_coin_price(COIN_MARKET_URL+CLORE, COIN_CLASS_NAME)
        if not clore_price:
            return

        gpus_dict = get_gpus_revenue_from_hashrate(HASHRATE_GPUS_URL)
        gpu_revenue_dict = self.gpu_service.update_prices(gpus_dict)
        self.server_service.update_servers_profit(gpu_revenue_dict, clore_price, bitcoin_price)


def get_coin_price(coin_market_url: str, class_: str) -> float:
    response = requests.get(coin_market_url, timeout=10)
    if response.status_code != 200:
        logger.warning(f"CoinMarket response status code: {response.status_code}, text: {response.text}")
        return
    soup = s(response.text, "html.parser")
    coin = soup.find(class_=class_)
    if not coin:
        logger.warning(f"Coin not found with class_: {class_}")
        return
    result = float(coin.text.replace(",", "")[1:])
    return result


def get_gpus_revenue_from_hashrate(hashrate_url: str):
    result_dict = {}
    response = requests.get(hashrate_url)
    if response.status_code != 200:
        logger.warning(f"Hashrate response status code: {response.status_code}, text: {response.text}")
        return
    soup = s(response.text, 'html.parser')


    html_containers = soup.find("ul", id="myUL")
    gpus_info = html_containers.find_all(class_="w3-col l12 m12 s12")
    
    for element in gpus_info:
        try:
            gpu_name = element.find(class_="deviceHeader2").text
        except AttributeError:
            continue

        gpu_revenue_and_coin = element.find_all(class_="w3-col l3 m6 s6 deviceData")[-1]

        coin = gpu_revenue_and_coin.find('td', style="font-weight: bold;").text
        revenue = float(gpu_revenue_and_coin.find_all('td')[1].text.strip('$'))

        result_dict[gpu_name] = {"coin": coin, "revenueUSD24": revenue}

    return result_dict
