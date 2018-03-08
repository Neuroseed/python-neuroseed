from . import layer

__all__ = [
    'Conv2D'
]


class Conv2D(layer.Layer):
    schema = {
        "type": "object",
        "properties": {
            "filters": {"type": "number"},
            "kernel_size": {
                "type": "array",
                "items": {"type": "number"},
            },
            "strides": {"type": "number"},
            "padding": {"type": "string"},
            "dilation_rate": {"type": "number"},
            "activation": {"type": "string"},
            "use_bias": {"type": "boolean"},
            "kernel_initializer": {"type": "string"},
            "bias_initializer": {"type": "string"},
            "kerel_reqularizer": {"type": "string"},
            "bias_regularizer": {"type": "string"},
            "activity_regularizer": {"type": "string"},
            "kernel_constraint": {"type": "string"},
            "bias_constraint": {"type": "string"}
        },
        "required": [
            "filters",
            "kernel_size"
        ],
        "additionalProperties": False
    }

