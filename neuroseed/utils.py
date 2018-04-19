import requests
import jsonschema
from jsonschema import validate
import collections.abc

from . import authorization


def parse_args(args, kwargs, schema):
    """Parse args by given json-schema
    
    Args:
        args (list): List of args
        kwargs (dict): Dict of args
        schema (dict): JSON-schema for parsing data
        
    Returns:
        dict. Parsed dict of arguments
        
    Raises:
        TypeError
        jsonschema.ValidationError
    """

    if not isinstance(args, collections.abc.Iterable):
        raise TypeError('interface of args must be collection.abc.Iterable')

    if not isinstance(kwargs, collections.abc.Mapping):
        raise TypeError('interface of kwargs must be collection.abc.Mapping')

    kwargs = kwargs.copy()
    fields = list(schema['properties'].keys())
    args = {key: value for key, value in zip(fields, args)}
    kwargs.update(args)

    # validate data by json schema
    validate(kwargs, schema)

    return kwargs


def extract_schema(data, schema):
    """Extract data by json-schema
    
    Args:
        data (dict): Data to extracting
        schema (dict): Extracted schema
        
    Returns:
        dict
        
    Raises:
        TypeError
        jsonschema.ValidationError
    """

    if not isinstance(data, collections.abc.Mapping):
        raise TypeError('interface of data must be collection.abc.Mapping')

    if not isinstance(schema, collections.abc.Mapping):
        raise TypeError('interface of schema must be collection.abc.Mapping')

    fields = list(schema['properties'].keys())
    data = {key: data[key] for key in fields if key in data}

    # validate data by json schema
    validate(data, schema)

    return data


def delete_task(task_id):
    """Stop and delete task by id
    
    Args:
        task_id (str):
        
    Returns:
        None
        
    Raises:
        TypeError
        RuntimeError
    """

    url = '/api/v1/task/{id}'.format(id=task_id)

    result = delete(url)

    if result.status_code == 200:
        return

    raise RuntimeError('Status code', result.status_code)


def get(url, *args, **kwargs):
    """HTTP GET method with authorization token"""

    url = authorization.HOST + url

    headers = kwargs.setdefault('headers', {})
    auth_headers = authorization.get_auth_headers()
    headers.update(auth_headers)

    return requests.get(url, *args, **kwargs)


def post(url, *args, **kwargs):
    """HTTP POST method with authorization token"""

    url = authorization.HOST + url

    headers = kwargs.setdefault('headers', {})
    auth_headers = authorization.get_auth_headers()
    headers.update(auth_headers)

    return requests.post(url, *args, **kwargs)


def delete(url, *args, **kwargs):
    """HTTP DELETE method with authorization token"""

    url = authorization.HOST + url

    headers = kwargs.setdefault('headers', {})
    auth_headers = authorization.get_auth_headers()
    headers.update(auth_headers)

    return requests.delete(url, *args, **kwargs)
