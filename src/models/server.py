from typing import Any, Dict, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.domain import DomainServerSchema


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(nullable=True)
    demand_bitcoin: Mapped[float] = mapped_column(nullable=True)
    demand_clore: Mapped[float] = mapped_column(nullable=True)
    spot_bitcoin: Mapped[float] = mapped_column(nullable=True)
    spot_clore: Mapped[float] = mapped_column(nullable=True)
    mb: Mapped[str]
    cpu: Mapped[str]
    cpus: Mapped[str]
    ram: Mapped[float]
    disk: Mapped[str]
    disk_speed: Mapped[float]
    gpu_id: Mapped[int] = mapped_column(ForeignKey("gpus.id"), nullable=True)
    gpu_count: Mapped[int]
    net_up: Mapped[float]
    net_down: Mapped[float]
    rented: Mapped[bool]
    profit: Mapped[float] = mapped_column(nullable=True)


    def __str__(self):
         return f'{self.id} {self.price} {self.demand_bitcoin} {self.demand_clore} {self.spot_bitcoin} {self.spot_clore}\
         {self.mb} {self.cpu} {self.cpus} {self.ram} {self.disk} {self.disk_speed} {self.gpu_id} {self.gpu_count}\
         {self.net_up} {self.net_down} {self.rented} {self.profit}'
    

    # def __eq__(self, other):
    #     return all((
    #         self.id == other.id,
    #         self.price == other.price,
    #         self.demand_bitcoin == other.demand_bitcoin,
    #         self.demand_clore == other.demand_clore,
    #         self.spot_bitcoin == other.spot_bitcoin,
    #         self.spot_clore == other.spot_clore,
    #         self.mb == other.mb,
    #         self.cpu == other.cpu,
    #         self.cpus == other.cpus,
    #         self.ram == other.ram,
    #         self.disk == other.disk,
    #         self.disk_speed == other.disk_speed,
    #         self.gpu_id == other.gpu_id,
    #         self.gpu_count == other.gpu_count,
    #         self.net_up == other.net_up,
    #         self.net_down == other.net_down,
    #         self.rented == other.rented,
    #         self.profit == other.profit
    #     ))
    

    def __ne__(self, other):
        return self.id != other.id or \
            self.price != other.price or \
            self.demand_bitcoin != other.demand_bitcoin or \
            self.demand_clore != other.demand_clore or \
            self.spot_bitcoin != other.spot_bitcoin or \
            self.spot_clore != other.spot_clore or \
            self.mb != other.mb or \
            self.cpu != other.cpu or \
            self.cpus != other.cpus or \
            self.ram != other.ram or \
            self.disk != other.disk or \
            self.disk_speed != other.disk_speed or \
            self.gpu_id != other.gpu_id or \
            self.gpu_count != other.gpu_count or \
            self.net_up != other.net_up or \
            self.net_down != other.net_down or \
            self.rented != other.rented or \
            self.profit != other.profit


def get_servers_dict(servers: List[Server]) -> Dict[int, Server]:
    result = {}

    for server in servers:
        result[int(server.id)] = server
    
    return result


def server_redis_to_domain(server_dict: Dict[str, Dict[str, Any]]) -> List[Server]:
    servers: List[Server] = list()
    for key, value in server_dict.items():
            value["id"] = key.split(":")[1]
            value["rented"] = value["rented"] == '1'
            server_schema = DomainServerSchema(**value)

            server = Server(**server_schema.model_dump())
            servers.append(server)

    return servers


def server_domain_to_redis(server_list: List[Server], redis_server_name: str) -> Dict[str, Dict[str, Any]]:
    server_dict = {}
    for server in server_list:
        temp_server_dict = server.__dict__
        del temp_server_dict["_sa_instance_state"]
        cache_key_id = temp_server_dict.pop("id")
        for key, value in temp_server_dict.items():
            temp_server_dict[key] = value if value is not None else ''
        temp_server_dict["rented"] = int(temp_server_dict["rented"])
        server_dict[f'{redis_server_name}:{cache_key_id}'] = temp_server_dict
    return server_dict