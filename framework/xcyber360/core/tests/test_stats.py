

import os
import sys
import json
from datetime import date, datetime, timezone
from unittest.mock import MagicMock, mock_open, patch, call

import pytest

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators
        from xcyber360.core import common, stats
        from xcyber360.core.exception import Xcyber360Error, Xcyber360Exception, Xcyber360InternalError
        from xcyber360.tests.util import RBAC_bypasser

        del sys.modules['xcyber360.rbac.orm']
        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser

test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'stats')


@pytest.mark.parametrize('date_', [date(2005, 5, 5)])
def test_totals_(date_):
    """Verify totals_() function works as expected"""
    data_ = '1-2-3-4\n22-34-5-3\n15--107--1483--1257--0'
    with patch("builtins.open", mock_open(read_data=data_)):
        affected = stats.totals_(date_)
        if affected:
            for line in data_:
                data = line.split('-')
                if len(data) == 4:
                    assert int(data[1]) == affected[0]['alerts'][0]['sigid']
                    assert int(data[2]) == affected[0]['alerts'][0]['level'], 'Data do not match'
                    assert int(data[3]) == affected[0]['alerts'][0]['times'], 'Data do not match'
                else:
                    data = line.split('--')
                    if len(data) == 5:
                        assert int(data[0]) == affected[0]['hour'], 'Data do not match'
                        assert int(data[1]) == affected[0]['totalAlerts'], 'Data do not match'
                        assert int(data[2]) == affected[0]['events'], 'Data do not match'
                        assert int(data[3]) == affected[0]['syscheck'], 'Data do not match'
                        assert int(data[4]) == affected[0]['firewall'], 'Data do not match'


def test_totals_ko_():
    """Verify totals_() function exception with data problems works"""
    with patch('xcyber360.core.stats.open', side_effect=IOError):
        with pytest.raises(Xcyber360Exception, match=".* 1308 .*"):
            stats.totals_(date(1996, 8, 13))

    with patch("builtins.open", mock_open(read_data='15-571-3-2\n15--107--1483')):
        with pytest.raises(Xcyber360InternalError, match=".* 1309 .*"):
            stats.totals_(date(1996, 8, 13))


@patch('xcyber360.core.common.STATS_PATH', new=test_data_path)
def test_weekly_():
    """Verify weekly_() function works as expected"""
    result = stats.weekly_()
    assert 0 == result[0]['Sun']['interactions'], 'Data do not match'
    for day in "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat":
        assert day in [d for r in result for d in r.keys()], 'Data do not match'


@patch('xcyber360.core.common.STATS_PATH', new='')
def test_weekly_data():
    """Verify weekly_() function works as expected"""
    result = stats.weekly_()
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for day in days:
        for i in range(24):
            assert 0 == result[days.index(day)][day]['hours'][i]
        assert 0 == result[days.index(day)][day]['interactions']


@patch('xcyber360.core.common.STATS_PATH', new=test_data_path)
def test_hourly_():
    """Verify hourly_() function works as expected"""
    result = stats.hourly_()
    assert 24 == result[0]['interactions'], 'Data do not match'
    for hour in range(24):
        assert hour in result[0]['averages'], 'Data do not match'


@patch('xcyber360.core.common.STATS_PATH', new='')
def test_hourly_data():
    """Test hourly_() function exceptions works"""
    result = stats.hourly_()
    for average in result[0]['averages']:
        assert average == 0, 'Data do not match'
    assert result[0]['interactions'] == 0


@pytest.mark.parametrize('agent, daemon, expected_value', [
    (1, 'logcollector', common.REMOTED_SOCKET),
    (1, 'agent', common.REMOTED_SOCKET)
])
def test_get_stats_socket_path(agent, daemon, expected_value):
    """Verify get_stats_socket_path function works as expected"""
    assert stats.get_stats_socket_path(agent, daemon) == expected_value


@pytest.mark.parametrize('agent, daemon, next_page, expected_value', [
    (1, 'agent', False, '001 agent getstate'),
    (1, 'agent', True, '001 agent getstate next'),
])
def test_create_stats_command(agent, daemon, next_page, expected_value):
    """Verify create_stats_command function works as expected"""
    assert stats.create_stats_command(agent_id=agent, daemon=daemon, next_page=next_page) == expected_value


@pytest.mark.asyncio
@pytest.mark.parametrize('agents_list, expected_socket_response, expected_result', [
    (None,
     {'timestamp': 1658400850,
      'uptime': 1658400850,
      'stats': 'value'},
     {'timestamp': datetime(2022, 7, 21, 10, 54, 10, tzinfo=timezone.utc),
      'uptime': datetime(2022, 7, 21, 10, 54, 10, tzinfo=timezone.utc),
      'stats': 'value'}),

    ([1, 2, 3],
     {'timestamp': 1658400850,
      'agents': [{'id': agent_id, 'uptime': 1658400850} for agent_id in [1, 2, 3]]},
     {'timestamp': datetime(2022, 7, 21, 10, 54, 10, tzinfo=timezone.utc),
      'agents': [{'id': agent_id, 'uptime': datetime(2022, 7, 21, 10, 54, 10, tzinfo=timezone.utc)} for agent_id in
                 [1, 2, 3]]}),

    ('all',
     {'data': {'timestamp': 1658400850,
               'agents': [{'id': agent_id, 'uptime': 1658400850} for agent_id in [1, 2, 3]]}},
     {'data': {'timestamp': datetime(2022, 7, 21, 10, 54, 10, tzinfo=timezone.utc),
               'agents': [{'id': agent_id, 'uptime': datetime(2022, 7, 21, 10, 54, 10, tzinfo=timezone.utc)} for
                          agent_id in [1, 2, 3]]}})
])
@patch('xcyber360.core.xcyber360_socket.Xcyber360AsyncSocketJSON.close')
@patch('xcyber360.core.xcyber360_socket.Xcyber360AsyncSocketJSON.send')
@patch('xcyber360.core.xcyber360_socket.Xcyber360AsyncSocketJSON.connect')
async def test_get_daemons_stats_socket(mock_connect, mock_send, mock_close, 
                                        agents_list, expected_socket_response,
                                        expected_result):
    """Verify get_daemons_stats_socket(socket : str) function works as expected"""
    socket = '/test_path/socket'
    expected_msg = {'version': 1, 'origin': {'module': 'framework'},
                    'command': 'getagentsstats' if agents_list else 'getstats'}
    if agents_list:
        expected_msg |= {'parameters': {'agents': agents_list}}
        if agents_list == 'all':
            expected_msg['parameters'] |= {'last_id': 0}

    with patch('xcyber360.core.xcyber360_socket.Xcyber360AsyncSocketJSON.receive',
               return_value=expected_socket_response) as mock_receive, \
         patch('xcyber360.core.xcyber360_socket.Xcyber360AsyncSocketJSON.receive_json',
               return_value=expected_socket_response) as mock_receive_json:
        result = await stats.get_daemons_stats_socket(socket, agents_list=agents_list,
                                                last_id=0 if agents_list == 'all' else None)

        mock_connect.assert_awaited_once_with(socket)
        mock_send.assert_awaited_once_with(expected_msg)
        if  agents_list == 'all':
            mock_receive.assert_awaited_once()
        else:
            mock_receive_json.assert_awaited_once()
        mock_close.assert_called_once()
        assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize('agents_list', [
    None, [1, 2, 3]
])
async def test_get_daemons_stats_socket_ko(agents_list):
    """Test get_daemons_stats_socket(socket : str) function exception works"""
    socket = '/test_path/socket'
    with pytest.raises(Xcyber360InternalError, match=f".* 1121 .*: {socket}"):
        await stats.get_daemons_stats_socket(socket, agents_list=agents_list)


def test_get_daemons_stats_():
    """Verify get_daemons_stats_() function works as expected"""
    with patch("builtins.open", mock_open(read_data='# Queue size\nqueue_size=\'0\'')):
        result = stats.get_daemons_stats_('')
        assert result[0] == {'queue_size': 0}


def test_get_daemons_stats_ko():
    """Test get_daemons_stats_() function exceptions works"""
    with patch('xcyber360.core.stats.open', side_effect=IOError):
        with pytest.raises(Xcyber360Exception, match=".* 1308 .*"):
            stats.get_daemons_stats_('filename')

    with patch('xcyber360.core.stats.open'):
        with pytest.raises(Xcyber360InternalError, match=".* 1104 .*"):
            stats.get_daemons_stats_('filename')


@pytest.mark.parametrize("agent_id, daemon, response", [
    ('002', 'agent', '{"error":0, "data":{"test":0}}'),
    (3, 'test', '{"error":0, "data":{"test":0}}'),
])
def test_get_daemons_stats_from_socket(agent_id, daemon, response):
    """Check that get_daemons_stats_from_socket() function uses the expected params and returns expected result"""
    with patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.__init__', return_value=None) as mock_socket:
        with patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.send', side_effect=None) as mock_send:
            with patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.receive', return_value=response.encode()):
                with patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.close', side_effect=None):
                    stats.get_daemons_stats_from_socket(agent_id, daemon)

        mock_socket.assert_called_once_with(os.path.join(common.XCYBER360_PATH, "queue", "sockets", "remote"))
        mock_send.assert_called_once_with(f"{str(agent_id).zfill(3)} {daemon} getstate".encode())


@pytest.mark.parametrize("agent_id, daemon, responses, expected, expected_socket_calls, expected_arg_calls", [
    ('001', 'logcollector', [
        '{"error":0, "remaining": true, "data":{"global": {"start": "2023-11-27 19:51:54", '
        '"end": "2023-11-27 19:52:54", "files": [1, 2]}, "interval": {}}}'.encode(),
        '{"error":0, "remaining": true, "data":{"global": {"start": "2023-11-27 19:52:54", '
        '"end": "2023-11-27 19:53:54", "files": [3, 4]}, "interval": {}}}'.encode(),
        '{"error":0, "remaining": false, "data":{"global": {"start": "2023-11-27 19:53:54", '
        '"end": "2023-11-27 19:54:54", "files": [5, 6]}, "interval": {}}}'.encode()],
     {"global": {"start": "2023-11-27T19:51:54Z", "end": "2023-11-27T19:54:54Z", "files": [1, 2, 3, 4, 5, 6]},
      "interval": {}},
     3,
     [
         call('001 logcollector getstate'.encode()),
         call('001 logcollector getstate next'.encode()),
         call('001 logcollector getstate next'.encode())]),
    ('001', 'logcollector', [
        '{"error":0, "json_updated": false, "remaining": true, "data":{"global": {"start": "2023-11-27 19:51:54", '
        '"end": "2023-11-27 19:52:54", "files": [1, 2]}, "interval": {}}}'.encode(),
        '{"error":0, "json_updated": true, "remaining": true, "data":{"global": {"start": "2023-11-27 19:52:54", '
        '"end": "2023-11-27 19:53:54", "files": [3, 4]}, "interval": {}}}'.encode(),
        '{"error":0, "json_updated": false, "remaining": false, "data":{"global": {"start": "2023-11-27 19:53:54", '
        '"end": "2023-11-27 19:54:54", "files": [5, 6]}, "interval": {}}}'.encode()],
     {"global": {"start": "2023-11-27T19:53:54Z", "end": "2023-11-27T19:54:54Z", "files": [5, 6]}, "interval": {}},
     3,
     [
         call('001 logcollector getstate'.encode()),
         call('001 logcollector getstate next'.encode()),
         call('001 logcollector getstate'.encode())]),
])
def test_get_daemons_stats_from_socket(agent_id, daemon, responses, expected, expected_socket_calls,
                                       expected_arg_calls):
    """Check that get_daemons_stats_from_socket() function uses the pagination logic"""
    with patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.__init__', return_value=None) as mock_socket:
        with patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.send', side_effect=None) as mock_send:
            with patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.receive', side_effect=responses):
                with patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.close', side_effect=None):
                    result = stats.get_daemons_stats_from_socket(agent_id, daemon)

    assert result == expected
    assert mock_send.call_count == expected_socket_calls
    mock_send.assert_has_calls(expected_arg_calls)


@pytest.mark.parametrize("data, expected", [
    ({}, {}),
    ({"start": "2023-11-27 19:51:54", "end": "2023-11-27 19:52:54", "files": [1, 2]},
     {"start": "2023-11-27T19:51:54Z", "end": "2023-11-27T19:52:54Z", "files": [1, 2]})

])
def test_pagination_handler_sets_data(data, expected):
    """Check that the PaginatedDataHandler sets the data correctly """
    test_handler = stats.PaginatedDataHandler()
    test_handler.set_data(data)

    assert expected == test_handler.to_dict()


@pytest.mark.parametrize("initial_data, data, expected", [
    ({}, {}, {}),
    ({}, {"start": "2023-11-27 19:51:54", "end": "2023-11-27 19:52:54", "files": [1, 2]},
     {"start": "2023-11-27T19:51:54Z", "end": "2023-11-27T19:52:54Z", "files": [1, 2]}),
    ({"start": "2023-11-27 19:51:54", "end": "2023-11-27 19:52:54", "files": [1, 2]},
     {"start": "2023-11-27 19:52:54", "end": "2023-11-27 19:53:54", "files": [3, 4]},
     {"start": "2023-11-27T19:51:54Z", "end": "2023-11-27T19:53:54Z", "files": [1, 2, 3, 4]}),
    ({"start": "2023-11-27 19:51:54", "end": "2023-11-27 19:52:54", "files": [1, 2]},
     {},
     {"start": "2023-11-27T19:51:54Z", "end": "2023-11-27T19:52:54Z", "files": [1, 2]})

])
def test_pagination_handler_updates_data(initial_data, data, expected):
    """Check that the PaginatedDataHandler updates the data correctly """
    test_handler = stats.PaginatedDataHandler()
    test_handler.set_data(initial_data)
    test_handler.update_data(data)

    assert expected == test_handler.to_dict()


def test_get_daemons_stats_from_socket_ko():
    """Check if get_daemons_stats_from_socket() raises expected exceptions."""
    with pytest.raises(Xcyber360Error, match=r'\b1307\b'):
        stats.get_daemons_stats_from_socket(None, None)
