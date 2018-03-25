import os

import neuroseed


TOKEN = os.environ.get('AUTH_TOKEN', None) or input('Enter auth token: ')
HOST = 'http://localhost:8080'

neuroseed.authorize(TOKEN, HOST)

ds = neuroseed.datasets
print('Datasets:', ds)
