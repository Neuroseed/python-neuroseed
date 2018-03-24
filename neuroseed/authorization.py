
HOST = 'http://api.neuroseed.net'
AUTH_TOKEN = None


class NotAuthorized(Exception):
    pass


def authorize(token, host=None):
    global AUTH_TOKEN, HOST

    if not type(token) is str:
        raise TypeError('Type of token must be str')

    if not type(host) is str:
        raise TypeError('Type of host must be str')

    AUTH_TOKEN = token
    HOST = host or HOST


def is_authorized():
    return bool(AUTH_TOKEN)


def assert_authorization():
    if not is_authorized():
        raise NotAuthorized('Not authorized on Neuroseed platform')


def get_auth_headers():
    assert_authorization()

    return {
        'Authorization': 'Bearer {token}'.format(token=AUTH_TOKEN)
    }
