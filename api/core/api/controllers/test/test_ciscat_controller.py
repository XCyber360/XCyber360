

import sys
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest
from connexion.lifecycle import ConnexionResponse
from api.controllers.test.utils import CustomAffectedItems

with patch('xcyber360.common.xcyber360_uid'):
    with patch('xcyber360.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators
        from api.controllers.ciscat_controller import get_agents_ciscat_results
        from xcyber360 import ciscat
        from xcyber360.tests.util import RBAC_bypasser
        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser
        del sys.modules['xcyber360.rbac.orm']


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["ciscat_controller"], indirect=True)
@patch('api.controllers.ciscat_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.ciscat_controller.remove_nones_to_dict')
@patch('api.controllers.ciscat_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.ciscat_controller.raise_if_exc', return_value=CustomAffectedItems())
async def test_get_agents_ciscat_results(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_request):
    """Verify 'get_agents_ciscat_results' endpoint is working as expected."""
    result = await get_agents_ciscat_results(
                                             agent_id='001')
    f_kwargs = {
        'agent_list': ['001'],
        'offset': 0,
        'limit': None,
        'sort': None,
        'search': None,
        'select': None,
        'filters': {
            'benchmark': None,
            'profile': None,
            'pass': mock_request.query_params.get('pass', None),
            'fail': None,
            'error': None,
            'notchecked': None,
            'unknown': None,
            'score': None
            },
        'q': None
        }
    mock_dapi.assert_called_once_with(f=ciscat.get_ciscat_results,
                                      f_kwargs=mock_remove.return_value,
                                      request_type='distributed_master',
                                      is_async=False,
                                      wait_for_complete=False,
                                      logger=ANY,
                                      rbac_permissions=mock_request.context['token_info']['rbac_policies']
                                      )
    mock_exc.assert_called_once_with(mock_dfunc.return_value)
    mock_remove.assert_called_once_with(f_kwargs)
    assert isinstance(result, ConnexionResponse)
