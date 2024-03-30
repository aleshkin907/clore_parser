from typing import Any, Dict, List
from repositories.cache import AbstractServerCacheRepository

from models.server import Server, get_servers_dict
from repositories.server_repository import ServerRepository


class ServerService:
    repository: ServerRepository
    cache_repository: AbstractServerCacheRepository


    def __init__(self, repository: ServerRepository, cache_repository: AbstractServerCacheRepository):
        self.repository = repository
        self.cache_repository = cache_repository


    def update_or_create_all(self, server_models: List[Server]) -> None:
        cache_servers = self.cache_repository.server_get_all()

        servers_to_update = get_updated_servers(cache_servers, server_models)
        print(len(servers_to_update))

        if servers_to_update:
            self.repository.create_or_update_all(servers_to_update)
            self.cache_repository.server_create_or_update_all(servers_to_update)


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


# def to_compare_dict(server: Server) -> Dict[str, Any]:
#     result = {}
#     fields = ["id", "demand_bitcoin", "demand_clore", "spot_bitcoin", "spot_clore", "mb", "cpu", "cpus",
#               "ram", "disk", "gpu_count", "rented", "mb", "disk_speed", "net_up", "net_down", "gpu_id"]
    
#     for field in fields:
#         result[field] = getattr(server, field)
#     print(result)
#     return result
