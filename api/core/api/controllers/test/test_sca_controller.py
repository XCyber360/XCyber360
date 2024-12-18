

import sys
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest
from connexion.lifecycle import ConnexionResponse
from api.controllers.test.utils import CustomAffectedItems

with patch('xcyber360.common.xcyber360_uid'):
    with patch('xcyber360.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators
        from api.controllers.sca_controller import (get_sca_agent,
                                                    get_sca_checks)
        from xcyber360 import sca
        from xcyber360.core.common import DATABASE_LIMIT
        from xcyber360.tests.util import RBAC_bypasser
        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser
        del sys.modules['xcyber360.rbac.orm']


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["sca_controller"], indirect=True)
@patch('api.controllers.sca_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.sca_controller.remove_nones_to_dict')
@patch('api.controllers.sca_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.sca_controller.raise_if_exc', return_value=CustomAffectedItems())
async def test_get_sca_agent(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_request):
    """Verify 'get_sca_agent' endpoint is working as expected."""
    result = await get_sca_agent()
    filters = {'name': None,
               'description': None,
               'references': None
               }
    f_kwargs = {'agent_list': [None],
                'offset': 0,
                'limit': DATABASE_LIMIT,
                'sort': None,
                'search': None,
                'select': None,
                'q': None,
                'distinct': False,
                'filters': filters
                }
    mock_dapi.assert_called_once_with(f=sca.get_sca_list,
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


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["sca_controller"], indirect=True)
@patch('api.controllers.sca_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.sca_controller.remove_nones_to_dict')
@patch('api.controllers.sca_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.sca_controller.raise_if_exc', return_value=CustomAffectedItems())
async def test_get_sca_checks(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_request):
    """Verify 'get_sca_checks' endpoint is working as expected."""
    result = await get_sca_checks()
    filters = {'title': None,
               'description': None,
               'rationale': None,
               'remediation': None,
               'command': None,
               'reason': None,
               'file': None,
               'process': None,
               'directory': None,
               'registry': None,
               'references': None,
               'result': None,
               'condition': None
               }
    f_kwargs = {'policy_id': None,
                'agent_list': [None],
                'offset': 0,
                'limit': DATABASE_LIMIT,
                'sort': None,
                'search': None,
                'select': None,
                'q': None,
                'distinct': False,
                'filters': filters
                }
    mock_dapi.assert_called_once_with(f=sca.get_sca_checks,
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
