import os

import neuroseed
from neuroseed import datasets


TOKEN = os.environ.get('AUTH_TOKEN', None) or input('Enter auth token: ')
HOST = 'http://localhost:8080'

neuroseed.authorize(TOKEN, HOST)

ds = datasets.get_datasets()
print('Datasets:', ds)
