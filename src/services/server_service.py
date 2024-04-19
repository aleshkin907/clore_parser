from typing import Dict, List

from logging_loguru.loguru import get_logger
from repositories.cache import AbstractServerCacheRepository
from models.server import Server, get_servers_dict
from repositories.server_repository import ServerRepository


logger = get_logger()


class ServerService:
    repository: ServerRepository
    cache_repository: AbstractServerCacheRepository

    def __init__(self, repository: ServerRepository, cache_repository: AbstractServerCacheRepository):
        self.repository = repository
        self.cache_repository = cache_repository

    def update_or_create_all(self, server_models: List[Server]) -> None:
        cache_servers = self.cache_repository.server_get_all()

        servers_to_update = get_updated_servers(cache_servers, server_models)
        logger.info(f"Servers count to update: {len(servers_to_update)}.")

        if servers_to_update:
            self.repository.create_or_update_all(servers_to_update)
            self.cache_repository.server_create_or_update_all(servers_to_update)

    def update_servers_profit(self, gpu_revenue_dict: Dict[int, float], price_clore: float, price_bitcoin: float)-> None:
        servers = self.repository.get_all()

        for server in servers:
            prices = set()
            if server.demand_bitcoin:
                prices.add(server.demand_bitcoin * price_bitcoin)
            
            if server.demand_clore:
                prices.add(server.demand_clore * price_clore)

            lowest_price_rent = min(list(prices))

            gpu_price = gpu_revenue_dict.get(server.gpu_id)
            if gpu_price:
                server_revenue = gpu_price * server.gpu_count
                server.profit = server_revenue - lowest_price_rent
                server.price = lowest_price_rent
        
        self.repository.create_or_update_all(servers)


def get_updated_servers(
    cache_servers: List[Server],
    servers: List[Server]
) -> List[Server]:
    result = []

    cache_servers_dict = get_servers_dict(cache_servers)

    for server in servers:
        if server.id not in cache_servers_dict or server != cache_servers_dict.get(server.id):
            result.append(server)

    return result
