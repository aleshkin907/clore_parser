# import time
import time
from db.db import session
from repositories.redis_repository import RedisRepository
from parser.parser import Parser, get_coin_price
from repositories.gpu_repository import GpuRepository
from repositories.server_repository import ServerRepository
from services.gpu_service import GpuService
from configs.config import settings
from services.server_service import ServerService
from logging_loguru.loguru import get_logger


logger =get_logger()


if __name__ == "__main__":
    redis = RedisRepository(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, gpu_redis_name="gpu", server_redis_name="server")

    gpu_repository = GpuRepository(session)
    server_repository = ServerRepository(session)

    gpu_service = GpuService(gpu_repository, redis)
    server_service = ServerService(server_repository, redis)
 
    parser = Parser(settings.SECRET_KEY, settings.HASHRATE_API_KEY, gpu_service, server_service)

    @logger.catch
    def parse():
        parser.parse()

    parse()
    parser.update_servers_profit()

    # parser.update_prices()
