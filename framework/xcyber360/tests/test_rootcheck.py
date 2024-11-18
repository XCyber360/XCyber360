#!/usr/bin/env python


import os
import sys
from unittest.mock import patch, MagicMock, call

import pytest

from api.util import parse_api_param
from xcyber360.core.exception import Xcyber360Error

with patch('xcyber360.common.xcyber360_uid'):
    with patch('xcyber360.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators

        del sys.modules['xcyber360.rbac.orm']

        from xcyber360.tests.util import RBAC_bypasser

        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser
        from xcyber360 import rootcheck
        from xcyber360.core.rootcheck import Xcyber360DBQueryRootcheck
        from xcyber360.core.tests.test_rootcheck import InitRootcheck, send_msg_to_wdb, remove_db, \
            test_data_path as core_data

test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
test_agent_path = os.path.join(test_data_path, 'agent')
test_data = InitRootcheck()
callable_list = list()


# Retrieve used parameters in mocked method
def set_callable_list(*params, **kwargs):
    callable_list.append((params, kwargs))


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
@patch('xcyber360.core.common.CLIENT_KEYS', new=os.path.join(test_agent_path, 'client.keys'))
@patch('xcyber360.rootcheck.Xcyber360DBQueryAgents.__exit__')
@patch('xcyber360.rootcheck.Xcyber360DBQueryAgents.__init__', return_value=None)
@patch('xcyber360.syscheck.Xcyber360Queue._connect')
@patch('xcyber360.syscheck.Xcyber360Queue.send_msg_to_agent', side_effect=set_callable_list)
@patch('xcyber360.syscheck.Xcyber360Queue.close')
@pytest.mark.skip('Remove tested function or update it to use the indexer.')
def test_rootcheck_run(close_mock, send_mock, connect_mock, agent_init__mock, agent_exit__mock,
                       agent_list, failed_items, status_list, expected_result):
    """Test function `run` from rootcheck module.

    Parameters
    ----------
    agent_list : list
        List of agent IDs.
    failed_items : list
        List with the Xcyber360DBQueryAgents response.
    status_list : list
        List of agent statuses.
    expected_result : list
        List of dicts with expected results for every test.
    """
    with patch('xcyber360.rootcheck.Xcyber360DBQueryAgents.run', return_value=failed_items[0]):
        result = rootcheck.run(agent_list=agent_list)
        for args, kwargs in callable_list:
            assert (isinstance(a, str) for a in args)
            assert (isinstance(k, str) for k in kwargs)
        assert isinstance(result, rootcheck.AffectedItemsXcyber360Result)
        assert result.affected_items == expected_result['affected_items']
        assert result.total_affected_items == expected_result['total_affected_items']
        if result.failed_items:
            assert next(iter(result.failed_items.values())) == expected_result['failed_items']
        else:
            assert result.failed_items == expected_result['failed_items']
        assert result.total_failed_items == expected_result['total_failed_items']


@pytest.mark.parametrize('agent_list, expected_affected_items, expected_calls, wdb_side_effect', [
    (['002'], [], [call('agent 002 rootcheck delete')], Xcyber360Error(2004)),
    (['001', '003'], ['001'], [call('agent 001 rootcheck delete')],
     [None, None])
])
@patch('xcyber360.rootcheck.get_agents_info', return_value={'001', '002'})
@patch('socket.socket.connect')
@pytest.mark.skip('Remove tested function or update it to use the indexer.')
def test_clear(mock_connect, mock_info, agent_list, expected_affected_items, expected_calls, wdb_side_effect):
    """Test if function clear() returns expected result and if delete command is executed.

    The databases of 4 agents are requested to be cleared, 3 of them exist.
    2 failed items are expected:
        - 1 non existent agent.
        - 1 exception when running execute() method.

    Parameters
    ----------
    agent_list : list
        List of agent IDs.
    expected_affected_items : list
        List of expected agent IDs in the result.
    expected_calls : list
        List of expected calls to the mocked Xcyber360DBConnection._send function.
    wdb_side_effect : Xcyber360Error or list
        Side effect used in the mocked Xcyber360DBConnection._send function.
    """
    with patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=wdb_side_effect) as mock_wdbconn:
        result = rootcheck.clear(agent_list).render()

        assert result['data']['affected_items'] == expected_affected_items
        assert result['data']['total_affected_items'] == len(expected_affected_items)
        assert result['data']['total_failed_items'] == len(agent_list) - len(expected_affected_items)

        mock_wdbconn.assert_has_calls(expected_calls, any_order=True)


@patch('xcyber360.core.agent.Agent.get_basic_information')
@patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=send_msg_to_wdb)
@patch('socket.socket.connect')
def test_get_last_scan(mock_connect, mock_send, mock_info):
    """Check if get_last_scan() returned results have expected format and content"""
    result = rootcheck.get_last_scan(['001']).render()['data']['affected_items'][0]
    assert result['start'] == '2020-10-27T12:19:40Z' and result['end'] == '2020-10-27T12:29:40Z'


@pytest.mark.parametrize('limit', [
    1, 3, None
])
@patch('xcyber360.core.utils.path.exists', return_value=True)
@patch('xcyber360.core.agent.Agent.get_basic_information')
@patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=send_msg_to_wdb)
@patch('socket.socket.connect')
def test_get_rootcheck_agent(mock_connect, mock_send, mock_info, mock_exists, limit):
    """Check if limit is correctly applied to get_rootcheck_agent() function

    Parameters
    ----------
    limit : int
        Number of items to be returned.
    """
    result = rootcheck.get_rootcheck_agent(agent_list=['001'], limit=limit, filters={'status': 'all'}).render()['data']
    limit = limit if limit else 6
    assert len(result['affected_items']) == limit and result['total_affected_items'] == 6
    assert len(result['failed_items']) == 0 and result['total_failed_items'] == 0

    # Check returned keys are allowed (they exist in core/rootcheck -> fields)
    for item in result['affected_items']:
        for key in item.keys():
            assert key in Xcyber360DBQueryRootcheck.fields


@pytest.mark.parametrize('select', [
    ['log'], ['log', 'pci_dss'], ['status'], None
])
@patch('xcyber360.core.utils.path.exists', return_value=True)
@patch('xcyber360.core.agent.Agent.get_basic_information')
@patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=send_msg_to_wdb)
@patch('socket.socket.connect')
def test_get_rootcheck_agent_select(mock_connect, mock_send, mock_info, mock_exists, select):
    """Check that only selected elements are returned

    Parameters
    ----------
    select : list
        Fields to be returned.
    """
    result = rootcheck.get_rootcheck_agent(agent_list=['001'], select=select, filters={'status': 'all'}).render()[
        'data']
    select = select if select else list(Xcyber360DBQueryRootcheck.fields.keys())

    # Check returned keys are specified inside 'select' field
    for item in result['affected_items']:
        for key in item.keys():
            assert key in select


@pytest.mark.parametrize('search, total_expected_items', [
    ('1.5', 4),
    ('1.6', 0),
    ('ssh', 1),
    ('robust', 3),
    ('4.1', 2),
    ('outstanding', 5),
    ('solved', 1)
])
@patch('xcyber360.core.utils.path.exists', return_value=True)
@patch('xcyber360.core.agent.Agent.get_basic_information')
@patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=send_msg_to_wdb)
@patch('socket.socket.connect')
def test_get_rootcheck_agent_search(mock_connect, mock_send, mock_info, mock_exists, search, total_expected_items):
    """Checks if the number of items returned is as expected when using the search parameter.

    Parameters
    ----------
    search : str
        String to be searched in the database.
    total_expected_items : int
        Number of expected items to be returned.
    """
    result = rootcheck.get_rootcheck_agent(agent_list=['001'], search=parse_api_param(search, 'search'),
                                           filters={'status': 'all'}).render()['data']
    assert result['total_affected_items'] == total_expected_items


@pytest.mark.parametrize('query, total_expected_items', [
    ('cis=1.4 Debian Linux', 3),
    ('log=testing', 1),
    ('log!=testing', 5),
    ('', 6),
    ('log=SSH Configuration', 0),
    ('log~SSH Configuration', 1),
    ('pci_dss<3', 4),
    ('pci_dss>3', 2),
    ('(pci_dss>3,pci_dss<2);log~System', 5),
])
@patch('xcyber360.core.utils.path.exists', return_value=True)
@patch('xcyber360.core.agent.Agent.get_basic_information')
@patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=send_msg_to_wdb)
@patch('socket.socket.connect')
def test_get_rootcheck_agent_query(mock_connect, mock_send, mock_info, mock_exists, query, total_expected_items):
    """Checks if the number of items returned is as expected when using query parameter.

    Parameters
    ----------
    query : str
        Query to be applied in the database
    total_expected_items : int
        Number of expected items to be returned.
    """
    result = rootcheck.get_rootcheck_agent(agent_list=['001'], q=query, filters={'status': 'all'}).render()['data']
    assert result['total_affected_items'] == total_expected_items


@pytest.mark.parametrize('select, distinct, total_expected_items', [
    (['cis'], True, 3),
    (['cis'], False, 6),
    (['pci_dss'], True, 2),
    (['pci_dss'], False, 6),
    (['cis', 'pci_dss'], True, 3),
    (['log'], True, 6),
])
@patch('xcyber360.core.utils.path.exists', return_value=True)
@patch('xcyber360.core.agent.Agent.get_basic_information')
@patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=send_msg_to_wdb)
@patch('socket.socket.connect')
def test_get_rootcheck_agent_distinct(mock_connect, mock_send, mock_info, mock_exists, select, distinct,
                                      total_expected_items):
    """Checks if the number of items returned is as expected when using distinct and select parameters.

    Parameters
    ----------
    select : list
        Fields to be returned.
    distinct : bool
        Whether to apply distinct filter.
    total_expected_items : int
        Number of expected items to be returned.
    """
    result = rootcheck.get_rootcheck_agent(agent_list=['001'], select=select, distinct=distinct,
                                           filters={'status': 'all'}).render()['data']
    assert result['total_affected_items'] == total_expected_items


@pytest.mark.parametrize('sort, first_item', [
    ('-log', 'Testing'),
    ('+log', '/opt'),
    ('-cis', 'Benchmark v1.0'),
    ('+cis', '/var'),
])
@patch('xcyber360.core.utils.path.exists', return_value=True)
@patch('xcyber360.core.agent.Agent.get_basic_information')
@patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=send_msg_to_wdb)
@patch('socket.socket.connect')
def test_get_rootcheck_agent_sort(mock_connect, mock_send, mock_info, mock_exists, sort, first_item):
    """Checks if the the first item returned is expected when using sort parameter

    Parameters
    ----------
    sort : str
        Field and order to sort by
    first_item : int
        Expected string to be contained in the log of the first returned element.
    """
    result = rootcheck.get_rootcheck_agent(agent_list=['001'], sort=parse_api_param(sort, 'sort'),
                                           filters={'status': 'all'}).render()['data']

    assert first_item in result['affected_items'][0]['log']


@pytest.mark.parametrize('filters, total_expected_items', [
    ({'status': 'all'}, 6),
    ({'status': 'solved'}, 1),
    ({'status': 'outstanding'}, 5),
    ({'status': 'all', 'cis': '2.3'}, 0),
    ({'status': 'all', 'cis': '1.4 Debian Linux'}, 3),
    ({'status': 'solved', 'cis': '1.4 Debian Linux'}, 0),
    ({'status': 'all', 'pci_dss': '1.5'}, 4),
    ({'status': 'all', 'pci_dss': '4.1'}, 2),
    ({'status': 'solved', 'pci_dss': '4.1'}, 1),
    ({'status': 'all', 'cis': '3.4 Debian Linux', 'pci_dss': '1.5'}, 1),
    ({'status': 'all', 'cis': '3.4 Debian Linux', 'pci_dss': '4.1'}, 0)
])
@patch('xcyber360.core.utils.path.exists', return_value=True)
@patch('xcyber360.core.agent.Agent.get_basic_information')
@patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=send_msg_to_wdb)
@patch('socket.socket.connect')
def test_get_rootcheck_agent_filters(mock_connect, mock_send, mock_info, mock_exists, filters, total_expected_items):
    """Checks if the number of items returned is as expected when using different filters.

    Parameters
    ----------
    filters : dict
        Strings to filter by.
    total_expected_items : int
        Number of expected items to be returned.
    """
    result = rootcheck.get_rootcheck_agent(agent_list=['001'], filters=filters).render()['data']
    assert result['total_affected_items'] == total_expected_items


remove_db(core_data)
