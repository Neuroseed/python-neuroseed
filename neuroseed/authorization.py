
HOST = 'http://api.neuroseed.net'
AUTH_TOKEN = None


class NotAuthorized(Exception):
    pass


def authorize(token: str, host: str=None):
    """Authorize on Neuroseed MVP by authorization token
    
    Args:
        token (str): The authorization token
    
    Kwargs:
        host (str): Neuroseed MVP server host
     
    Returns:
        None
        
    Raises:
        TypeError
    """

    global AUTH_TOKEN, HOST

    if not type(token) is str:
        raise TypeError('Type of token must be str')

    if not type(host) is str:
        raise TypeError('Type of host must be str')

    AUTH_TOKEN = token
    HOST = host or HOST


def is_authorized():
    """Check if authorized on Neuroseed MVP
    
    Returns:
        bool
    """

    return bool(AUTH_TOKEN)


def assert_authorization():
    """Assert authorization on Neuroseed MVP
    
    Returns:
         None
         
    Raises:
        NotAuthorized
    """

    if not is_authorized():
        raise NotAuthorized('Not authorized on Neuroseed platform')


def get_auth_headers():
    """Return JWT authorization header
    
    Returns:
        dict
    
    Raises:
        NotAuthorized
    """

    assert_authorization()

    return {
        'Authorization': 'Bearer {token}'.format(token=AUTH_TOKEN)
    }
