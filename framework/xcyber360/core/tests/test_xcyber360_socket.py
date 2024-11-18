

from unittest.mock import patch, MagicMock, call
from asyncio import BaseEventLoop, BaseProtocol, StreamWriter, StreamReader, BaseTransport
from struct import pack

import pytest
from xcyber360.core.exception import Xcyber360Exception
from xcyber360.core.xcyber360_socket import Xcyber360Socket, Xcyber360SocketJSON, \
     SOCKET_COMMUNICATION_PROTOCOL_VERSION, create_xcyber360_socket_message, Xcyber360AsyncSocket, \
     Xcyber360AsyncSocketJSON

@pytest.fixture
def aux_conn_patch():
    """Fixture with asyncio.open_unix_connection patched."""
    return patch('asyncio.open_unix_connection',
                 return_value=(StreamReader(),StreamWriter(protocol=BaseProtocol(),
                                                           transport=BaseTransport(),
                                                           loop=BaseEventLoop(),
                                                           reader=None)))


@pytest.mark.asyncio
@pytest.fixture
async def connected_xcyber360_async_socket(aux_conn_patch):
    """Fixture to instantiate Xcyber360AsyncSocket."""
    with aux_conn_patch:
        s = Xcyber360AsyncSocket()
        await s.connect('/any/pipe')
        yield s


@patch('xcyber360.core.xcyber360_socket.Xcyber360Socket._connect')
def test_Xcyber360Socket__init__(mock_conn):
    """Tests Xcyber360Socket.__init__ function works"""

    Xcyber360Socket('test_path')

    mock_conn.assert_called_once_with()


@patch('xcyber360.core.xcyber360_socket.socket.socket.connect')
def test_Xcyber360Socket_protected_connect(mock_conn):
    """Tests Xcyber360Socket._connect function works"""

    Xcyber360Socket('test_path')

    mock_conn.assert_called_with('test_path')


@patch('xcyber360.core.xcyber360_socket.socket.socket.connect', side_effect=Exception)
def test_Xcyber360Socket_protected_connect_ko(mock_conn):
    """Tests Xcyber360Socket._connect function exceptions works"""

    with pytest.raises(Xcyber360Exception, match=".* 1013 .*"):
        Xcyber360Socket('test_path')


@patch('xcyber360.core.xcyber360_socket.socket.socket.connect')
@patch('xcyber360.core.xcyber360_socket.socket.socket.close')
def test_Xcyber360Socket_close(mock_close, mock_conn):
    """Tests Xcyber360Socket.close function works"""

    queue = Xcyber360Socket('test_path')

    queue.close()

    mock_conn.assert_called_once_with('test_path')
    mock_close.assert_called_once_with()


@patch('xcyber360.core.xcyber360_socket.socket.socket.connect')
@patch('xcyber360.core.xcyber360_socket.socket.socket.send')
def test_Xcyber360Socket_send(mock_send, mock_conn):
    """Tests Xcyber360Socket.send function works"""

    queue = Xcyber360Socket('test_path')

    response = queue.send(b"\x00\x01")

    assert isinstance(response, MagicMock)
    mock_conn.assert_called_once_with('test_path')


@pytest.mark.parametrize('msg, effect, send_effect, expected_exception', [
    ('text_msg', 'side_effect', None, 1105),
    (b"\x00\x01", 'return_value', 0, 1014),
    (b"\x00\x01", 'side_effect', Exception, 1014)
])
@patch('xcyber360.core.xcyber360_socket.socket.socket.connect')
def test_Xcyber360Socket_send_ko(mock_conn, msg, effect, send_effect, expected_exception):
    """Tests Xcyber360Socket.send function exceptions works"""

    queue = Xcyber360Socket('test_path')

    if effect == 'return_value':
        with patch('xcyber360.core.xcyber360_socket.socket.socket.send', return_value=send_effect):
            with pytest.raises(Xcyber360Exception, match=f'.* {expected_exception} .*'):
                queue.send(msg)
    else:
        with patch('xcyber360.core.xcyber360_socket.socket.socket.send', side_effect=send_effect):
            with pytest.raises(Xcyber360Exception, match=f'.* {expected_exception} .*'):
                queue.send(msg)

    mock_conn.assert_called_once_with('test_path')


@patch('xcyber360.core.xcyber360_socket.socket.socket.connect')
@patch('xcyber360.core.xcyber360_socket.unpack', return_value='1024')
@patch('xcyber360.core.xcyber360_socket.socket.socket.recv')
def test_Xcyber360Socket_receive(mock_recv, mock_unpack, mock_conn):
    """Tests Xcyber360Socket.receive function works"""

    queue = Xcyber360Socket('test_path')

    response = queue.receive()

    assert isinstance(response, MagicMock)
    mock_conn.assert_called_once_with('test_path')


@patch('xcyber360.core.xcyber360_socket.socket.socket.connect')
@patch('xcyber360.core.xcyber360_socket.socket.socket.recv', side_effect=Exception)
def test_Xcyber360Socket_receive_ko(mock_recv, mock_conn):
    """Tests Xcyber360Socket.receive function exception works"""

    queue = Xcyber360Socket('test_path')

    with pytest.raises(Xcyber360Exception, match=".* 1014 .*"):
        queue.receive()

    mock_conn.assert_called_once_with('test_path')


@patch('xcyber360.core.xcyber360_socket.Xcyber360Socket._connect')
def test_Xcyber360SocketJSON__init__(mock_conn):
    """Tests Xcyber360SocketJSON.__init__ function works"""

    Xcyber360SocketJSON('test_path')

    mock_conn.assert_called_once_with()


@patch('xcyber360.core.xcyber360_socket.socket.socket.connect')
@patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.send')
def test_Xcyber360SocketJSON_send(mock_send, mock_conn):
    """Tests Xcyber360SocketJSON.send function works"""

    queue = Xcyber360SocketJSON('test_path')

    response = queue.send('test_msg')

    assert isinstance(response, MagicMock)
    mock_conn.assert_called_once_with('test_path')


@pytest.mark.parametrize('raw', [
    True, False
])
@patch('xcyber360.core.xcyber360_socket.socket.socket.connect')
@patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.receive')
@patch('xcyber360.core.xcyber360_socket.loads', return_value={'error':0, 'message':None, 'data':'Ok'})
def test_Xcyber360SocketJSON_receive(mock_loads, mock_receive, mock_conn, raw):
    """Tests Xcyber360SocketJSON.receive function works"""
    queue = Xcyber360SocketJSON('test_path')
    response = queue.receive(raw=raw)
    if raw:
        assert isinstance(response, dict)
    else:
        assert isinstance(response, str)
    mock_conn.assert_called_once_with('test_path')


@patch('xcyber360.core.xcyber360_socket.socket.socket.connect')
@patch('xcyber360.core.xcyber360_socket.Xcyber360Socket.receive')
@patch('xcyber360.core.xcyber360_socket.loads', return_value={'error':10000, 'message':'Error', 'data':'KO'})
def test_Xcyber360SocketJSON_receive_ko(mock_loads, mock_receive, mock_conn):
    """Tests Xcyber360SocketJSON.receive function works"""

    queue = Xcyber360SocketJSON('test_path')

    with pytest.raises(Xcyber360Exception, match=".* 10000 .*"):
        queue.receive()

    mock_conn.assert_called_once_with('test_path')


@pytest.mark.parametrize('origin, command, parameters', [
    ('origin_sample', 'command_sample', {'sample': 'sample'}),
    (None, 'command_sample', {'sample': 'sample'}),
    ('origin_sample', None, {'sample': 'sample'}),
    ('origin_sample', 'command_sample', None),
    (None, None, None)
])
def test_create_xcyber360_socket_message(origin, command, parameters):
    """Test create_xcyber360_socket_message function."""
    response_message = create_xcyber360_socket_message(origin, command, parameters)
    assert response_message['version'] == SOCKET_COMMUNICATION_PROTOCOL_VERSION
    assert response_message.get('origin') == origin
    assert response_message.get('command') == command
    assert response_message.get('parameters') == parameters


@pytest.mark.asyncio
async def test_xcyber360_async_socket_connect():
    """Test socket connection."""
    s = Xcyber360AsyncSocket()
    with patch('asyncio.open_unix_connection',
               return_value=(StreamReader(),
                             StreamWriter(protocol=BaseProtocol(),
                                          transport=BaseTransport(),
                                          loop=BaseEventLoop(),
                                          reader=StreamReader()))) as mock_open:
        await s.connect(path_to_socket='/etc/socket/path')
        assert isinstance(s.reader, StreamReader, )
        assert isinstance(s.writer, StreamWriter)
        mock_open.assert_awaited_once_with('/etc/socket/path')


@pytest.mark.parametrize('exception', [(ValueError()),(OSError),(FileNotFoundError),((AttributeError()))])
async def test_xcyber360_async_socket_connect_ko(exception):
    """Test socket connection errors."""
    s = Xcyber360AsyncSocket()
    aux_conn_patch.side_effect = exception
    with patch('asyncio.open_unix_connection', side_effect=exception):
        with pytest.raises(Xcyber360Exception) as exc_info:
            await s.connect(path_to_socket='/etc/socket/path')

    assert exc_info.value.code == 1013
    assert exc_info.errisinstance(Xcyber360Exception)


@pytest.mark.asyncio
async def test_xcyber360_async_socket_receive(connected_xcyber360_async_socket: Xcyber360AsyncSocket):
    """Test receive function."""
    with patch.object(connected_xcyber360_async_socket.reader, 'read',
                      side_effect=[b'\x05\x00\x00\x00', b'12345']) as read_patch:
        data = await connected_xcyber360_async_socket.receive()
        assert data == b'12345'
        read_patch.assert_has_awaits([call(4), call(5)])


@pytest.mark.asyncio
async def test_xcyber360_async_socket_receive_ko(connected_xcyber360_async_socket: Xcyber360AsyncSocket):
    """Test receive function."""
    with patch.object(connected_xcyber360_async_socket.reader, 'read',
                      side_effect=Exception()):
        with pytest.raises(Xcyber360Exception) as exc_info:
            await connected_xcyber360_async_socket.receive()
    assert exc_info.value.code == 1014
    assert exc_info.errisinstance(Xcyber360Exception)


@pytest.mark.asyncio
async def test_xcyber360_async_socket_send(connected_xcyber360_async_socket: Xcyber360AsyncSocket):
    """Test receive function."""
    d_bytes = b'12345'
    with patch.object(connected_xcyber360_async_socket.writer, 'write') as write_patch,\
         patch.object(connected_xcyber360_async_socket.writer, 'drain') as drain_patch:
        await connected_xcyber360_async_socket.send(d_bytes)
        bytes_sent = pack('<I', len(d_bytes)) + d_bytes
        write_patch.assert_called_once_with(bytes_sent)
        drain_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_xcyber360_async_socket_send_ko(connected_xcyber360_async_socket: Xcyber360AsyncSocket):
    """Test receive function."""
    with patch.object(connected_xcyber360_async_socket.writer, 'write',
                      side_effect=OSError()):
        with pytest.raises(Xcyber360Exception) as exc_info:
            await connected_xcyber360_async_socket.send(b'12345')
    assert exc_info.value.code == 1014
    assert exc_info.errisinstance(Xcyber360Exception)


def test_xcyber360_async_socket_close(connected_xcyber360_async_socket: Xcyber360AsyncSocket):
    """Test receive function."""

    with patch.object(connected_xcyber360_async_socket.writer, 'close') as close_patch:
        connected_xcyber360_async_socket.close()
        close_patch.assert_called_once()


@pytest.mark.asyncio
async def test_xcyber360_async_json_socket_receive_json():
    """Test receive_json function."""

    s = Xcyber360AsyncSocketJSON()
    with patch.object(Xcyber360AsyncSocket,
                      'receive', return_value=b'{"data": {"field":"value"}}') as receive_patch:
        msg = await s.receive_json()
        receive_patch.assert_called_once()
        assert msg['field'] == 'value'


@pytest.mark.asyncio
async def test_xcyber360_async_json_socket_receive_json_ko():
    """Test receive_json function."""

    s = Xcyber360AsyncSocketJSON()
    with patch.object(Xcyber360AsyncSocket, 'receive',
                      return_value=b'{"error": 1000, "message": "error message"}'):
        with pytest.raises(Xcyber360Exception) as exc_info:
            await s.receive_json()
        exc_info.errisinstance(Xcyber360Exception)
        assert exc_info.value.code == 1000
