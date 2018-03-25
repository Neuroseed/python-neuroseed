import jsonschema
from requests_toolbelt.multipart import encoder

from . import utils
from .schema.dataset import DATASET_SCHEMA

BASE = '/api/v1'


class Dataset:
    def __init__(self, **kwargs):
        self._id = None
        self._metadata = {}

        if 'file_path' in kwargs:
            self._file_path = kwargs['file_path']
            del kwargs['file_path']
        else:
            self._file_path = None

        if 'id' in kwargs:
            self._id = kwargs['id']
            self.load_metadata()
            return

        for key in kwargs:
            setattr(self, key, kwargs[key])

    @classmethod
    def from_id(cls, id):
        if not type(id) is str:
            raise TypeError('id type must be str')

        ins = cls(id=id)

        return ins

    def __str__(self):
        return f'<neuroseed.datasets.Dataset with id {self.id}>'

    def __repr__(self):
        return f'<neuroseed.datasets.Dataset with id {self.id}>'

    def __eq__(self, other):
        if hasattr(other, 'id'):
            return self.id == other.id

        return False

    def __getattr__(self, key):
        keys = DATASET_SCHEMA['properties'].keys()

        if key in keys:
            return self._metadata.get(key, None)

        return super().__getattribute__(key)

    def __setattr__(self, key, value):
        keys = DATASET_SCHEMA['properties'].keys()

        if key in keys:
            jsonschema.validate(value, DATASET_SCHEMA['properties'][key])
            self._metadata[key] = value
        else:
            super().__setattr__(key, value)

    @property
    def id(self):
        return self._id or self._metadata.get('id', None)

    @property
    def metadata(self):
        return self._metadata.copy()

    def load_metadata(self):
        url = BASE + f'/dataset/{self.id}'
        result = utils.get(url)

        if result.status_code == 200:
            self._metadata = result.json()
        else:
            raise ValueError(f'Status code {result.status_code}')

    def _create_metadata(self):
        url = BASE + '/dataset'
        json = self.metadata

        jsonschema.validate(json, DATASET_SCHEMA)

        result = utils.post(url, json=json)

        if result.status_code == 200:
            self._id = result.json()['id']
        else:
            raise RuntimeError(f'code {result.status_code}, {result.text}')

    def _upload_file(self):
        print(f'Upload file {self._file_path}')

        url = BASE + f'/dataset/{self.id}'

        with open(self._file_path, 'rb') as f:
            form = encoder.MultipartEncoder({
                "file": (self._file_path, f, "text/plain")
            })

            headers = {
                "Prefer": "respond-async",
                "Content-Type": form.content_type,
            }

            resp = utils.post(url, headers=headers, data=form, stream=True)

            if resp.status_code == 200:
                self._is_uploaded = True
            else:
                raise RuntimeError(f'code {resp.status_code}, {resp.text}')

    def upload(self, file_path=None):
        self._file_path = self._file_path or file_path

        self._create_metadata()
        self._upload_file()
