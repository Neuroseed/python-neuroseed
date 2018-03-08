import neuroseed
from neuroseed import models
from neuroseed import layers

input = layers.Conv2D(32, [3, 3])
x = layers.MaxPooling2D()(input)
x = layers.Conv2D(32, [3, 3])(x)
x = layers.MaxPooling2D()(x)
x = layers.Flatten()(x)
x = layers.Dense(10)(x)

model = models.Model(input, x)

print('Config:', model.get_config())

model.compile(optimizer="sgd", loss='mean_squared_error')
model.fit("d1")

