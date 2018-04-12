from .layer import Layer


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
        "required": ["pool_size"],
        "additionalProperties": False
    }
