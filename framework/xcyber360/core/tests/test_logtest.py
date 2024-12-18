

from unittest.mock import patch

import pytest

with patch('xcyber360.common.xcyber360_uid'):
    with patch('xcyber360.common.xcyber360_gid'):
        from xcyber360.core.logtest import send_logtest_msg, validate_dummy_logtest
        from xcyber360.core.common import LOGTEST_SOCKET
        from xcyber360.core.exception import Xcyber360Error


@pytest.mark.parametrize('params', [
    {'command': 'random_command', 'parameters': {'param1': 'value1'}},
    {'command': None, 'parameters': None}
])
@patch('xcyber360.core.logtest.Xcyber360SocketJSON.__init__', return_value=None)
@patch('xcyber360.core.logtest.Xcyber360SocketJSON.send')
@patch('xcyber360.core.logtest.Xcyber360SocketJSON.close')
@patch('xcyber360.core.logtest.create_xcyber360_socket_message')
def test_send_logtest_msg(create_message_mock, close_mock, send_mock, init_mock, params):
    """Test `send_logtest_msg` function from module core.logtest.

    Parameters
    ----------
    params : dict
        Params that will be sent to the logtest socket.
    """
    with patch('xcyber360.core.logtest.Xcyber360SocketJSON.receive',
               return_value={'data': {'response': True, 'output': {'timestamp': '1970-01-01T00:00:00.000000-0200'}}}):
        response = send_logtest_msg(**params)
        init_mock.assert_called_with(LOGTEST_SOCKET)
        create_message_mock.assert_called_with(origin={'name': 'Logtest', 'module': 'framework'}, **params)
        assert response == {'data': {'response': True, 'output': {'timestamp': '1970-01-01T02:00:00.000000Z'}}}


@patch('xcyber360.core.logtest.Xcyber360SocketJSON.__init__', return_value=None)
@patch('xcyber360.core.logtest.Xcyber360SocketJSON.send')
@patch('xcyber360.core.logtest.Xcyber360SocketJSON.close')
@patch('xcyber360.core.logtest.create_xcyber360_socket_message')
def test_validate_dummy_logtest(create_message_mock, close_mock, send_mock, init_mock):
    with patch('xcyber360.core.logtest.Xcyber360SocketJSON.receive',
               return_value={'data': {'codemsg': -1}, 'error': 0}):
        with pytest.raises(Xcyber360Error) as err_info:
            validate_dummy_logtest()

        assert err_info.value.code == 1113
