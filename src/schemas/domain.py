from typing import Union

from pydantic import BaseModel, validator


class DomainServerSchema(BaseModel):
    id: int
    demand_bitcoin: Union[float, None]
    demand_clore: Union[float, None]
    spot_bitcoin: Union[float, None]
    spot_clore: Union[float, None]

    @validator('demand_bitcoin', 'demand_clore', 'spot_bitcoin', 'spot_clore', pre=True, always=True)
    def check_empty_string(cls, v):
        if v == '':
            return None
        return v
    
    mb: str
    cpu: str
    cpus: str
    ram: float
    disk: str
    disk_speed: float
    gpu_count: int
    net_up: float
    net_down: float
    rented: bool
    gpu_id: int
