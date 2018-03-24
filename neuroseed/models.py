import shutil
from json.decoder import JSONDecodeError

from . import datasets
from . import utils

BASE = '/api/v1'


class Model:
    def __init__(self, input, output):
        self._is_compiled = False
        self.input = input
        self.output = output

    def get_config(self):
        def get_layers(layer):
            if layer:
                return get_layers(layer.inbound_node) + (layer,)
            return (layer,)

        layers = get_layers(self.output)
        layers = filter(None, layers)

        config = map(lambda layer: layer.get_config(), layers)
        return tuple(config)

    def summary(self, line_length=None):
        line_length = line_length or shutil.get_terminal_size().columns
        fields = ['Layer (type)', 'Output Shape', 'Param', 'Connected']
        columns_number = len(fields)

        def print_row(fields):
            line = ''
            for i, field in enumerate(fields):
                line += field
                line += ' ' * (line_length // columns_number * (i+1) - len(line))
            print(line)

        print_row(fields)
        print('=' * line_length)

        for layer in self.get_config():
            print_row([layer['name'], '-', '-', '-'])
            print('_' * line_length)

    def _create_architecture(self):
        url = BASE + '/architecture'

        architecture = {
            'layers': self.get_config()
        }
        json = {
            "id": str(id(self)),
            "is_public": False,
            "title": "arch {}".format(id(self)),
            "architecture": architecture
        }

        resp = utils.post(url, json=json)

        if resp.status_code == 200:
            self.arch_id = resp.json()['id']
            return self.arch_id

        try:
            error = resp.json().get('error', '')
        except JSONDecodeError:
            error = resp.text

        raise ValueError('Status code: {}, {}'.format(resp.status_code, error))

    def _create_model(self, arch_id):
        url = BASE + '/model'

        json = {
            "is_public": False,
            "title": "model {}".format(id(self)),
            "architecture": arch_id,
        }

        resp = utils.post(url, json=json)

        if resp.status_code == 200:
            self._model_id = resp.json()['id']
            return self._model_id

        try:
            error = resp.json().get('error', '')
        except JSONDecodeError:
            error = resp.text

        raise ValueError('Status code: {}, {}'.format(resp.status_code, error))

    def _train_model(self):
        url = BASE + '/model/{id}/train'.format(id=self._model_id)
        json = {
            'dataset': self._dataset.id,
            'optimizer': {
                'name': self._optimizer,
                'config': {}
            },
            'loss': self._loss,
            'metrics': list(self._metrics)
        }

        resp = utils.post(url, json=json)
        if resp.status_code == 200:
            self._task_id = resp.json()['id']
            return self._task_id

        try:
            error = resp.json().get('error', '')
        except JSONDecodeError:
            error = resp.text

        raise ValueError('Status code: {}, {}'.format(resp.status_code, error))

    def compile(self, optimizer, loss, metrics=()):
        self._optimizer = optimizer
        self._loss = loss
        self._metrics = metrics

        arch_id = self._create_architecture()
        self._create_model(arch_id)

        self._is_compiled = True

    def fit(self, dataset, batch_size=None, epochs=1, verbose=1, callbacks=None, sync=False):
        if not self._is_compiled:
            raise RuntimeError('Model is not compiled')

        if type(dataset) is str:
            dataset = datasets.get_datasets()[dataset]

        if not isinstance(datasets, datasets.Dataset):
            raise TypeError('dataset type must be Dataset')

        self._dataset = dataset
        self._train_model()

    def evaluate(self, dataset, verbose=0):
        pass

    def predict(self, dataset, verbose=0):
        pass

