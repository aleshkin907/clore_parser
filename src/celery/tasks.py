import sys
print(sys.path)
from .celery import celery
import json
import re
import requests
import redis
from configs.config import settings
from db.db import session
from models.gpu import Gpu
from models.price import Price
from models.server import Server


MARKETPLACE_URL = "https://api.clore.ai/v1/marketplace"

headers = {
    "auth": "Ydf_WxAujU7AIZQK1.gvdDo8Qg6EQP7h"
}

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

@celery.task
def parse_clore():
    # response = requests.get(url=MARKETPLACE_URL, headers=headers)
    # servers = response.json()["servers"]
    # for server in servers:
    #     update_or_add_server(server)
    pass


def update_or_add_server(server_data):
    server_id = str(server_data["id"])
    existing_data = redis_client.get(server_id)
    if existing_data:
        existing_data = json.loads(existing_data)
        if existing_data != server_data:
            redis_client.set(server_id, json.dumps(server_data))
            print(f"Server with ID {server_id} updated in Redis.")
            save_servers_and_gpus(server_data)
        else:
            print(f"Server with ID {server_id} already exists and is identical.")
    else:
        redis_client.set(server_id, json.dumps(server_data))
        print(f"Server with ID {server_id} added to Redis.")
        save_servers_and_gpus(server_data)


def save_servers_and_gpus(server_data):
    quantity_and_name = extract_quantity_and_name(server_data["specs"]["gpu"])
    existing_gpu = session.query(Gpu).filter_by(name=quantity_and_name[1]).first()
    if existing_gpu == None:
        new_gpu = Gpu(name=quantity_and_name[1], gpu_ram=server_data["specs"]["gpuram"])
        session.add(new_gpu)
        session.commit()
        existing_gpu = session.query(Gpu).filter_by(name=quantity_and_name[1]).first()
    new_server = Server(id=server_data["id"], 
                        price=server_data["price"]["on_demand"]["bitcoin"],
                        mb=server_data["specs"]["mb"], 
                        cpu=server_data["specs"]["cpu"],
                        cpus=server_data["specs"]["cpus"],
                        ram=server_data["specs"]["ram"],
                        disk=server_data["specs"]["mb"],
                        disk_speed=server_data["specs"]["disk_speed"],
                        gpu_id=existing_gpu.id,
                        gpu_count=quantity_and_name[0],
                        net_up=server_data["specs"]["net"]["up"],
                        net_down=server_data["specs"]["net"]["down"],
                        rented=server_data["rented"]
    )
    session.merge(new_server)
    session.commit()
    new_price_history = Price(gpu_id=existing_gpu.id, 
                              price=server_data["price"]["on_demand"]["bitcoin"]/quantity_and_name[0]
    )
    session.add(new_price_history)
    session.commit()

    
        


def extract_quantity_and_name(input_string):
    pattern = r'(\d+)x\s+(.+)'
    match = re.match(pattern, input_string)
    if match:
        quantity = int(match.group(1))
        name = match.group(2)
        return (quantity, name)
    else:
        return None


# parse_clore()
