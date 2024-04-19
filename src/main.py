import time
import schedule

from db.db import session
from repositories.redis_repository import RedisRepository
from parser.parser import Parser
from repositories.gpu_repository import GpuRepository
from repositories.server_repository import ServerRepository
from services.gpu_service import GpuService
from configs.config import settings
from services.server_service import ServerService
from logging_loguru.loguru import get_logger


logger = get_logger()


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Execution time of {func.__name__}: {end_time - start_time} seconds")
        return result
    return wrapper


if __name__ == "__main__":
    redis = RedisRepository(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, gpu_redis_name="gpu", server_redis_name="server")

    gpu_repository = GpuRepository(session)
    server_repository = ServerRepository(session)

    gpu_service = GpuService(gpu_repository, redis)
    server_service = ServerService(server_repository, redis)
 
    parser = Parser(settings.SECRET_KEY, settings.HASHRATE_API_KEY, gpu_service, server_service)


    @measure_time
    def parse_wrapper():
        parser.parse()


    @measure_time
    def update_servers_profit_wrapper():
        parser.update_servers_profit()


    parse_wrapper()
    update_servers_profit_wrapper()
    
    schedule.every(5).minutes.do(parse_wrapper)
    schedule.every(5).minutes.do(update_servers_profit_wrapper)

    while True:
        schedule.run_pending()
        time.sleep(1)
