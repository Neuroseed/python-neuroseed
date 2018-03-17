import jsonschema
from jsonschema import validate


def parse_args(args, kwargs, schema):
    kwargs = kwargs.copy()
    fields = list(schema['properties'].keys())
    args = {key:value for key, value in zip(fields, args)}
    kwargs.update(args)
    jsonschema.validate(kwargs, schema)
    return kwargs


def extract_schema(dict, schema):
    fields = list(schema['properties'].keys())
    data = {key:dict[key] for key in fields if key in dict}
    jsonschema.validate(data, schema)
    return data
