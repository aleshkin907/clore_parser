
from typing import List

from sqlalchemy.orm import Session

from models.gpu import Gpu, gpu_list_to_name_dict


class GpuRepository:
    db: Session


    def __init__(self, db: Session):
        self.db = db

    
    def get_or_create_all(self, gpus: List[Gpu]) -> List[Gpu]:
        result = []
        gpus_repo = self.db.query(Gpu).all()
        gpus_repo_dict = gpu_list_to_name_dict(gpus_repo)

        for gpu in gpus:
            gpu.id = gpus_repo_dict.get(gpu.name)
            gpu = self.db.merge(gpu)
            result.append(gpu)
        self.db.commit()

        return result
    

    def get_all(self) -> List[Gpu]:
        gpus = self.db.query(Gpu).all()
        return gpus
        