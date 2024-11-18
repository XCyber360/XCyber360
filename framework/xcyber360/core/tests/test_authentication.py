from unittest.mock import patch, call

import pytest

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        from xcyber360.core import authentication
        from xcyber360.core.exception import Xcyber360InternalError

@patch('builtins.open')
def test_get_keypair(mock_open):
    """Verify correct params when calling open method inside get_keypair."""
    with patch('xcyber360.core.authentication.keypair_exists', return_value=True):
        authentication.get_keypair()
        calls = [call(authentication._private_key_path, mode='r'),
                 call(authentication._public_key_path, mode='r')]
        mock_open.assert_has_calls(calls, any_order=True)


def test_get_keypair_ko():
    """Verify an exception is raised when there's no key pair."""
    with patch('xcyber360.core.authentication.keypair_exists', return_value=False):
        with pytest.raises(Xcyber360InternalError, match='.*6003*.'):
            authentication.get_keypair()


@patch('os.chmod')
@patch('os.chown')
@patch('builtins.open')
def test_generate_keypair(mock_open, mock_chown, mock_chmod):
    """Verify correct params when calling open method inside generate_keypair."""
    result = authentication.generate_keypair()
    assert isinstance(result[0], str)
    assert isinstance(result[1], str)

    mock_open.assert_has_calls([
        call(authentication._private_key_path, mode='w'),
        call(authentication._public_key_path, mode='w')
    ], any_order=True)
    mock_chown.assert_has_calls([
        call(authentication._private_key_path, authentication.xcyber360_uid(), authentication.xcyber360_gid()),
        call(authentication._public_key_path, authentication.xcyber360_uid(), authentication.xcyber360_gid())
    ])
    mock_chmod.assert_has_calls([
        call(authentication._private_key_path, 0o640),
        call(authentication._public_key_path, 0o640)
    ])


@pytest.mark.parametrize("exists", [True, False])
def test_keypair_exists(exists):
    """Verify that `keypair_exists` works as expected."""
    with patch('os.path.exists', return_value=exists):
        assert authentication.keypair_exists() == exists
