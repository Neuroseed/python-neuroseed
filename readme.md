# python-neuroseed

A Python wrapper around the [Neuroseed MVP](http://mvp.neuroseed.net) REST API. It inherits most of [Keras](https://github.com/keras-team/keras) and [Tensorflow](https://github.com/tensorflow/tensorflow) application programming interface.

**All computations runs remotely on Neuroseed's servers!**

Is compatible with: **Python 3.6**

## Installation

The easiest way is to install from pypi:

```bash
pip3 install neuroseed
```

Alternatively you can clone this repo and install it with:

```bash
python3 setup.py install
```

## Requirements

* requests==2.18.1
* jsonschema==2.6.0
* requests-toolbelt==0.8.0

## Usage

### Authentication

In order to use the API you need an API key that can be obtained [here](https://mvp.neuroseed.net). This is user specific and is used instead of passwords.

```python
import neuroseed

TOKEN = 'paste-your-token-there'
neuroseed.authorize(TOKEN)
```

## Show avalible datasets

`neuroseed.datasets` is registry that contains datasets remote proxies. It has list-like interface, and inherit collections.Iterable interface. Dataset loading is lazy procedure.

```python
datasets = neuroseed.datasets

print('Datasets list:', datasets)
```

## Upload new dataset

You must prepare a dataset in [hdf5](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) format. Name hdf5's datasets: 'x' - input data, 'y' - output data. NeuroSeed validate hdf5 schema and you can not upload dataset with invalid schema.

```python
from neuroseed.dataset import Dataset

DATASET_PATH = '<dir>/<dataset-name>.hdf5'

dataset = Dataset()
dataset.is_public = False
dataset.title = 'dataset-title'
dataset.description = 'dataset-description'
dataset.upload(DATASET_PATH)
```

## Create Model

Model creating look like Keras code but under the hood perform instructions to Neuroseed command schemas. For convenience it imitate Keras interface as close as possible.

```python
input = x = layers.Conv2D(32, [3, 3])
x = layers.MaxPooling2D(pool_size=[2, 2])(x)
x = layers.Conv2D(32, [3, 3])(x)
x = layers.MaxPooling2D(pool_size=[2, 2])(x)
x = layers.Flatten()(x)
x = layers.Dense(10)(x)

model = models.Model(input, x)
model.summary()
```

## Train Model

Models are trained on Neuroseed platform datasets. You can not use `numpy.array` as dataset. Before training a model, you need to configure the learning process, which is done via the `compile` method.

```python
model.compile(optimizer="SGD", loss='mean_squared_error')
model.fit(dataset, epochs=10)
```

You always can break training and delete task by press `CTRL+C` in terminal window or 'stop' button in your IDE.

## Examples

In the [examples folder](/examples) of the repository, you will find more advanced code.

## Documentation

View the latest python-neuroseed documentation at [python-neuroseed.readthedocs.io](https://python-neuroseed.readthedocs.io). You can view Neuroseed MVP REST API documentation at: [mvp.neuroseed.net/docs/api](https://api.neuroseed.net/docs/api).

## Support

Contact us:

* ihor.omelchenko@neuroseed.net  (Ihor Omelchenko)

You can also post bug reports and feature requests (only) in GitLab issues.