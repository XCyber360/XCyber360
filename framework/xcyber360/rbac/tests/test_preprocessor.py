

import json
import os
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine

from framework.xcyber360.rbac.tests.utils import init_db

test_path = os.path.dirname(os.path.realpath(__file__))
test_data_path = os.path.join(test_path, 'data/')


@pytest.fixture(scope='function')
def db_setup():
    with patch('xcyber360.core.common.xcyber360_uid'), patch('xcyber360.core.common.xcyber360_gid'):
        with patch('sqlalchemy.create_engine', return_value=create_engine("sqlite://")):
            with patch('shutil.chown'), patch('os.chmod'):
                with patch('api.constants.SECURITY_PATH', new=test_data_path):
                    from xcyber360.rbac.preprocessor import PreProcessor
    init_db('schema_security_test.sql', test_data_path)

    yield PreProcessor


permissions = list()
results = list()
actual_test = 0
with open(test_data_path + 'RBAC_preprocessor_policies.json') as f:
    file = json.load(f)

inputs = [test_case['no_processed_policies'] for test_case in file]
outputs = [test_case['processed_policies'] for test_case in file]


@pytest.mark.parametrize('input_, output', zip(inputs, outputs))
def test_expose_resources(db_setup, input_, output):
    preprocessor = db_setup()
    for policy in input_:
        preprocessor.process_policy(policy)
    preprocessed_policies = preprocessor.get_optimize_dict()
    assert preprocessed_policies == output
