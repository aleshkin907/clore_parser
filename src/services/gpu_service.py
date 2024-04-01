from typing import Dict, List, Set
from models.gpu import Gpu, get_prices_and_ids_from_gpus, gpu_list_to_name_dict, gpu_list_to_name_set, gpu_list_unique
from repositories.cache import AbstractGpuCacheRepository
from repositories.gpu_repository import GpuRepository
from schemas.hashrate import DeviceSchema, RevenueSchema, from_gpu_scemas_to_dict
from parser.consts import gpu_mapping


class GpuService:
    repository: GpuRepository
    cache_repository: AbstractGpuCacheRepository


    def __init__(self, repository: GpuRepository, cache_repository: AbstractGpuCacheRepository):
        self.repository = repository
        self.cache_repository = cache_repository
    

    def get_or_create_all(self, gpu_models: List[Gpu]) -> List[int]:
        cache_gpus = self.cache_repository.gpu_get_all()
        gpus_dict = gpu_list_to_name_dict(cache_gpus)
        # сет по имнам из того что в редисе потом из того что в моделс
        gpu_cache_names = gpu_list_to_name_set(cache_gpus)
        gpu_models_names = gpu_list_to_name_set(gpu_models)
        
        new_gpu_names: Set[str] = gpu_models_names - gpu_cache_names

        result: List[int] = [None]*len(gpu_models)

        if new_gpu_names:
            new_gpus: List[Gpu] = gpu_list_unique(gpu_models)
            repository_gpus = self.repository.get_or_create_all(new_gpus) # старые подтягивает
            gpus_dict = gpu_list_to_name_dict(repository_gpus)
            self.cache_repository.gpu_create_or_update_all(repository_gpus)
        
        for i in range(len(gpu_models)):
            result[i] = gpus_dict.get(gpu_models[i].name)

        return result
    

    def update_prices(self, gpus_schemas: Dict[DeviceSchema, RevenueSchema]) -> Dict[int, float]:
        gpus_dict = from_gpu_scemas_to_dict(gpus_schemas)
        gpus = self.repository.get_all()

        reverced_gpu_mapping = {value: key for key, value in gpu_mapping.items()}
        for gpu in gpus:
            hashrate_gpu_name = reverced_gpu_mapping.get(gpu.name)
            price_data = gpus_dict.get(hashrate_gpu_name)
            if price_data:
                gpu.coin = price_data.get("coin")
                gpu.revenue = price_data.get("revenueUSD24")

        updated_gpus = self.repository.get_or_create_all(gpus)

        gpu_revenue_dict = get_prices_and_ids_from_gpus(updated_gpus)

        return gpu_revenue_dict

        
