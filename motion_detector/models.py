from elasticsearch_dsl import Keyword

from base_model.base_model import BaseModel


class MotionDetector(BaseModel):
    detector_range = Keyword()
    detection_type = Keyword()
    installation_place = Keyword()
    optic_type = Keyword()
    max_current_consumption = Keyword()

    class Index:
        name = 'eltrox-motiondetector'
        settings = {'number_of_shard': 1,
                    }


class SingleMotionDetector(MotionDetector):
    class Index:
        name = 'eltrox-motiondetector-single'
        settings = {'number_of_shard': 1,
                    }


class DualMotionDetector(MotionDetector):
    class Index:
        name = 'eltrox-motiondetector-dual'
        settings = {'number_of_shard': 1,
                    }
