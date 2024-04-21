from typing import List

from sqlalchemy.orm import Session

from models.gpu import Gpu
from models.server import Server
from logging_loguru.loguru import get_logger


logger = get_logger()


class ServerRepository:
    db: Session

    def __init__(self, db: Session):
        self.db = db
    
    def create_or_update_all(self, servers: List[Server]) -> None:
        for server in servers:
            self.db.merge(server)
        self.db.commit()

    def get_all(self) -> List[Server]:
        servers = self.db.query(Server).all()
        return servers
    
    def get_servers_to_update_profit(self) -> List[Server]:
        servers_with_gpu = self.db.query(Server).join(Server.gpu).filter(Gpu.revenue != 0).all()
        return servers_with_gpu
    