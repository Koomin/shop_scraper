from elasticsearch_dsl import Boolean, Integer, Keyword

from base_model.base_model import BaseModel


class Recorder(BaseModel):
    number_of_supported_cameras = Integer()
    number_of_supported_drivers = Integer()
    max_res = Keyword()

    class Index:
        name = 'eltrox-recorder'
        settings = {'number_of_shard': 1,
                    }


class IpRecorder(Recorder):
    network_protocol = Keyword()
    if_onvif = Boolean()

    class Index:
        name = 'eltrox-recorder-ip'
        settings = {'number_of_shard': 1,
                    }


class AnalogRecorder(Recorder):
    class Index:
        name = 'eltrox-recorder-analog'
        settings = {'number_of_shard': 1,
                    }


class HDCVIRecorder(Recorder):
    class Index:
        name = 'eltrox-recorder-hdcvi'
        settings = {'number_of_shard': 1,
                    }
