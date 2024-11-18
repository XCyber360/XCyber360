

import json
import sys
from unittest.mock import MagicMock, patch

import pytest

from xcyber360.core.exception import Xcyber360ClusterError
from api.models.order_model import Order

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators
        from xcyber360.tests.util import RBAC_bypasser

        del sys.modules['xcyber360.rbac.orm']
        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser

        from xcyber360.order import send_orders


@pytest.mark.parametrize('side_effect,message', [
    (None, 'All orders were published'),
    (Xcyber360ClusterError(3023), 'No orders were published'),
])
@patch('xcyber360.order.distribute_orders')
@patch('xcyber360.order.local_client.LocalClient')
async def test_send_orders(local_client_mock, distribute_orders_mock, side_effect, message):
    """Validate that the `send_orders` function is working as expected."""
    distribute_orders_mock.side_effect = side_effect
    orders = [Order().to_dict()]
    result = await send_orders(orders=orders)

    assert result.message == message
    assert result.total_affected_items == 0 if side_effect else len(orders)
