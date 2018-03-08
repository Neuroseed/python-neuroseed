import requests

HOST = 'http://localhost:8080'
BASE = HOST + '/api/v1'


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

    def summary(self):
        pass

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

        resp = requests.post(url, json=json)

        if resp.status_code == 200:
            self.arch_id = resp.json()['id']
            return self.arch_id

        raise ValueError('Status code: {}'.format(resp.status_code))

    def _create_model(self, arch_id):
        url = BASE + '/model'

        json = {
            "is_public": False,
            "meta":{
                "title": "model {}".format(id(self)),
                "architecture": arch_id,
            }
        }
        resp = requests.post(url, json=json)

        if resp.status_code == 200:
            self._model_id = resp.json()['model']['_id']
            return self._model_id

        raise ValueError('Status code: {}'.format(resp.status_code))

    def _train_model(self):
        url = BASE + '/model/{id}/train'.format(id=self._model_id)
        json = {
            'dataset': self._dataset_id,
            'optimizer': self._optimizer,
            'loss': self._loss,
            'metrics': self._metrics
        }

        resp = requests.post(url, json=json)
        if resp.status_code == 200:
            self._task_id = resp.json()['task']
            return self._task_id

        raise ValueError('Status code: {}'.format(resp.status_code))

    def compile(self, optimizer, loss, metrics=None):
        self._optimizer = optimizer
        self._loss = loss,
        self._metrics = metrics

        arch_id = self._create_architecture()
        self._create_model(arch_id)

        self._is_compiled = True

    def fit(self, dataset_id, batch_size=None, epochs=1, verbose=1, callbacks=None, sync=False):
        if not self._is_compiled:
            raise RuntimeError('Model is not compiled')

        self._dataset_id = dataset_id
        self._train_model()

    def evaluate(self, dataset_id, verbose=0):
        pass

    def predict(self, dataset_id, verbose=0):
        pass

