from typing import List
import redis
from configs.config import settings
from models.gpu import Gpu, gpu_domain_to_redis, gpu_redis_to_domain
from models.server import Server, server_domain_to_redis, server_redis_to_domain
from repositories.cache import AbstractGpuCacheRepository, AbstractServerCacheRepository


class RedisRepository(AbstractGpuCacheRepository, AbstractServerCacheRepository):
    connection: redis.Redis
    gpu_redis_name: str
    server_redis_name: str


    def __init__(self, host, port, db, gpu_redis_name, server_redis_name):
        self.connection = redis.Redis(host=host, port=port, db=db, decode_responses=True, encoding='utf-8')
        self.gpu_redis_name = gpu_redis_name
        self.server_redis_name = server_redis_name


    def gpu_get_all(self) -> List[Gpu]:
        gpu_keys_list = list(self.connection.scan_iter(match=f"{self.gpu_redis_name}:*"))
        pipeline = self.connection.pipeline()
        for key in gpu_keys_list:
            pipeline.hgetall(key)

        gpu_values_list = pipeline.execute()
        gpu_dict = dict(zip(gpu_keys_list, gpu_values_list))    
        gpus = gpu_redis_to_domain(gpu_dict)
        
        return gpus
        

    def gpu_create_or_update_all(self, gpus: List[Gpu]) -> None:
        pipeline = self.connection.pipeline()
        gpu_dict = gpu_domain_to_redis(gpus, "gpu")
        for key, value in gpu_dict.items():
            pipeline.hmset(key, value)
        pipeline.execute()


    def server_create_or_update_all(self, servers: List[Server]) -> None:
        pipeline = self.connection.pipeline()
        server_dict = server_domain_to_redis(servers, "server")
        for key, value in server_dict.items():
            pipeline.hmset(key, value)
        pipeline.execute()
        

    def server_get_all(self) -> List[Server]:
        server_keys_list = list(self.connection.scan_iter(match=f"{self.server_redis_name}:*"))
        pipline = self.connection.pipeline()
        for key in server_keys_list:
            pipline.hgetall(key)

        server_values_list = pipline.execute()
        server_dict = dict(zip(server_keys_list, server_values_list))
        servers = server_redis_to_domain(server_dict)

        return servers
