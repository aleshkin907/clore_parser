from typing import List, Set
from models.gpu import Gpu, gpu_list_to_name_dict, gpu_list_to_name_set, gpu_list_unique
from repositories.cache import AbstractGpuCacheRepository
from repositories.gpu_repository import GpuRepository


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
