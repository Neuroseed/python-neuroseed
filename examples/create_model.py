import os

import neuroseed
from neuroseed import models
from neuroseed import layers

TOKEN = os.environ.get('AUTH_TOKEN', None) or input('Enter auth token: ')

neuroseed.authorize(TOKEN)

inp = layers.Conv2D(32, [3, 3])
x = layers.MaxPooling2D()(inp)
x = layers.Conv2D(32, [3, 3])(x)
x = layers.MaxPooling2D()(x)
x = layers.Flatten()(x)
x = layers.Dense(10)(x)

model = models.Model(inp, x)
model.summary()

#print('Config:', model.get_config())

model.compile(optimizer="sgd", loss='mean_squared_error')

DATASET = input('Enter dataset ID: ')
model.fit(DATASET)
