from elasticsearch_dsl import (Document, Date, Text, Integer, Float, Keyword, Index, Search)

from base_model.base_model import BaseModel


class Camera(BaseModel):
    type = Keyword()
    resolution = Keyword()
    ip = Keyword()

    class Index:
        name = 'eltrox-camera'
        settings = {'number_of_shard': 1,
                    }


class IpCamera(Camera):
    network_interface = Keyword()
    network_protocols = Keyword()

    class Index:
        name = 'eltrox-camera-ip'
        settings = {'number_of_shard': 1,
                    }