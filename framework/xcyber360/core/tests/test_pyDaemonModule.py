

from unittest.mock import MagicMock, patch
from pathlib import Path
import pytest

from xcyber360.core.pyDaemonModule import *
from xcyber360.core.exception import Xcyber360Exception
from tempfile import NamedTemporaryFile, TemporaryDirectory


@pytest.mark.parametrize('effect', [
   None,
   OSError(10000, 'Error')
])
@patch('xcyber360.core.pyDaemonModule.sys.exit')
@patch('xcyber360.core.pyDaemonModule.os.setsid')
@patch('xcyber360.core.pyDaemonModule.sys.stderr.write')
@patch('xcyber360.core.pyDaemonModule.sys.stdin.fileno')
@patch('xcyber360.core.pyDaemonModule.os.dup2')
@patch('xcyber360.core.pyDaemonModule.os.chdir')
def test_pyDaemon(mock_chdir, mock_dup, mock_fileno, mock_write, mock_setsid, mock_exit, effect):
    """Tests pyDaemon function works"""

    with patch('xcyber360.core.pyDaemonModule.os.fork', return_value=255, side_effect=effect):
        pyDaemon()

    if effect == None:
        mock_exit.assert_called_with(0)
    else:
        mock_exit.assert_called_with(1)
    mock_setsid.assert_called_once_with()
    mock_chdir.assert_called_once_with('/')


@patch('xcyber360.core.pyDaemonModule.common.XCYBER360_RUN', new=Path('/tmp'))
def test_create_pid():
    """Tests create_pid function works"""

    with TemporaryDirectory() as tmpdirname:
        tmpfile = NamedTemporaryFile(dir=tmpdirname, delete=False, suffix='-255.pid')
        create_pid(tmpfile.name.split('/')[3].split('-')[0], '255')


@patch('xcyber360.core.pyDaemonModule.common.XCYBER360_RUN', new=Path('/tmp'))
@patch('xcyber360.core.pyDaemonModule.os.chmod', side_effect=OSError)
def test_create_pid_ko(mock_chmod):
    """Tests create_pid function exception works"""

    with TemporaryDirectory() as tmpdirname:
        tmpfile = NamedTemporaryFile(dir=tmpdirname, delete=False, suffix='-255.pid')
        with pytest.raises(Xcyber360Exception, match=".* 3002 .*"):
            create_pid(tmpfile.name.split('/')[3].split('-')[0], '255')


@pytest.mark.parametrize('process_name, expected_pid', [
   ('foo', 123),
   ('bar', 456),
   ('xcyber360-apid', 789),
   ('xcyber360-clusterd', None)
])
@patch('os.listdir', return_value=['foo-123.pid', 'bar-456.pid', 'xcyber360-apid-789.pid'])
def test_get_parent_pid(os_listdir_mock, expected_pid, process_name):
    """Validates that the get_parent_pid function works as expected."""
    actual_pid = get_parent_pid(process_name)
    assert expected_pid == actual_pid


def test_delete_pid():
    """Tests delete_pid function works"""

    with TemporaryDirectory() as tmpdirname:
        tmpfile = NamedTemporaryFile(dir=tmpdirname, delete=False, suffix='-255.pid')
        with patch('xcyber360.core.pyDaemonModule.common.XCYBER360_RUN', new=Path(tmpdirname.split('/')[2])):
            delete_pid(tmpfile.name.split('/')[3].split('-')[0], '255')

@patch('xcyber360.core.pyDaemonModule.next')
@patch('xcyber360.core.pyDaemonModule.Path')
def test_get_xcyber360_server_pid(path_mock, next_mock):
    """Validate that `get_xcyber360_server_pid` works as expected."""
    pid = 123
    daemon_name = 'xcyber360-server'
    xcyber360_server_pid = f'{daemon_name}-{pid}'
    next_mock.return_value = MagicMock(stem=xcyber360_server_pid)

    assert get_xcyber360_server_pid(daemon_name) == pid


@patch('xcyber360.core.pyDaemonModule.next', side_effect=StopIteration)
@patch('xcyber360.core.pyDaemonModule.Path')
def test_get_xcyber360_server_pid_ko(path_mock, next_mock):
    """Validate that `get_xcyber360_server_pid` works as expected when the server is not running."""
    daemon_name = 'xcyber360-server'
    with pytest.raises(StopIteration):
        get_xcyber360_server_pid(daemon_name)


@patch('xcyber360.core.pyDaemonModule.Path')
def test_get_running_processes(path_mock):
    """Validate that `get_running_processes` works as expected."""
    daemons = ['xcyber360-server', 'xcyber360-apid', 'xcyber360-comms-apid', 'xcyber360-engine']
    path_mock.return_value.glob.return_value = (MagicMock(stem=f'{daemon}-{i}') for i, daemon in enumerate(daemons))

    assert get_running_processes() == daemons