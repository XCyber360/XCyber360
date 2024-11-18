import os
import pytest
import subprocess
import sys
from unittest.mock import Mock, patch

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from utils import find_xcyber360_path, call_xcyber360_control, get_xcyber360_info, get_xcyber360_version


@pytest.mark.parametrize('path, expected', [
    ('/var/ossec/wodles/aws', '/var/ossec'),
    ('/my/custom/path/wodles/aws', '/my/custom/path'),
    ('/my/fake/path', '')
])
def test_find_xcyber360_path(path, expected):
    """Validate that the Xcyber360 absolute path is returned successfully."""
    with patch('utils.__file__', new=path):
        assert (find_xcyber360_path.__wrapped__() == expected)


def test_find_xcyber360_path_relative_path():
    """Validate that the Xcyber360 relative path is returned successfully."""
    with patch('os.path.abspath', return_value='~/wodles'):
        assert (find_xcyber360_path.__wrapped__() == '~')


@patch("subprocess.Popen")
@pytest.mark.parametrize('option', ['info', 'status'])
def test_call_xcyber360_control(mock_popen, option):
    """Validate that the call_xcyber360_control function works correctly."""
    b_output = b'output'
    process_mock = Mock()
    attrs = {'communicate.return_value': (b_output, b'error')}
    process_mock.configure_mock(**attrs)
    mock_popen.return_value = process_mock

    output = call_xcyber360_control(option)
    assert output == b_output.decode()
    mock_popen.assert_called_once_with([os.path.join(find_xcyber360_path(), "bin", "xcyber360-control"), option], 
                                               stdout=subprocess.PIPE)


def test_call_xcyber360_control_ko():
    """Validate that call_xcyber360_control exists with a code 1 when there's a system error."""
    with pytest.raises(SystemExit) as sys_exit:
        with patch('subprocess.Popen', side_effect=OSError):
            call_xcyber360_control('info')

    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 1


@pytest.mark.parametrize('field, xcyber360_info, expected', [
    ('XCYBER360_VERSION', 'XCYBER360_VERSION="v5.0.0"\nXCYBER360_REVISION="50000"\nXCYBER360_TYPE="server"\n', 'v5.0.0'),
    ('XCYBER360_REVISION', 'XCYBER360_VERSION="v5.0.0"\nXCYBER360_REVISION="50000"\nXCYBER360_TYPE="server"\n', '50000'),
    ('XCYBER360_TYPE', 'XCYBER360_VERSION="v5.0.0"\nXCYBER360_REVISION="50000"\nXCYBER360_TYPE="server"\n', 'server'),
    (None, 'XCYBER360_REVISION="50000"', 'XCYBER360_REVISION="50000"'),
    ('XCYBER360_TYPE', None, 'ERROR')
])
def test_get_xcyber360_info(field, xcyber360_info, expected):
    """Validate that get_xcyber360_info returns the correct information."""
    with patch('utils.call_xcyber360_control', return_value=xcyber360_info):
        actual = get_xcyber360_info(field)
        assert actual == expected


def test_get_xcyber360_version():
    """Validate that get_xcyber360_version returns the correct information."""
    xcyber360_info = 'XCYBER360_VERSION="v5.0.0"\nXCYBER360_REVISION="50000"\nXCYBER360_TYPE="server"\n'
    expected = 'v5.0.0'
    with patch('utils.call_xcyber360_control', return_value=xcyber360_info):
        version = get_xcyber360_version()

    assert version == expected
