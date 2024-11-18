

import json
from unittest.mock import patch

import pytest

with patch('xcyber360.common.xcyber360_uid'):
    with patch('xcyber360.common.xcyber360_gid'):
        from api.encoder import prettify, dumps
        from xcyber360.core.results import Xcyber360Result
        from xcyber360.core.indexer.agent import Agent


def custom_hook(dct):
    if 'id' in dct:
        return Agent(**dct)

    if 'key' in dct:
        return {'key': dct['key']}

    if 'error' in dct:
        return Xcyber360Result.decode_json({'result': dct, 'str_priority': 'v2'})

    return dct


@pytest.mark.parametrize('o', [
    {'key': 'v1'},
    Xcyber360Result({'k1': 'v1'}, str_priority='v2'),
    Agent(id='0191e730-f9eb-7794-b2d1-949405d7d6ce', name='test')
])
def test_encoder_dumps(o):
    """Test dumps method from API encoder using Xcyber360APIJSONEncoder."""
    encoded = dumps(o)
    decoded = json.loads(encoded, object_hook=custom_hook)
    assert decoded == o


def test_encoder_prettify():
    """Test prettify method from API encoder using Xcyber360APIJSONEncoder."""
    assert prettify({'k1': 'v1'}) == '{\n   "k1": "v1"\n}'
