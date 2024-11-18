

import sys
from datetime import date
from json import dumps
from unittest.mock import call, MagicMock, patch

import pytest

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        with patch('xcyber360.core.utils.load_xcyber360_xml'):
            sys.modules['xcyber360.rbac.orm'] = MagicMock()
            import xcyber360.rbac.decorators
            from xcyber360.tests.util import RBAC_bypasser

            del sys.modules['xcyber360.rbac.orm']
            xcyber360.rbac.decorators.expose_resources = RBAC_bypasser

            import xcyber360.stats as stats
            from xcyber360.core.results import AffectedItemsXcyber360Result
            from api.util import remove_nones_to_dict
            from xcyber360.core.tests.test_agent import InitAgent

SOCKET_PATH_DAEMONS_MAPPING = {'/var/ossec/queue/sockets/remote': 'xcyber360-remoted',
                               '/var/ossec/queue/sockets/analysis': 'xcyber360-analysisd'}
DAEMON_SOCKET_PATHS_MAPPING = {'xcyber360-remoted': '/var/ossec/queue/sockets/remote',
                               'xcyber360-analysisd': '/var/ossec/queue/sockets/analysis'}

test_data = InitAgent()


def send_msg_to_wdb(msg, raw=False):
    query = ' '.join(msg.split(' ')[2:])
    result = list(map(remove_nones_to_dict, map(dict, test_data.cur.execute(query).fetchall())))
    return ['ok', dumps(result)] if raw else result


def test_totals():
    """Verify totals() function works and returns correct data"""
    with patch('xcyber360.stats.totals_', return_value=({})):
        response = stats.totals(date(2019, 8, 13))
        assert response.total_affected_items == len(response.affected_items)
        assert isinstance(response, AffectedItemsXcyber360Result), 'The result is not Xcyber360Result type'


def test_hourly():
    """Makes sure hourly() fit with the expected."""
    response = stats.hourly()
    assert isinstance(response, AffectedItemsXcyber360Result), 'The result is not Xcyber360Result type'
    assert response.total_affected_items == len(response.affected_items)


def test_weekly():
    """Makes sure weekly() fit with the expected."""
    response = stats.weekly()
    assert isinstance(response, AffectedItemsXcyber360Result), 'The result is not Xcyber360Result type'
    assert response.total_affected_items == len(response.affected_items)


@pytest.mark.asyncio
@patch('xcyber360.core.common.REMOTED_SOCKET', '/var/ossec/queue/sockets/remote')
@patch('xcyber360.core.common.ANALYSISD_SOCKET', '/var/ossec/queue/sockets/analysis')
@patch('xcyber360.core.common.WDB_SOCKET', '/var/ossec/queue/db/wdb')
@patch('xcyber360.stats.get_daemons_stats_socket')
async def test_get_daemons_stats(mock_get_daemons_stats_socket):
    """Makes sure get_daemons_stats() fit with the expected."""
    response = await stats.get_daemons_stats(['xcyber360-remoted', 'xcyber360-analysisd', 'xcyber360-db'])

    calls = [call('/var/ossec/queue/sockets/remote'), call('/var/ossec/queue/sockets/analysis'),
             call('/var/ossec/queue/db/wdb')]
    mock_get_daemons_stats_socket.assert_has_calls(calls)
    assert isinstance(response, AffectedItemsXcyber360Result), \
            'The result is not AffectedItemsXcyber360Result type'
    assert response.total_affected_items == len(response.affected_items)


@pytest.mark.asyncio
@patch('xcyber360.core.common.REMOTED_SOCKET', '/var/ossec/queue/sockets/wrong_socket_name')
async def test_get_daemons_stats_ko():
    """Makes sure get_daemons_stats() fit with the expected."""
    response = await stats.get_daemons_stats(['xcyber360-remoted'])

    assert isinstance(response, AffectedItemsXcyber360Result), \
        'The result is not AffectedItemsXcyber360Result type'

    assert response.render()['data']['failed_items'][0]['error']['code'] == 1121, \
        'Expected error code was not returned'


def side_effect_test_get_daemons_stats(daemon_path, agents_list):
    return {'name': SOCKET_PATH_DAEMONS_MAPPING[daemon_path], 'agents': [{'id': a} for a in agents_list]}


@pytest.mark.asyncio
@pytest.mark.parametrize('daemons_list, expected_daemons_list', [
    ([], ['xcyber360-remoted', 'xcyber360-analysisd']),
    (['xcyber360-remoted'], ['xcyber360-remoted']),
    (['xcyber360-remoted', 'xcyber360-analysisd'], ['xcyber360-remoted', 'xcyber360-analysisd'])
])
@patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=send_msg_to_wdb)
@patch('socket.socket.connect')
@patch('xcyber360.stats.get_agents_info', return_value={'001', '002', '003', '004', '005'})
@patch('xcyber360.core.common.REMOTED_SOCKET', '/var/ossec/queue/sockets/remote')
@patch('xcyber360.core.common.ANALYSISD_SOCKET', '/var/ossec/queue/sockets/analysis')
@patch('xcyber360.stats.get_daemons_stats_socket', side_effect=side_effect_test_get_daemons_stats)
async def test_get_daemons_stats_agents(mock_get_daemons_stats_socket, mock_get_agents_info,
                                        mock_socket_connect, mock_send_wdb,
                                        daemons_list, expected_daemons_list):
    """Makes sure get_daemons_stats_agents() fit with the expected."""
    agents_list = ['001', '004', '999']  # Only stats from 001 are obtained
    expected_errors_and_items = {'1701': {'999'}, '1707': {'004'}}
    result = await stats.get_daemons_stats_agents(daemons_list, agents_list)

    # get_daemons_stats_socket called with the expected parameters
    calls = [call(DAEMON_SOCKET_PATHS_MAPPING[daemon], agents_list=[1])
             for daemon in expected_daemons_list]
    mock_get_daemons_stats_socket.assert_has_calls(calls)

    # Check affected_items
    assert result.affected_items == [{'name': daemon, 'agents': [{'id': 1}]}
                                     for daemon in expected_daemons_list]
    assert result.total_affected_items == len(expected_daemons_list)

    # Check failed items
    error_codes_in_failed_items = [error.code for error in result.failed_items.keys()]
    failed_items = list(result.failed_items.values())
    errors_and_items = {str(error): failed_items[i]
                        for i, error in enumerate(error_codes_in_failed_items)}
    assert expected_errors_and_items == errors_and_items

    assert isinstance(result, AffectedItemsXcyber360Result), \
        'The result is not an AffectedItemsXcyber360Result object'


def side_effect_test_get_daemons_stats_all(daemon_path, agents_list, last_id):
    # side_effect used to return a response with 10 items and 'due' the first time that get_daemons_stats_socket is
    # called, and a response with 10 items and 'ok' the second time
    if last_id:
        last_id += 1
    return {'data': {'name': SOCKET_PATH_DAEMONS_MAPPING[daemon_path],
                     'agents': [{'id': i} for i in range(last_id, last_id + 10)]},
            'message': 'due' if last_id == 0 else 'ok',
            'error': 1 if last_id == 0 else 0}


@pytest.mark.asyncio
@pytest.mark.parametrize('daemons_list, expected_daemons_list', [
    ([], ['xcyber360-remoted', 'xcyber360-analysisd']),
    (['xcyber360-remoted'], ['xcyber360-remoted']),
    (['xcyber360-remoted', 'xcyber360-analysisd'], ['xcyber360-remoted', 'xcyber360-analysisd'])
])
@patch('xcyber360.core.common.REMOTED_SOCKET', '/var/ossec/queue/sockets/remote')
@patch('xcyber360.core.common.ANALYSISD_SOCKET', '/var/ossec/queue/sockets/analysis')
@patch('xcyber360.stats.get_daemons_stats_socket', side_effect=side_effect_test_get_daemons_stats_all)
async def test_get_daemons_stats_all_agents(mock_get_daemons_stats_socket,
                                            daemons_list, expected_daemons_list):
    """Makes sure get_daemons_stats_agents() fit with the expected."""
    result = await stats.get_daemons_stats_agents(daemons_list, ['all'])

    # get_daemons_stats_socket called with the expected parameters
    calls = []
    for daemon in expected_daemons_list:
        calls.extend((call(DAEMON_SOCKET_PATHS_MAPPING[daemon], agents_list='all', last_id=0),
                      call(DAEMON_SOCKET_PATHS_MAPPING[daemon], agents_list='all', last_id=9)))
    mock_get_daemons_stats_socket.assert_has_calls(calls)

    # Check affected_items
    expected_affected_items = [{'name': daemon, 'agents': [{'id': i} for i in range(0, 20)]}
                               for daemon in expected_daemons_list]
    assert result.affected_items == expected_affected_items
    assert result.total_affected_items == len(expected_daemons_list)

    # Check failed items
    assert not result.failed_items

    assert isinstance(result, AffectedItemsXcyber360Result), \
        'The result is not an AffectedItemsXcyber360Result object'


@patch('xcyber360.stats.get_daemons_stats_', return_value=[{"events_decoded": 1.0}])
def test_deprecated_get_daemons_stats(mock_daemons_stats_):
    """Makes sure deprecated_get_daemons_stats() fit with the expected."""
    response = stats.deprecated_get_daemons_stats('filename')
    assert isinstance(response, AffectedItemsXcyber360Result), 'The result is not Xcyber360Result type'
    assert response.total_affected_items == len(response.affected_items)


@pytest.mark.parametrize('component', [
    'logcollector', 'test'
])
@patch('xcyber360.core.agent.Agent.get_stats')
@patch('xcyber360.stats.get_agents_info', return_value=['001'])
@pytest.mark.skip('Remove tested function or update it to use the indexer.')
def test_get_agents_component_stats_json(mock_agents_info, mock_getstats, component):
    """Test `get_agents_component_stats_json` function from agent module."""
    response = stats.get_agents_component_stats_json(agent_list=['001'], component=component)
    assert isinstance(response, AffectedItemsXcyber360Result), 'The result is not AffectedItemsXcyber360Result type'
    mock_getstats.assert_called_once_with(component=component)


@patch('xcyber360.core.agent.Agent.get_stats')
@patch('xcyber360.stats.get_agents_info', return_value=['001'])
@pytest.mark.skip('Remove tested function or update it to use the indexer.')
def test_get_agents_component_stats_json_ko(mock_agents_info, mock_getstats):
    """Test `get_agents_component_stats_json` function from agent module."""
    response = stats.get_agents_component_stats_json(agent_list=['003'], component='logcollector')
    assert isinstance(response, AffectedItemsXcyber360Result), 'The result is not AffectedItemsXcyber360Result type'
    assert response.render()['data']['failed_items'][0]['error']['code'] == 1701, 'Expected error code was not returned'
