import requests
import jsonschema

from . import authorization


def parse_args(args, kwargs, schema):
    kwargs = kwargs.copy()
    fields = list(schema['properties'].keys())
    args = {key: value for key, value in zip(fields, args)}
    kwargs.update(args)
    jsonschema.validate(kwargs, schema)
    return kwargs


def extract_schema(dict, schema):
    fields = list(schema['properties'].keys())
    data = {key: dict[key] for key in fields if key in dict}
    jsonschema.validate(data, schema)
    return data


def get(url, *args, **kwargs):
    url = authorization.HOST + '/' + url

    headers = kwargs.setdefault('headers', {})
    auth_headers = authorization.get_auth_headers()
    headers.update(auth_headers)

    return requests.get(url, *args, **kwargs)


def post(url, *args, **kwargs):
    url = authorization.HOST + '/' + url

    headers = kwargs.setdefault('headers', {})
    auth_headers = authorization.get_auth_headers()
    headers.update(auth_headers)

    return requests.post(url, *args, **kwargs)
