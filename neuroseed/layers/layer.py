from .. import utils


class Layer:
    """Layer Keras-like interface
    
    Args:
        *: Args for layer json-schema
        
    Kwargs:
        *: Kwargs for layer json-schema
        
    Raises:
        jsonschema.ValidationError
    """

    schema = {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }

    def __init__(self, *args, **kwargs):
        self._inbound_node = None

        data = utils.parse_args(args, kwargs, self.schema)
        utils.validate(data, self.schema)
        self.__dict__.update(data)

    def __call__(self, node):
        self._inbound_node = node
        return self

    @property
    def inbound_node(self):
        return self._inbound_node

    def get_config(self):
        """Return layer config

        Returns:
            dict
        """

        name = self.__class__.__name__
        config = utils.extract_schema(self.__dict__, self.schema)

        return {
            'name': name,
            'config': config
        }
