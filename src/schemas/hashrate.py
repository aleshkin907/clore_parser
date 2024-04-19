from typing import Any, Dict, Union

from pydantic import BaseModel, validator


class DeviceSchema(BaseModel):
    name: str


class RevenueSchema(BaseModel):
    coin: str
    revenueUSD24: float

    @validator('revenueUSD24')
    def result_check(cls, v):
        return round(v, 2)


class DeviceRevenueSchema(BaseModel):
    device: DeviceSchema
    revenue24: RevenueSchema


def from_dict_to_revenue_schemas(data: Dict[str, Any]) -> Dict[DeviceSchema, RevenueSchema]:
    # result = {k: DeviceRevenueSchema(
    #     device=DeviceSchema(**v["device"]), 
    #     revenue24=RevenueSchema(**v["revenue24"]))
    #     for k, v in data.items()
    # }
    # return result
    result = {}
    for device_name, device_data in data.items():
        device_schema = DeviceSchema(name=device_name)
        revenue_schema = RevenueSchema(**device_data)
        result[device_schema] = revenue_schema
    return result


def from_gpu_scemas_to_dict(revenue_schemas: Dict[DeviceSchema, RevenueSchema]) -> Dict[str, Dict[str, Union[int, float]]]:
    result = {v.device.name: v.revenue24.dict() for v in revenue_schemas.values()}
    return result
