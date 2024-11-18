#!/usr/bin/env python


import os
import sys
from sqlite3 import connect
from unittest.mock import patch, MagicMock

import pytest

from xcyber360.tests.util import InitWDBSocketMock

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators

        del sys.modules['xcyber360.rbac.orm']

        from xcyber360.tests.util import RBAC_bypasser

        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser
        from xcyber360.syscheck import run, clear, last_scan, files
        from xcyber360.syscheck import AffectedItemsXcyber360Result
        from xcyber360 import Xcyber360Error, Xcyber360InternalError
        from xcyber360.core import common

callable_list = list()
test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
test_agent_data_path = os.path.join(test_data_path, 'agent')


# Retrieve used parameters in mocked method
def set_callable_list(*params, **kwargs):
    callable_list.append((params, kwargs))


# Get a fake database
def get_fake_syscheck_db(sql_file):
    def create_memory_db(*args, **kwargs):
        syscheck_db = connect(':memory:')
        cur = syscheck_db.cursor()
        with open(os.path.join(test_data_path, sql_file)) as f:
            cur.executescript(f.read())
        return syscheck_db

    return create_memory_db


test_result = [
    {'affected_items': ['001', '002'], 'total_affected_items': 2, 'failed_items': {}, 'total_failed_items': 0},
    {'affected_items': ['003', '008'], 'total_affected_items': 2, 'failed_items': {'001'}, 'total_failed_items': 1},
    {'affected_items': ['001'], 'total_affected_items': 1, 'failed_items': {'002', '003'},
     'total_failed_items': 2},
    # This result is used for exceptions
    {'affected_items': [], 'total_affected_items': 0, 'failed_items': {'001'}, 'total_failed_items': 1},
]


@pytest.mark.parametrize('agent_list, failed_items, status_list, expected_result', [
    (['002', '001'], [{'items': []}], ['active', 'active'], test_result[0]),
    (['003', '001', '008'], [{'items': [{'id': '001', 'status': ['disconnected']}]}],
     ['active', 'disconnected', 'active'], test_result[1]),
    (['001', '002', '003'], [{'items': [{'id': '002', 'status': ['disconnected']},
                                        {'id': '003', 'status': ['disconnected']}]}],
     ['active', 'disconnected', 'disconnected'], test_result[2]),
])
@patch('xcyber360.core.common.CLIENT_KEYS', new=os.path.join(test_agent_data_path, 'client.keys'))
@patch('xcyber360.syscheck.Xcyber360DBQueryAgents.__exit__')
@patch('xcyber360.syscheck.Xcyber360DBQueryAgents.__init__', return_value=None)
@patch('xcyber360.syscheck.Xcyber360Queue._connect')
@patch('xcyber360.syscheck.Xcyber360Queue.send_msg_to_agent', side_effect=set_callable_list)
@patch('xcyber360.syscheck.Xcyber360Queue.close')
@pytest.mark.skip('Remove tested function or update it to use the indexer.')
def test_syscheck_run(close_mock, send_mock, connect_mock, agent_init_mock, agent_exit_mock,
                      agent_list, failed_items, status_list, expected_result):
    """Test function `run` from syscheck module.

    Parameters
    ----------
    agent_list : list
        List of agent IDs.
    agent_list : list
        List of failed items.
    status_list : list
        List of agent statuses.
    expected_result : list
        List of dicts with expected results for every test.
    """
    with patch('xcyber360.syscheck.Xcyber360DBQueryAgents.run', return_value=failed_items[0]):
        result = run(agent_list=agent_list)
        for args, kwargs in callable_list:
            assert (isinstance(a, str) for a in args)
            assert (isinstance(k, str) for k in kwargs)
        assert isinstance(result, AffectedItemsXcyber360Result)
        assert result.affected_items == expected_result['affected_items']
        assert result.total_affected_items == expected_result['total_affected_items']
        if result.failed_items:
            assert next(iter(result.failed_items.values())) == expected_result['failed_items']
        else:
            assert result.failed_items == expected_result['failed_items']
        assert result.total_failed_items == expected_result['total_failed_items']


@pytest.mark.parametrize('agent_version', ('v3.11.9',))
@pytest.mark.parametrize('agent_list, expected_result, agent_info_list', [
    (['001', '002'], test_result[0], ['001', '002']),
    (['003', '001', '008'], test_result[1], ['003', '008'])
])
@patch('xcyber360.core.wdb.Xcyber360DBConnection.__init__', return_value=None)
@patch('xcyber360.core.wdb.Xcyber360DBConnection.execute', return_value=None)
@patch('xcyber360.core.wdb.Xcyber360DBConnection.close')
@pytest.mark.skip('Remove tested function or update it to use the indexer.')
def test_syscheck_clear(wdb_close_mock, wdb_execute_mock, wdb_init_mock, agent_list, expected_result, agent_info_list,
                        agent_version):
    """Test function `clear` from syscheck module.

    Parameters
    ----------
    agent_list : list
        List of agent IDs.
    expected_result : list
        List of dicts with expected results for every test.
    agent_info_list : list
        List of agent IDs that `syscheck.get_agents_info` will return when mocked.
    """
    with patch('xcyber360.syscheck.get_agents_info', return_value=set(agent_info_list)), \
            patch('xcyber360.syscheck.Xcyber360DBQueryAgents') as mock_wdbqa:
        mock_wdbqa.return_value.run.return_value = {
            'items': [{'id': ag_id, 'version': agent_version} for ag_id in agent_info_list]}

        result = clear(agent_list=agent_list)
        assert isinstance(result, AffectedItemsXcyber360Result)
        assert result.affected_items == expected_result['affected_items']
        assert result.total_affected_items == expected_result['total_affected_items']
        if result.failed_items:
            assert next(iter(result.failed_items.values())) == expected_result['failed_items']
        else:
            assert result.failed_items == expected_result['failed_items']
        assert result.total_failed_items == expected_result['total_failed_items']
        wdb_close_mock.assert_called()


@pytest.mark.parametrize('agent_version, expected_version_errcode', [
    ('v3.12.0', 1760),
    ('Xcyber360 v4.2.0', 1760),
    (None, 1015)
])
@pytest.mark.parametrize('agent_list, expected_result, agent_info_list', [
    (['001'], test_result[3], ['001']),
])
@patch('xcyber360.core.wdb.Xcyber360DBConnection.__init__', return_value=None)
@patch('xcyber360.core.wdb.Xcyber360DBConnection.execute', side_effect=Xcyber360Error(1000))
@patch('xcyber360.core.wdb.Xcyber360DBConnection.close')
@pytest.mark.skip('Remove tested function or update it to use the indexer.')
def test_syscheck_clear_exception(wdb_close_mock, execute_mock, wdb_init_mock, agent_list, expected_result,
                                  agent_info_list, agent_version, expected_version_errcode):
    """Test function `clear` from syscheck module.

    It will force an exception.

    Parameters
    ----------
    agent_list : list
        List of agent IDs.
    expected_result : list
        List of dicts with expected results for every test.
    agent_info_list : list
        List of agent IDs that `syscheck.get_agents_info` will return when mocked.
    """
    with patch('xcyber360.syscheck.get_agents_info', return_value=set(agent_info_list)), \
            patch('xcyber360.syscheck.Xcyber360DBQueryAgents') as mock_wdbqa:
        mock_wdbqa.return_value.run.return_value = {
            'items': [{'id': ag_id, 'version': agent_version} for ag_id in agent_info_list]}

        result = clear(agent_list=agent_list)

        w_error = next(iter(result.failed_items))
        assert expected_version_errcode == w_error.code
        assert isinstance(result, AffectedItemsXcyber360Result)
        assert result.affected_items == expected_result['affected_items']
        assert result.total_affected_items == expected_result['total_affected_items']
        if result.failed_items:
            assert next(iter(result.failed_items.values())) == expected_result['failed_items']
        assert result.total_failed_items == expected_result['total_failed_items']


@pytest.mark.parametrize('agent_id, xcyber360_version', [
    (['001'], {'version': 'Xcyber360 v3.6.0'}),
    (['002'], {'version': 'Xcyber360 v3.8.3'}),
    (['005'], {'version': 'Xcyber360 v3.5.3'}),
    (['006'], {'version': 'Xcyber360 v3.9.4'}),
    (['004'], {}),
])
@patch('xcyber360.core.utils.path.exists', return_value=True)
@patch('sqlite3.connect', side_effect=get_fake_syscheck_db('schema_syscheck_test.sql'))
@patch("xcyber360.syscheck.Xcyber360DBConnection.execute", return_value=[{'end': '', 'start': ''}])
@patch('socket.socket.connect')
def test_syscheck_last_scan(socket_mock, wdb_conn_mock, db_mock, exists_mock, agent_id, xcyber360_version):
    """Test function `last_scan` from syscheck module.

    Parameters
    ----------
    agent_id : list
        Agent ID.
    xcyber360_version : dict
        Dict with the Xcyber360 version to be applied.
    """
    with patch('xcyber360.syscheck.Agent.get_basic_information', return_value=xcyber360_version):
        result = last_scan(agent_id)
        assert isinstance(result, AffectedItemsXcyber360Result)
        assert isinstance(result.affected_items, list)
        assert result.total_affected_items == 1


@pytest.mark.parametrize('agent_id, select, filters, distinct, q', [
    (['001'], None, None, None, None),
    (['002'], ['file', 'size', 'mtime'], None, False, None),
    (['003'], None, {'inode': '15470536'}, True, None),
    (['004'], ['file', 'size'], {'hash': '15470536'}, False, None),
    (['005'], None, {'date': '2019-05-21 12:10:20'}, True, None),
    (['006'], None, {'type': 'registry_key'}, True, None),
    (['007'], ['file', 'arch', 'value.name', 'value.type'], None, True, None),
    (['008'], ['file', 'value.name'], None, True, None),
    (['009'], ['value.name'], None, True, None)
])
@patch('xcyber360.core.utils.path.exists', return_value=True)
@patch('socket.socket.connect')
@patch('xcyber360.core.common.WDB_PATH', new=test_data_path)
def test_syscheck_files(socket_mock, exists_mock, agent_id, select, filters, distinct, q):
    """Test function `files` from syscheck module.

    Parameters
    ----------
    agent_id : list
        Agent ID.
    select :
        List of parameters to show from the query.
    filters : dict
        Dict to filter out the result.
    distinct : bool
        True if all response items must be unique
    """
    select_list = ['date', 'mtime', 'file', 'size', 'perm', 'uname', 'gname', 'md5', 'sha1', 'sha256', 'inode', 'gid',
                   'uid', 'type', 'changes', 'attributes', 'arch', 'value.name', 'value.type']
    nested_fields = ['value']

    with patch('xcyber360.core.utils.Xcyber360DBConnection') as mock_wdb:
        mock_wdb.return_value = InitWDBSocketMock(sql_schema_file='schema_syscheck_test.sql')
        select = select if select else select_list
        result = files(agent_id, select=select, filters=filters, q=q)
        assert isinstance(result, AffectedItemsXcyber360Result)
        assert isinstance(result.affected_items, list)
        # Use flag for min_select_field, if file not in select, len(item.keys()) = len(select) + 1
        flag_select_min = 1 if 'file' not in select else 0
        for item in result.affected_items:
            # Use flag for nested_fields in order to compare select and item.keys() lengths
            flag_nested = 0
            for nested_field in nested_fields:
                if nested_field in item.keys():
                    flag_nested += sum(1 for i in select if i.startswith(nested_field)) - 1
            assert len(select) + flag_select_min == len(item.keys()) + flag_nested
            assert (param in select for param in item.keys())
        assert not any(result.affected_items.count(item) > 1 for item in result.affected_items) if distinct else True
        if filters:
            for key, value in filters.items():
                assert (item[key] == value for item in result.affected_items)
