#!/usr/bin/env python


from unittest.mock import patch

import pytest

from xcyber360.tests.util import InitWDBSocketMock

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        from xcyber360.core.syscollector import *
        from xcyber360.core import common


# Tests

@pytest.mark.parametrize("os_name", [
    'Windows',
    'Linux'
])
@patch('xcyber360.core.agent.Agent.get_basic_information')
def test_get_valid_fields(mock_info, os_name):
    """Check get_valid_fields returns expected type and content

    Parameters
    ----------
    os_name : str
        Request information of this OS.
    """
    with patch('xcyber360.core.agent.Agent.get_agent_os_name', return_value=os_name):
        response = get_valid_fields(Type.OS, '0')
        assert isinstance(response, tuple) and isinstance(response[1], dict), 'Data type not expected'
        assert 'sys_osinfo' in response[0], f'"sys_osinfo" not contained in {response}'


@patch('xcyber360.core.utils.path.exists', return_value=True)
@patch('xcyber360.core.agent.Agent.get_basic_information', return_value=None)
@patch('xcyber360.core.agent.Agent.get_agent_os_name', return_value='Linux')
def test_Xcyber360DBQuerySyscollector(mock_basic_info, mock_agents_info, mock_exists):
    """Verify that the method connects correctly to the database and returns the correct type."""
    with patch('xcyber360.core.utils.Xcyber360DBConnection') as mock_wdb:
        mock_wdb.return_value = InitWDBSocketMock(sql_schema_file='schema_syscollector_000.sql')
        db_query = Xcyber360DBQuerySyscollector(agent_id='000', offset=0, limit=common.DATABASE_LIMIT, select=None,
                                            search=None, sort=None, filters=None,
                                            fields=get_valid_fields(Type.OS, '000')[1], table='sys_osinfo',
                                            array=True, nested=True, query='')
        db_query._filter_status(None)
        data = db_query.run()
        assert isinstance(db_query, Xcyber360DBQuerySyscollector) and isinstance(data, dict)
