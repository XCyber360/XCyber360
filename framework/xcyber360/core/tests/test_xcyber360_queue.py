

from unittest.mock import patch
import socket

import pytest
from xcyber360.core.exception import Xcyber360Exception
from xcyber360.core.xcyber360_queue import BaseQueue, Xcyber360AnalysisdQueue, Xcyber360Queue


@patch('xcyber360.core.xcyber360_queue.BaseQueue._connect')
def test_BaseQueue__init__(mock_conn):
    """Test BaseQueue.__init__ function."""

    BaseQueue('test_path')

    mock_conn.assert_called_once_with()


@patch('xcyber360.core.xcyber360_queue.BaseQueue.close')
@patch('xcyber360.core.xcyber360_queue.socket.socket.connect')
def test_BaseQueue__enter__(mock_conn, mock_close):
    """Test BaseQueue.__enter__ function."""
    with BaseQueue('test_path') as wq:
        assert isinstance(wq, BaseQueue)


@patch('xcyber360.core.xcyber360_queue.BaseQueue.close')
@patch('xcyber360.core.xcyber360_queue.socket.socket.connect')
def test_BaseQueue__exit__(mock_connect, mock_close):
    """Test BaseQueue.__exit__ function."""
    with BaseQueue('test_path'):
        pass

    mock_close.assert_called_once()


@patch('xcyber360.core.xcyber360_queue.socket.socket.connect')
@patch('xcyber360.core.xcyber360_queue.socket.socket.setsockopt')
def test_BaseQueue_protected_connect(mock_set, mock_conn):
    """Test BaseQueue._connect function."""

    BaseQueue('test_path')

    with patch('xcyber360.core.xcyber360_queue.socket.socket.getsockopt', return_value=1):
        BaseQueue('test_path')

    mock_conn.assert_called_with('test_path')
    mock_set.assert_called_once_with(1, 7, 6400)


@patch('xcyber360.core.xcyber360_queue.socket.socket.connect', side_effect=Exception)
def test_BaseQueue_protected_connect_ko(mock_conn):
    """Test BaseQueue._connect function exceptions."""

    with pytest.raises(Xcyber360Exception, match=".* 1010 .*"):
        BaseQueue('test_path')


@pytest.mark.parametrize('send_response, error', [
    (1, False),
    (0, True)
])
@patch('xcyber360.core.xcyber360_queue.socket.socket.connect')
@patch('xcyber360.core.xcyber360_queue.BaseQueue.MAX_MSG_SIZE', new=0)
def test_BaseQueue_protected_send(mock_conn, send_response, error):
    """Test BaseQueue._send function.

    Parameters
    ----------
    send_response : int
        Returned value of the socket send mocked function.
    error : bool
        Indicates whether a Xcyber360Exception will be raised or not.
    """

    queue = BaseQueue('test_path')

    with patch('socket.socket.send', return_value=send_response):
        if error:
            with pytest.raises(Xcyber360Exception, match=".* 1011 .*"):
                queue._send('msg')
        else:
            queue._send('msg')

    mock_conn.assert_called_with('test_path')


@pytest.mark.parametrize(
        "errno,match",
        [(1, ".* 1011 .*")]
)
@patch('xcyber360.core.xcyber360_queue.socket.socket.connect')
@patch('xcyber360.core.xcyber360_queue.BaseQueue.MAX_MSG_SIZE', new=0)
@patch('socket.socket.send')
def test_BaseQueue_protected_send_ko(mock_send, mock_conn, errno, match):
    """Test BaseQueue._send function exceptions."""
    error = socket.error()
    error.errno = errno
    mock_send.side_effect = error

    queue = BaseQueue('test_path')
    with pytest.raises(Xcyber360Exception, match=match):
        queue._send('msg'.encode())

    mock_conn.assert_called_with('test_path')


@patch('xcyber360.core.xcyber360_queue.socket.socket.connect')
@patch('xcyber360.core.xcyber360_queue.socket.socket.close')
def test_BaseQueue_close(mock_close, mock_conn):
    """Test BaseQueue.close function."""

    with BaseQueue('test_path'):
        pass

    mock_conn.assert_called_once_with('test_path')
    mock_close.assert_called_once_with()


@pytest.mark.parametrize('msg, agent_id, msg_type', [
    ('test_msg', '000', 'ar-message'),
    ('test_msg', '001', 'ar-message'),
    ('test_msg', None, 'ar-message'),
    ('syscheck restart', '000', None),
    ('force_reconnect', '000', None),
    ('restart-ossec0', '001', None),
    ('syscheck restart', None, None),
    ('force_reconnect', None, None),
    ('restart-ossec0', None, None)
])
@patch('xcyber360.core.xcyber360_queue.socket.socket.connect')
@patch('xcyber360.core.xcyber360_queue.Xcyber360Queue._send')
def test_Xcyber360Queue_send_msg_to_agent(mock_send, mock_conn, msg, agent_id, msg_type):
    """Test Xcyber360Queue.send_msg_to_agent function.

    Parameters
    ----------
    msg : str
        Message sent to the agent.
    agent_id : str
        String indicating the agent ID.
    msg_type : str
        String indicating the message type.
    """

    queue = Xcyber360Queue('test_path')

    response = queue.send_msg_to_agent(msg, agent_id, msg_type)

    assert isinstance(response, str)
    mock_conn.assert_called_once_with('test_path')


@pytest.mark.parametrize('msg, agent_id, msg_type, expected_exception', [
    ('test_msg', '000', None, 1012),
    ('syscheck restart', None, None, 1014),
])
@patch('xcyber360.core.xcyber360_queue.socket.socket.connect')
@patch('xcyber360.core.xcyber360_queue.Xcyber360Queue._send', side_effect=Exception)
def test_Xcyber360Queue_send_msg_to_agent_ko(mock_send, mock_conn, msg, agent_id, msg_type, expected_exception):
    """Test Xcyber360Queue.send_msg_to_agent function exceptions.

    Parameters
    ----------
    msg : str
        Message sent to the agent.
    agent_id : str
        String indicating the agent ID.
    msg_type : str
        String indicating the message type.
    expected_exception : int
        Expected Xcyber360 exception.
    """

    queue = Xcyber360Queue('test_path')

    with pytest.raises(Xcyber360Exception, match=f'.* {expected_exception} .*'):
        queue.send_msg_to_agent(msg, agent_id, msg_type)

    mock_conn.assert_called_once_with('test_path')


@patch('xcyber360.core.xcyber360_queue.socket.socket.connect')
@patch('xcyber360.core.xcyber360_queue.Xcyber360AnalysisdQueue._send')
def test_Xcyber360AnalysisdQueue_send_msg(mock_send, mock_conn):
    """Test Xcyber360AnalysisdQueue.send_msg function."""

    queue = Xcyber360AnalysisdQueue('test_path')

    msg_header = '1:Head:'
    msg = "{'foo': 1}"

    queue.send_msg(msg_header=msg_header, msg=msg)

    mock_conn.assert_called_once_with('test_path')
    mock_send.assert_called_once_with(f'{msg_header}{msg}'.encode())


@pytest.mark.parametrize(
        "max_msg_size,expected_error_code",
        ([20, 1014], [1, 1012])
)
@patch('xcyber360.core.xcyber360_queue.socket.socket.connect')
@patch('xcyber360.core.xcyber360_queue.Xcyber360AnalysisdQueue._send', side_effect=Exception)
def test_Xcyber360AnalysisdQueue_send_msg_ko(mock_send, mock_conn, max_msg_size, expected_error_code):
    """Test Xcyber360AnalysisdQueue.send_msg function exceptions."""

    queue = Xcyber360AnalysisdQueue('test_path')
    queue.MAX_MSG_SIZE = max_msg_size

    with pytest.raises(Xcyber360Exception, match=f'.* {expected_error_code} .*'):
        queue.send_msg(msg_header='1:Head:', msg="{'foo': 1}")

    mock_conn.assert_called_once_with('test_path')
