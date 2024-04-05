from typing import Any, Dict, List, Set
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base


class Gpu(Base):
    __tablename__ = "gpus"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    gpu_ram: Mapped[int]
    revenue: Mapped[float] = mapped_column(nullable=True)
    coin: Mapped[str] = mapped_column(nullable=True)

    servers = relationship("Server", back_populates="gpu")
    

def gpu_list_to_name_dict(gpus: List[Gpu]) -> Dict[str, int]:
    gpu_names = {}
    for gpu in gpus:
        gpu_names[gpu.name] = gpu.id
    return gpu_names


def gpu_list_to_name_set(gpus: List[Gpu]) -> Set[str]:
    gpu_set: Set[str] = set()

    for gpu in gpus:
        gpu_set.add(gpu.name)
    
    return gpu_set


def gpu_list_unique(gpus: List[Gpu]) -> List[Gpu]:
    # gpu_set: Set[str] = gpu_list_to_name_set(gpus)
    # res_list: List[Gpu] = [None]*len(gpu_set)
    # for i in range(len(gpu_set)):
    #     if gpus[i].name in gpu_set:
    #         res_list[i] = gpus[i]
    #         gpu_set.remove(gpus[i].name)
    # print(res_list)
    # return res_list

    gpu_set: Set[str] = gpu_list_to_name_set(gpus)
    res_list: List[Gpu] = []
    for gpu in gpus:
        if gpu.name in gpu_set:
            res_list.append(gpu)
            gpu_set.remove(gpu.name)
    return res_list
    

def gpu_redis_to_domain(gpu_dict: Dict[str, Dict[str, Any]]) -> List[Gpu]:
    gpus: List[Gpu] = list()
    for key, value in gpu_dict.items():
            value["id"] = key.split(":")[1]
            gpu = Gpu(**value)
            gpus.append(gpu)
    return gpus


def gpu_domain_to_redis(gpu_list: List[Gpu], redis_gpu_name: str) -> Dict[str, Dict[str, Any]]:
    gpu_dict = {}
    for gpu in gpu_list:
        temp_gpu_dict = gpu.__dict__
        del temp_gpu_dict["_sa_instance_state"]
        cache_key_id = temp_gpu_dict.pop("id")
        for key, value in temp_gpu_dict.items():
            temp_gpu_dict[key] = value if value is not None else ''
        gpu_dict[f'{redis_gpu_name}:{cache_key_id}'] = temp_gpu_dict
    return gpu_dict


def get_prices_and_ids_from_gpus(gpus: List[Gpu]) -> Dict[int, float]:
    result = {}
    for gpu in gpus:
        result[gpu.id] = gpu.revenue
    return result