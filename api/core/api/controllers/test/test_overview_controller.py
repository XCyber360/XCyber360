

import sys
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest
from connexion.lifecycle import ConnexionResponse
from api.controllers.test.utils import CustomAffectedItems

with patch('xcyber360.common.xcyber360_uid'):
    with patch('xcyber360.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators
        from api.controllers.overview_controller import get_overview_agents
        from xcyber360 import agent
        from xcyber360.tests.util import RBAC_bypasser
        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser
        del sys.modules['xcyber360.rbac.orm']


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["overview_controller"], indirect=True)
@patch('api.controllers.overview_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.overview_controller.remove_nones_to_dict')
@patch('api.controllers.overview_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.overview_controller.raise_if_exc', return_value=CustomAffectedItems())
async def test_get_overview_agents(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_request):
    """Verify 'get_overview_agents' endpoint is working as expected."""
    result = await get_overview_agents()
    mock_dapi.assert_called_once_with(f=agent.get_full_overview,
                                      f_kwargs=mock_remove.return_value,
                                      request_type='local_master',
                                      is_async=False,
                                      wait_for_complete=False,
                                      logger=ANY,
                                      rbac_permissions=mock_request.context['token_info']['rbac_policies']
                                      )
    mock_exc.assert_called_once_with(mock_dfunc.return_value)
    mock_remove.assert_called_once_with({})
    assert isinstance(result, ConnexionResponse)
