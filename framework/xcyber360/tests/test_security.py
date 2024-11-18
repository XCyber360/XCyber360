#!/usr/bin/env python



import glob
import os
from importlib import reload
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy import orm as sqlalchemy_orm
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from yaml import safe_load

from xcyber360.core.exception import Xcyber360Error

test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'security/')

# Params

security_cases = list()
rbac_cases = list()
default_orm_engine = create_engine("sqlite:///:memory:")
os.chdir(test_data_path)

for file in glob.glob('*.yml'):
    with open(os.path.join(test_data_path, file)) as f:
        tests_cases = safe_load(f)

    for function_, test_cases in tests_cases.items():
        for test_case in test_cases:
            if file != 'rbac_catalog.yml':
                security_cases.append((function_, test_case['params'], test_case['result']))
            else:
                rbac_cases.append((function_, test_case['params'], test_case['result']))

with open(os.path.join(test_data_path, 'sanitize_policies.yaml')) as f:
    sanitize_policies = safe_load(f)


def create_memory_db(sql_file, session):
    with open(os.path.join(test_data_path, sql_file)) as f:
        for line in f.readlines():
            line = line.strip()
            if '* ' not in line and '/*' not in line and '*/' not in line and line != '':
                session.execute(text(line))
                session.commit()


def reload_default_rbac_resources():
    with patch('xcyber360.core.common.xcyber360_uid'), patch('xcyber360.core.common.xcyber360_gid'):
        with patch('sqlalchemy.create_engine', return_value=default_orm_engine):
            with patch('shutil.chown'), patch('os.chmod'):
                import xcyber360.rbac.orm as orm
                reload(orm)
                orm.db_manager.connect(orm.DB_FILE)
                orm.db_manager.create_database(orm.DB_FILE)
                orm.db_manager.insert_default_resources(orm.DB_FILE)
                import xcyber360.rbac.decorators as decorators
                from xcyber360.tests.util import RBAC_bypasser

                decorators.expose_resources = RBAC_bypasser
                from xcyber360 import security
    return security, orm


@pytest.fixture(scope='function')
def db_setup():
    with (
        patch('xcyber360.core.common.xcyber360_uid'),
        patch('xcyber360.core.common.xcyber360_gid'),
        patch('xcyber360.core.utils.load_xcyber360_xml')
    ):
        with patch('sqlalchemy.create_engine', return_value=create_engine("sqlite://")):
            with patch('shutil.chown'), patch('os.chmod'):
                with patch('api.constants.SECURITY_PATH', new=test_data_path):
                    import xcyber360.rbac.orm as orm
                    # Clear mappers
                    sqlalchemy_orm.clear_mappers()
                    # Invalidate in-memory database
                    orm.db_manager.close_sessions()
                    orm.db_manager.connect(orm.DB_FILE)
                    orm.db_manager.sessions[orm.DB_FILE].close()
                    orm.db_manager.engines[orm.DB_FILE].dispose()

                    reload(orm)
                    orm.db_manager.connect(orm.DB_FILE)
                    orm.db_manager.create_database(orm.DB_FILE)
                    orm.db_manager.insert_default_resources(orm.DB_FILE)
                    import xcyber360.rbac.decorators as decorators
                    from xcyber360.tests.util import RBAC_bypasser

                    decorators.expose_resources = RBAC_bypasser
                    from xcyber360 import security
                    from xcyber360.core.results import Xcyber360Result
                    from xcyber360.core import security as core_security
    try:
        create_memory_db('schema_security_test.sql', orm.db_manager.sessions[orm.DB_FILE])
    except OperationalError:
        pass

    yield security, Xcyber360Result, core_security
    orm.db_manager.close_sessions()


@pytest.fixture(scope='function')
def new_default_resources():
    global default_orm_engine
    default_orm_engine = create_engine("sqlite:///:memory:")

    security, orm = reload_default_rbac_resources()

    with open(os.path.join(test_data_path, 'default', 'default_cases.yml')) as f:
        new_resources = safe_load(f)

    for function_, cases in new_resources.items():
        for case in cases:
            getattr(security, function_)(**case['params']).to_dict()

    return security, orm


def affected_are_equal(target_dict, expected_dict):
    return target_dict['affected_items'] == expected_dict['affected_items']


def failed_are_equal(target_dict, expected_dict):
    if len(target_dict['failed_items'].keys()) == 0 and len(expected_dict['failed_items'].keys()) == 0:
        return True
    result = False
    for target_key, target_value in target_dict['failed_items'].items():
        for expected_key, expected_value in expected_dict['failed_items'].items():
            result = expected_key in str(target_key) and set(target_value) == set(expected_value)
            if result:
                break

    return result


@pytest.mark.parametrize('security_function, params, expected_result', security_cases)
async def test_security(db_setup, security_function, params, expected_result):
    """Verify the entire security module.

    Parameters
    ----------
    db_setup : callable
        This function creates the rbac.db file.
    security_function : list of str
        This is the name of the tested function.
    params : list of str
        Arguments for the tested function.
    expected_result : list of dict
        This is a list that contains the expected results .
    """
    try:
        security, _, _ = db_setup
        result = await getattr(security, security_function)(**params)
        result_dict = result.to_dict()
        assert affected_are_equal(result_dict, expected_result)
        assert failed_are_equal(result_dict, expected_result)
    except Xcyber360Error as e:
        assert str(e.code) == list(expected_result['failed_items'].keys())[0]


@pytest.mark.parametrize('security_function, params, expected_result', rbac_cases)
def test_rbac_catalog(db_setup, security_function, params, expected_result):
    """Verify RBAC catalog functions.

    Parameters
    ----------
    db_setup : callable
        This function creates the rbac.db file.
    security_function : list of str
        This is the name of the tested function.
    params : list of str
        Arguments for the tested function.
    expected_result : list of dict
        This is a list that contains the expected results .
    """
    security, _, _ = db_setup
    final_params = dict()
    for param, value in params.items():
        if value.lower() != 'none':
            final_params[param] = value
    result = getattr(security, security_function)(**final_params).to_dict()
    assert result['result']['data'] == expected_result


@pytest.mark.parametrize('policy_case', sanitize_policies['policies'])
def test_sanitize_rbac_policy(db_setup, policy_case):
    _, _, core_security = db_setup
    policy = policy_case['policy']
    core_security.sanitize_rbac_policy(policy)
    for element in ('actions', 'resources', 'effect'):
        if element in policy:
            if element != 'resources':
                assert all(p.islower() for p in policy[element])
            else:
                assert all(':'.join(p.split(':')[:-1]) for p in policy[element])
