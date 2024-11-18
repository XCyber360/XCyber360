

from datetime import datetime
from json import loads
from unittest.mock import patch, ANY

import pytest

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        from xcyber360.core import syscheck
        from xcyber360.core.utils import get_date_from_timestamp


@pytest.mark.parametrize('agent', ['002', '080'])
@patch("xcyber360.core.syscheck.Xcyber360DBBackend")
@patch("xcyber360.core.syscheck.Xcyber360DBQuery.__init__")
def test_xcyber360_db_query_syscheck__init__(mock_wdbquery, mock_backend, agent):
    """Test if Xcyber360DBQuery and Xcyber360DBBackend are called with the expected parameters.

    Parameters
    ----------
    agent: str
        The agent to test.
    """
    syscheck.Xcyber360DBQuerySyscheck(agent)
    mock_backend.assert_called_with(agent)
    mock_wdbquery.assert_called_with(backend=ANY, default_sort_field='mtime', min_select_fields=set(), count=True,
                                     get_data=True, date_fields={'start', 'end', 'mtime', 'date'})


@pytest.mark.parametrize('data, is_json', [
    ({'end': 1603648351, 'start': 1603645251, 'module': 'api', 'date': 1627893702, 'mtime': 1627893600,
     'perm': 'rwxr-xr-x'},
     False),
    ({'end': 1603648351, 'start': 1603645251, 'module': 'api', 'date': 1627893702, 'mtime': 1627893600,
     'perm': '{"S-1-5-18": {"name": "SYSTEM", "allowed": ["delete", "read_control", "write_dac", "write_owner", '
             '"read_data", "write_data", "append_data", "read_ea", "write_ea", "execute"]}}'},
     True)
])
@patch("xcyber360.core.syscheck.Xcyber360DBBackend")
def test_xcyber360_db_syscheck_format_data_into_dictionary(mock_backend, data, is_json):
    """Test if _format_data_into_dictionary() returns the expected element."""
    test = syscheck.Xcyber360DBQuerySyscheck('002', offset=0, limit=1000, sort=None, search='test',
                                         select=['end', 'start', 'module', 'date', 'mtime', 'perm'],
                                         filters={}, table='pm_event', query='',
                                         fields={'end': 'end_scan', 'start': 'start_scan', 'module': 'module',
                                                 'date': 'date', 'mtime': 'mtime', 'perm': 'perm'})
    test._add_select_to_query()
    test._data = [data]
    result = test._format_data_into_dictionary()

    assert result['items'][0]['end'] == get_date_from_timestamp(data['end'])
    assert result['items'][0]['start'] == get_date_from_timestamp(data['start'])
    assert result['items'][0]['module'] == data['module']
    assert result['items'][0]['date'] == get_date_from_timestamp(data['date'])
    assert result['items'][0]['mtime'] == get_date_from_timestamp(data['mtime'])
    if is_json:
        assert isinstance(result['items'][0]['perm'], dict)
        assert result['items'][0]['perm'] == loads(data['perm'])
    else:
        assert isinstance(result['items'][0]['perm'], str)
        assert result['items'][0]['perm'] == data['perm']


@pytest.mark.parametrize('agent', ['001', '002', '003'])
@patch('xcyber360.core.wdb.Xcyber360DBConnection')
def test_syscheck_delete_agent(mock_db_conn, agent):
    """Test if proper parameters are being sent to the wdb socket.

    Parameters
    ----------
    agent : str
        Agent whose information is being deleted from the db.
    mock_db_conn : Xcyber360DBConnection
        Object used to send the delete message to the xcyber360db socket.
    """
    syscheck.syscheck_delete_agent(agent, mock_db_conn)
    mock_db_conn.execute.assert_any_call(f"agent {agent} sql delete from fim_entry", delete=True)
