from .layer import Layer
from .dense import *
from .conv import *


class MaxPooling2D(Layer):
    schema = {
        "type": "object",
        "properties": {
            "pool_size": {
                "type": "array",
                "items": {"type": "number"},
            },
            "strides": {
                "type": "array",
                "items": {"type": "number"},
            },
            "padding": {"type": "string"},
            "data_format": {"type": "string"},
        },
        "additionalProperties": False
    }


class Flatten(Layer):
    pass




