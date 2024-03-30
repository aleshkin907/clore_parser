from typing import List

from sqlalchemy.orm import Session

from models.server import Server


class ServerRepository:
    de: Session


    def __init__(self, db: Session):
        self.db = db

    
    def create_or_update_all(self, servers: List[Server]) -> None:
        for server in servers:
            self.db.merge(server)
        self.db.commit()