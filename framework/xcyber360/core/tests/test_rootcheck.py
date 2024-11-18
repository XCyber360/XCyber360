

import os
import sqlite3
from json import dumps
from unittest.mock import patch, ANY

import pytest

from api.util import remove_nones_to_dict
from xcyber360.core.common import DATE_FORMAT
from xcyber360.core.exception import Xcyber360Exception
from xcyber360.core.utils import get_date_from_timestamp

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        from xcyber360.core import rootcheck

test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'test_rootcheck')


class InitRootcheck:

    def __init__(self, data_path=test_data_path):
        """
        Sets up necessary test environment for agents:
            * One active agent.
            * One pending agent.
            * One never_connected agent.
            * One disconnected agent.

        :return: None
        """
        db_path = os.path.join(data_path, '001.db')
        remove_db(data_path)

        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self.cur = self.db.cursor()
        with open(os.path.join(data_path, 'schema_rootcheck_test.sql')) as f:
            self.cur.executescript(f.read())


def remove_db(data_path):
    db_path = os.path.join(data_path, '001.db')
    if os.path.isfile(db_path):
        os.remove(db_path)


test_data = InitRootcheck()


def send_msg_to_wdb(msg, raw=False):
    query = ' '.join(msg.split(' ')[3:])
    result = list(map(remove_nones_to_dict, map(dict, test_data.cur.execute(query).fetchall())))
    return ['ok', dumps(result)] if raw else result


@patch("xcyber360.core.rootcheck.Xcyber360DBBackend")
@patch("xcyber360.core.rootcheck.Xcyber360DBQuery.__init__")
@patch('xcyber360.core.agent.Agent.get_basic_information')
def test_Xcyber360DBQueryRootcheck_init(mock_info, mock_xcyber360DBQuery, mock_backend):
    """Test if Xcyber360DBQuery and Xcyber360DBBackend are called with expected parameters"""
    test = rootcheck.Xcyber360DBQueryRootcheck(agent_id='100', offset=1, limit=1, sort=None, search='test', select=['log'],
                                           query='test', count=True, get_data=True, distinct=False, filters=None,
                                           fields={})
    mock_backend.assert_called_with('100')
    mock_xcyber360DBQuery.assert_called_with(ANY, offset=1, limit=1, table='pm_event', sort=None, search='test',
                                         select=['log'], fields={}, default_sort_field='date_last',
                                         default_sort_order='DESC', filters={}, query='test', backend=ANY,
                                         min_select_fields=set(), count=True, get_data=True, distinct=False,
                                         date_fields={'date_last', 'date_first'})


@pytest.mark.parametrize('distinct', [
    True, False
])
@patch("xcyber360.core.rootcheck.Xcyber360DBBackend")
@patch('xcyber360.core.agent.Agent.get_basic_information')
def test_Xcyber360DBQueryRootcheck_default_query(mock_info, mock_backend, distinct):
    """Test if default query is changed according to distinct parameter

    Parameters
    ----------
    distinct : bool
        Whether to apply distinct to query
    """
    test = rootcheck.Xcyber360DBQueryRootcheck(agent_id='100', offset=1, limit=1, sort=None, search='test', select=['log'],
                                           query='test', count=True, get_data=True, distinct=distinct, filters=None,
                                           fields={})
    if distinct:
        assert test._default_query() == "SELECT DISTINCT {0} FROM "
    else:
        assert test._default_query() == "SELECT {0} FROM "


@patch("xcyber360.core.rootcheck.Xcyber360DBBackend")
@patch('xcyber360.core.agent.Agent.get_basic_information')
def test_Xcyber360DBQueryRootcheck_parse_filters(mock_info, mock_backend):
    """Test if expected query_filters are created after calling _parse_filters() method."""
    expected_query_filters = [{'value': 'all', 'field': 'status$0', 'operator': '=', 'separator': 'AND', 'level': 0},
                              {'value': None, 'field': 'pci_dss$0', 'operator': '=', 'separator': 'AND', 'level': 0},
                              {'value': None, 'field': 'cis$0', 'operator': '=', 'separator': '', 'level': 0}]

    test = rootcheck.Xcyber360DBQueryRootcheck(agent_id='100', offset=1, limit=1, sort=None, search='test', select=['log'],
                                           query='', count=True, get_data=True, distinct=False, fields={},
                                           filters={'status': 'all', 'pci_dss': None, 'cis': None})
    # Check it is empty before calling _parse_filters()
    assert test.query_filters == []
    test._parse_filters()
    assert test.query_filters == expected_query_filters


@pytest.mark.parametrize('status, expected_items', [
    ('outstanding', ['outstanding', '>']),
    ('solved', ['solved', '<=']),
    ('all', ['solved', 'outstanding', '<=', '>', 'UNION'])
])
@patch("xcyber360.core.rootcheck.Xcyber360DBBackend")
@patch('xcyber360.core.agent.Agent.get_basic_information')
def test_Xcyber360DBQueryRootcheck_filter_status(mock_info, mock_backend, status, expected_items):
    """Test if the query has the expected items after calling _filter_status() method

    Parameters
    ----------
    status : str
        Status to filter by
    expected_items : list
        Items which should be included in the query depending on the selected status
    """
    test = rootcheck.Xcyber360DBQueryRootcheck(agent_id='100', offset=1, limit=1, sort=None, search='test', select=['log'],
                                           query='', count=True, get_data=True, distinct=False, fields={},
                                           filters={'status': 'all', 'pci_dss': None, 'cis': None})

    test._filter_status({'value': status})
    assert all(item in test.query for item in expected_items)


@patch("xcyber360.core.rootcheck.Xcyber360DBBackend")
@patch('xcyber360.core.agent.Agent.get_basic_information')
def test_Xcyber360DBQueryRootcheck_filter_status_ko(mock_info, mock_backend):
    """Test if expected exception is raised when status does not exist"""
    test = rootcheck.Xcyber360DBQueryRootcheck(agent_id='100', offset=1, limit=1, sort=None, search='test', select=['log'],
                                           query='', count=True, get_data=True, distinct=False, fields={},
                                           filters={'status': 'all', 'pci_dss': None, 'cis': None})

    with pytest.raises(Xcyber360Exception, match=".* 1603 .*"):
        test._filter_status({'value': 'test'})


@patch("xcyber360.core.rootcheck.Xcyber360DBBackend")
@patch('xcyber360.core.agent.Agent.get_basic_information')
def test_Xcyber360DBQueryRootcheck_format_data_into_dictionary(mock_info, mock_backend):
    """Test if format_data_into_dictionary() returns expected element"""
    test = rootcheck.Xcyber360DBQueryRootcheck(agent_id='100', offset=1, limit=1, sort=None, search='test',
                                           select=['log', 'date_first', 'status', 'date_last', 'cis', 'pci_dss'],
                                           query='', count=True, get_data=True, distinct=False,
                                           fields=rootcheck.Xcyber360DBQueryRootcheck.fields,
                                           filters={'status': 'all', 'pci_dss': None, 'cis': None})
    test._add_select_to_query()
    test._data = [{'log': 'Testing', 'date_first': 1603645251, 'status': 'solved', 'date_last': 1603648851,
                   'cis': '2.3 Debian Linux', 'pci_dss': '4.1'}]
    result = test._format_data_into_dictionary()

    assert result['items'][0]['date_first'] == get_date_from_timestamp(1603645251).strftime(DATE_FORMAT) and \
           result['items'][0]['date_last'] == get_date_from_timestamp(1603648851).strftime(DATE_FORMAT)


@patch('xcyber360.core.agent.Agent.get_basic_information')
@patch('xcyber360.core.wdb.Xcyber360DBConnection._send', side_effect=send_msg_to_wdb)
@patch('socket.socket.connect')
def test_last_scan(mock_connect, mock_send, mock_info):
    """Check if last_scan function returns expected datetime according to the database"""
    result = rootcheck.last_scan('001')
    assert result == {'end': '2020-10-27T12:29:40Z', 'start': '2020-10-27T12:19:40Z'}


remove_db(test_data_path)


@pytest.mark.parametrize('agent', ['001', '002', '003'])
@patch('xcyber360.core.wdb.Xcyber360DBConnection')
def test_rootcheck_delete_agent(mock_db_conn, agent):
    """Test if proper parameters are being sent to the xcyber360db socket.

    Parameters
    ----------
    agent : str
        Agent whose information is being deleted from the db.
    mock_db_conn : Xcyber360DBConnection
        Object used to send the delete message to the xcyber360db socket.
    """
    rootcheck.rootcheck_delete_agent(agent, mock_db_conn)
    mock_db_conn.execute.assert_called_with(f"agent {agent} rootcheck delete", delete=True)