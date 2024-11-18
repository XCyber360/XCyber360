

import os
import sys
from unittest.mock import MagicMock, patch
from xcyber360.core.exception import Xcyber360Error


import pytest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators
        from xcyber360.tests.util import RBAC_bypasser

        del sys.modules['xcyber360.rbac.orm']
        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser

        from xcyber360.event import MSG_HEADER, send_event_to_analysisd


@pytest.mark.parametrize('events,side_effects,message', [
    (['{"foo": 1}'], (None,), 'All events were forwarded to analisysd'),
    (['{"foo": 1}', '{"bar": 2}'], (None, None), 'All events were forwarded to analisysd'),
    (['{"foo": 1}', '{"bar": 2}'], (Xcyber360Error(1014), None), 'Some events were forwarded to analisysd'),
    (['{"foo": 1}', '{"bar": 2}'], (Xcyber360Error(1014), Xcyber360Error(1014)), 'No events were forwarded to analisysd'),
])
@patch('xcyber360.event.Xcyber360AnalysisdQueue.send_msg')
@patch('socket.socket.connect')
def test_send_event_to_analysisd(socket_mock, send_msg_mock, events, side_effects, message):
    send_msg_mock.side_effect = side_effects
    ret_val = send_event_to_analysisd(events=events)

    assert send_msg_mock.call_count == len(events)
    for i, event in enumerate(events):
        assert send_msg_mock.call_args_list[i].kwargs['msg_header'] == MSG_HEADER
        assert send_msg_mock.call_args_list[i].kwargs['msg'] == event

    assert ret_val.affected_items == [events[i] for i, v in enumerate(side_effects) if v is None]
    assert ret_val.message == message
