# import time
import time
from db.db import session
from repositories.redis_repository import RedisRepository
from parser.parser import Parser
from repositories.gpu_repository import GpuRepository
from repositories.server_repository import ServerRepository
from services.gpu_service import GpuService
from configs.config import settings
from services.server_service import ServerService


def time_parser(func):
    def wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        execution_time = end_time - start_time
        print("Время выполнения функции parse: ", execution_time, "секунд")
    return wrapper


if __name__ == "__main__":
    redis = RedisRepository(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, gpu_redis_name="gpu", server_redis_name="server")

    gpu_repository = GpuRepository(session)
    server_repository = ServerRepository(session)

    gpu_service = GpuService(gpu_repository, redis)
    server_service = ServerService(server_repository, redis)
 
    parser = Parser(settings.SECRET_KEY, settings.HASHRATE_API_KEY, gpu_service, server_service)

    @time_parser
    def parse():
        parser.parse()

    parse()


    parser.update_prices()
