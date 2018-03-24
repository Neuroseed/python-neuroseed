import time
import functools

from . import utils

BASE = '/api/v1'
EXPIRE_TIME = 1


class Dataset:
    def __init__(self, id):
        if not type(id) is str:
            raise TypeError('id type must be str')

        self.id = id
        self.metadata = None

        self.load_metadata()

    def __str__(self):
        return f'<neuroseed.datasets.Dataset with id {self.id}>'

    def __repr__(self):
        return f'<neuroseed.datasets.Dataset with id {self.id}>'

    def load_metadata(self):
        url = BASE + f'/dataset/{self.id}'
        result = utils.get(url)

        if result.status_code == 200:
            self.metadata = result.json()
        else:
            raise ValueError(f'Status code {result.status_code}')

    def __getattr__(self, item):
        return self.metadata[item]


class Datasets:
    def __init__(self):
        self._ids = []
        self._datasets = {}
        self._ids_expire = 0

        self._update()

    @property
    def ids(self):
        self._update()

        return self._ids.copy()

    def __len__(self):
        url = BASE + '/datasets/number'
        result = utils.get(url)
        json = result.json()
        return json

    def __str__(self):
        return str([f'<neuroseed.datasets.Dataset with id {id}>' for id in self._ids])

    def __repr__(self):
        return repr([f'<neuroseed.datasets.Dataset with id {id}>' for id in self._ids])

    def __getitem__(self, id):
        self._update()

        if type(id) is int:
            return self.get_from_index(id)
        elif type(id) is str:
            return self.get_from_id(id)

    def get_from_id(self, id):
        if not type(id) is str:
            raise TypeError('id type must be str')

        if id not in self._ids:
            raise KeyError(id)

        if id in self._datasets:
            return self._datasets[id]

        dataset = Dataset(id)
        self._datasets[id] = dataset
        return dataset

    def get_from_index(self, index):
        if not type(index) is int:
            raise TypeError('id type must be str')

        if index > len(self) or index < 0:
            raise KeyError(index)

        id = self._ids[index]

        if id in self._datasets:
            return self._datasets[id]

        dataset = Dataset(id)
        self._datasets[id] = dataset
        return dataset

    def _update(self):
        if self._ids_expire < time.time():
            self._ids_expire = time.time() + EXPIRE_TIME
            self._ids = self._load_ids()

    def _load_ids(self):
        url = BASE + '/datasets'
        result = utils.get(url)
        json = result.json()
        ids = json['ids']
        return ids


@functools.lru_cache(1)
def get_datasets():
    return Datasets()
