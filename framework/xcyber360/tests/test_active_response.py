#!/usr/bin/env python


import os
import sys
from unittest.mock import patch, MagicMock

import pytest

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators
        from xcyber360.tests.util import RBAC_bypasser

        del sys.modules['xcyber360.rbac.orm']
        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser

        from xcyber360.active_response import run_command
        from xcyber360.core.tests.test_active_response import agent_config, agent_info_exception_and_version

test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'etc', 'shared', 'ar.conf')
full_agent_list = ['001', '002', '003', '004', '005', '006', '007', '008']


# Tests

@pytest.mark.parametrize('message_exception, send_exception, agent_id, command, arguments, alert, version', [
    (1701, None, ['999'], 'restart-xcyber3600', [], None, 'Xcyber360 v4.0.0'),
    (1650, None, ['001'], None, [], None, 'Xcyber360 v4.0.0'),
    (1652, None, ['002'], 'random', [], None, 'Xcyber360 v4.0.0'),
    (None, 1707, ['003'], 'restart-xcyber3600', [], None, None),
    (None, 1750, ['004'], 'restart-xcyber3600', [], None, 'Xcyber360 v4.0.0'),
    (None, None, ['005'], 'restart-xcyber3600', [], None, 'Xcyber360 v4.0.0'),
    (None, None, ['006'], '!custom-ar', [], None, 'Xcyber360 v4.0.0'),
    (None, None, ['007'], 'restart-xcyber3600', ["arg1", "arg2"], None, 'Xcyber360 v4.0.0'),
    (None, None, ['001', '002', '003', '004', '005', '006'], 'restart-xcyber3600', [], None, 'Xcyber360 v4.0.0'),
    (None, None, ['001'], 'restart-xcyber3600', ["arg1", "arg2"], None, 'Xcyber360 v4.2.0'),
    (None, None, ['002'], 'restart-xcyber3600', [], None, 'Xcyber360 v4.2.1'),
])
@patch("xcyber360.core.xcyber360_queue.Xcyber360Queue._connect")
@patch("xcyber360.syscheck.Xcyber360Queue._send", return_value='1')
@patch("xcyber360.core.xcyber360_queue.Xcyber360Queue.close")
@patch('xcyber360.core.common.AR_CONF', new=test_data_path)
@patch('xcyber360.active_response.get_agents_info', return_value=full_agent_list)
@pytest.mark.skip('Remove tested function or update it to use the indexer.')
def test_run_command(mock_get_agents_info, mock_close, mock_send, mock_conn, message_exception,
                     send_exception, agent_id, command, arguments, alert, version):
    """Verify the proper operation of active_response module.

    Parameters
    ----------
    message_exception : int
        Exception code expected when calling create_message.
    send_exception : int
        Exception code expected when calling send_command.
    agent_id : list
        Agents on which to execute the Active response command.
    command : string
        Command to be executed on the agent.
    arguments : list
        Arguments of the command.
    custom : boolean
        True if command is a script.
    version : list
        List with the agent version to test whether the message sent was the correct one or not.
    """
    with patch('xcyber360.core.agent.Agent.get_basic_information',
               return_value=agent_info_exception_and_version(send_exception, version)):
        with patch('xcyber360.core.agent.Agent.get_config', return_value=agent_config(send_exception)):
            if message_exception:
                ret = run_command(agent_list=agent_id, command=command, arguments=arguments, alert=alert)
                assert ret.render()['data']['failed_items'][0]['error']['code'] == message_exception
            else:
                ret = run_command(agent_list=agent_id, command=command, arguments=arguments, alert=alert)
                if send_exception:
                    assert ret.render()['message'] == 'AR command was not sent to any agent'
                    assert ret.render()['data']['failed_items'][0]['error']['code'] == send_exception
                else:
                    assert ret.render()['message'] == 'AR command was sent to all agents'
