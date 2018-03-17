
AUTH_TOKEN = None

class NotAuthorized(Exception):
    pass


def authorize(token):
    global AUTH_TOKEN

    if not type(token) is str:
        raise TypeError('Type of token must be str')

    AUTH_TOKEN = token


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
