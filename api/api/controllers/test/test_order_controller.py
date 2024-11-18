

import sys
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest
from connexion.lifecycle import ConnexionResponse

from api.controllers.test.utils import CustomAffectedItems

with patch('xcyber360.common.xcyber360_uid'):
    with patch('xcyber360.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators
        from xcyber360.order import send_orders
        from xcyber360.tests.util import RBAC_bypasser

        from api.controllers.order_controller import post_orders

        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser
        del sys.modules['xcyber360.rbac.orm']


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["order_controller"], indirect=True)
@patch('api.configuration.api_conf')
@patch('api.controllers.order_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.order_controller.remove_nones_to_dict')
@patch('api.controllers.order_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.order_controller.raise_if_exc', return_value=CustomAffectedItems())
async def test_post_orders(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_exp, mock_request):
    """Verify 'post_orders' endpoint is working as expected."""
    with patch('api.controllers.order_controller.Body.validate_content_type'):
        with patch(
            'api.controllers.order_controller.Orders.get_kwargs', return_value=AsyncMock()
        ) as mock_getkwargs:

            result = await post_orders()
            mock_dapi.assert_called_once_with(
                f=send_orders,
                f_kwargs=mock_remove.return_value,
                request_type='local_any',
                is_async=True,
                wait_for_complete=False,
                logger=ANY,
                rbac_permissions=mock_request.context['token_info']['rbac_policies']
            )
            mock_exc.assert_called_once_with(mock_dfunc.return_value)
            mock_remove.assert_called_once_with(mock_getkwargs.return_value)
            assert isinstance(result, ConnexionResponse)
