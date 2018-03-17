from .layer import Layer


class Dense(Layer):
    schema = {
        "type": "object",
        "properties": {
            "units": {"type": "number"},
            "activation": {"type": "string"},
            "use_bias": {"type": "boolean"},
            "kernel_initializer": {"type": "string"},
            "bias_initializer": {"type": "string"},
            "kernel_regularizer": {"type": "string"},
            "bias_regularizer": {"type": "string"},
            "activity_regularizer": {"type": "string"},
            "kernel_constraint": {"type": "string"},
            "bias_constraint": {"type": "string"}
        },
        "required": [
            "units",
        ],
        "additionalProperties": False
    }


