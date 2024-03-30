from typing import Dict, List
from pydantic import BaseModel

from models.gpu import Gpu
from models.server import Server


class PriceSchema(BaseModel):
    on_demand: Dict[str, float]
    spot: Dict[str, float]


class NetSchema(BaseModel):
    up: float
    down: float
    cc: str


class SpecsSchema(BaseModel):
    mb: str
    cpu: str
    cpus: str
    ram: float
    disk: str
    disk_speed: float
    gpu: str
    gpuram: int
    net: NetSchema
    backend_version: int
    pcie_rev: int
    pcie_width: int

    def get_gpu_name(self) -> str:
        return self.gpu.split(" ", 1)[-1]
    
    def get_gpu_count(self) -> int:
        return int(self.gpu.split(" ", 1)[0][:-1])


class RatingSchema(BaseModel):
    avg: float
    cnt: int


class ServerSchema(BaseModel):
    id: int
    owner: int
    price: PriceSchema
    specs: SpecsSchema
    rented: bool
    allowed_coins: List[str]
    rating: RatingSchema

    def to_gpu_model(self) -> Gpu:
        gpu = Gpu(name=self.specs.get_gpu_name(), gpu_ram=self.specs.gpuram)
        return gpu

    def to_server_model(self) -> Server:
        server = Server(
            id=self.id,
            demand_bitcoin=self.price.on_demand.get("bitcoin"),
            demand_clore=self.price.on_demand.get("CLORE-Blockchain"),
            spot_bitcoin=self.price.spot.get("bitcoin"),
            spot_clore=self.price.spot.get("CLORE-Blockchain"),
            mb=self.specs.mb,
            cpu=self.specs.cpu,
            cpus=self.specs.cpus,
            ram=self.specs.ram,
            disk=self.specs.disk,
            disk_speed=self.specs.disk_speed,
            gpu_count=self.specs.get_gpu_count(),
            net_up=self.specs.net.up,
            net_down=self.specs.net.down,
            rented=self.rented
        )
        return server
