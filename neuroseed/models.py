import shutil
from json.decoder import JSONDecodeError

from .dataset import Dataset
from .datasets_registry import datasets
from . import layers
from . import utils

BASE = '/api/v1'


class Model:
    """Model remote proxy to MVP Model resource with Keras-like interface
    
    Args:
        input (layers.Layer): Model input layer
        output (layers.Layer): Model output layer
        
    Raises:
        TypeError
    """

    def __init__(self, input, output):
        if not isinstance(input, layers.Layer):
            raise TypeError('type of input must be layers.Layer')

        if not isinstance(output, layers.Layer):
            raise TypeError('type of output must be layers.Layer')

        self._is_compiled = False
        self.input = input
        self.output = output

    def get_config(self):
        """Return model config
        
        Returns:
            tuple
        """

        def get_layers(layer):
            if layer:
                return get_layers(layer.inbound_node) + (layer,)
            return (layer,)

        layers = get_layers(self.output)
        layers = filter(None, layers)

        config = map(lambda layer: layer.get_config(), layers)
        return tuple(config)

    def summary(self, line_length=None):
        """Print model summary"""

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

    def _create_model(self, arch_id, dataset_id):
        url = BASE + '/model'

        json = {
            "is_public": False,
            "title": "model {}".format(id(self)),
            "architecture": arch_id,
            "dataset": dataset_id
        }

        resp = utils.post(url, json=json)

        if resp.status_code == 200:
            self._model_id = resp.json()['id']
            return self._model_id

        raise ValueError('Status code: {}, {}'.format(resp.status_code, resp.text))

    def _train_model(self, epochs=1):
        url = BASE + '/model/{id}/train'.format(id=self._model_id)
        json = {
            'epochs': epochs,
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

        raise ValueError('Status code: {}, {}'.format(resp.status_code, resp.text))

    def _wait_train(self, task_id):
        import time

        old_epoch = -1

        while True:
            url = BASE + '/model/train/{task_id}/history'.format(task_id=task_id)
            result = utils.get(url)

            if result.status_code == 200:
                history = result.json()

                examples = history.get('examples', None)
                current_example = history.get('current_example', None)

                epochs = history.get('epochs', None)
                current_epoch = history.get('current_epoch', None)

                if examples and epochs:
                    percent = current_example / examples
                    length = 60
                    llen = int(length * percent)
                    rlen = int(length * (1 - percent))
                    progress = '[' + '=' * llen + '>' + ' ' * (rlen - 1) + ']'

                    eta = 999
                    metrics = 'no batch metrics'

                    if current_epoch != old_epoch:
                        old_epoch = current_epoch
                        epoch_metrics = ''
                        if current_epoch > 0:
                            epoch_metrics = '-' + ' - '.join(['{key}: {value}'.format(key=key, value=value[-1]) for key, value in history['epoch'].items()])

                        print('Epoch {current}/{epochs} {metrics}'.format(
                            current=current_epoch,
                            epochs=epochs,
                            metrics=epoch_metrics))

                    print('{current}/{examples} {progress} - ETA: {eta}s - {metrics}'.format(
                        current=current_example,
                        examples=examples,
                        progress=progress,
                        eta=eta,
                        metrics=metrics))
            elif result.status_code == 201:
                print('Model is trained')
                return
            else:
                print(result.status_code, result.text)

            time.sleep(1)

    def compile(self, optimizer, loss, metrics=()):
        """Compile model. For keras-like interface"""

        self._optimizer = optimizer
        self._loss = loss
        self._metrics = metrics

        self.arch_id = self._create_architecture()

        self._is_compiled = True

    def fit(self, dataset, batch_size=None, epochs=1, verbose=1, callbacks=None, sync=False):
        """Train model on dataset
        
        Args:
            dataset (dataset.Dataset): Dataset proxy
            
        Kwargs:
            batch_size (int): Batch size
            epochs (int): Number of training epochs
            verbose (int): Logging verbose level
            callbacks (list): Training callbacks
            sync (bool): Wait for end training
            
        Raises:
            RuntimeError
            TypeError
        """

        if not self._is_compiled:
            raise RuntimeError('Model is not compiled')

        if type(dataset) is str:
            dataset = datasets[dataset]

        if not isinstance(dataset, Dataset):
            raise TypeError('dataset type must be Dataset')

        self._dataset = dataset
        self._create_model(self.arch_id, dataset.id)
        task_id = self._train_model(epochs)

        try:
            self._wait_train(task_id)
        except KeyboardInterrupt:
            utils.delete_task(task_id)
            print('Task is stopped')
            raise

    def evaluate(self, dataset, verbose=0):
        pass

    def predict(self, dataset, verbose=0):
        pass

