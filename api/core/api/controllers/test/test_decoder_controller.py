

import sys
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest
from connexion.lifecycle import ConnexionResponse
from api.controllers.test.utils import CustomAffectedItems

with patch('xcyber360.common.xcyber360_uid'):
    with patch('xcyber360.common.xcyber360_gid'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators
        from api.controllers.decoder_controller import (delete_file,
                                                        get_decoders,
                                                        get_decoders_files,
                                                        get_decoders_parents,
                                                        get_file, put_file)
        from xcyber360 import decoder as decoder_framework
        from xcyber360.tests.util import RBAC_bypasser
        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser
        del sys.modules['xcyber360.rbac.orm']


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["decoder_controller"], indirect=True)
@patch('api.controllers.decoder_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.decoder_controller.remove_nones_to_dict')
@patch('api.controllers.decoder_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.decoder_controller.raise_if_exc', return_value=CustomAffectedItems())
async def test_get_decoders(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_request):
    """Verify 'get_decoders' endpoint is working as expected."""
    result = await get_decoders()
    f_kwargs = {'names': None,
                'offset': 0,
                'limit': None,
                'select': None,
                'sort_by': ['filename', 'position'],
                'sort_ascending': True,
                'search_text': None,
                'complementary_search': None,
                'q': None,
                'filename': None,
                'status': None,
                'relative_dirname': None,
                'distinct': False
                }
    mock_dapi.assert_called_once_with(f=decoder_framework.get_decoders,
                                      f_kwargs=mock_remove.return_value,
                                      request_type='local_any',
                                      is_async=False,
                                      wait_for_complete=False,
                                      logger=ANY,
                                      rbac_permissions=mock_request.context['token_info']['rbac_policies']
                                      )
    mock_exc.assert_called_once_with(mock_dfunc.return_value)
    mock_remove.assert_called_once_with(f_kwargs)
    assert isinstance(result, ConnexionResponse)


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["decoder_controller"], indirect=True)
@patch('api.controllers.decoder_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.decoder_controller.remove_nones_to_dict')
@patch('api.controllers.decoder_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.decoder_controller.raise_if_exc', return_value=CustomAffectedItems())
async def test_get_decoders_files(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_request):
    """Verify 'get_decoders_files' endpoint is working as expected."""
    result = await get_decoders_files()
    f_kwargs = {'offset': 0,
                'limit': None,
                'sort_by': ['filename'],
                'sort_ascending': True,
                'search_text': None,
                'complementary_search': None,
                'filename': None,
                'status': None,
                'relative_dirname': None,
                'q': None,
                'select': None,
                'distinct': False
                }
    mock_dapi.assert_called_once_with(f=decoder_framework.get_decoders_files,
                                      f_kwargs=mock_remove.return_value,
                                      request_type='local_any',
                                      is_async=False,
                                      wait_for_complete=False,
                                      logger=ANY,
                                      rbac_permissions=mock_request.context['token_info']['rbac_policies']
                                      )
    mock_exc.assert_called_once_with(mock_dfunc.return_value)
    mock_remove.assert_called_once_with(f_kwargs)
    assert isinstance(result, ConnexionResponse)


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["decoder_controller"], indirect=True)
@patch('api.controllers.decoder_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.decoder_controller.remove_nones_to_dict')
@patch('api.controllers.decoder_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.decoder_controller.raise_if_exc', return_value=CustomAffectedItems())
async def test_get_decoders_parents(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_request):
    """Verify 'get_decoders_parents' endpoint is working as expected."""
    result = await get_decoders_parents()
    f_kwargs = {'offset': 0,
                'limit': None,
                'select': None,
                'sort_by': ['filename', 'position'],
                'sort_ascending': True,
                'search_text': None,
                'complementary_search': None,
                'parents': True
                }
    mock_dapi.assert_called_once_with(f=decoder_framework.get_decoders,
                                      f_kwargs=mock_remove.return_value,
                                      request_type='local_any',
                                      is_async=False,
                                      wait_for_complete=False,
                                      logger=ANY,
                                      rbac_permissions=mock_request.context['token_info']['rbac_policies']
                                      )
    mock_exc.assert_called_once_with(mock_dfunc.return_value)
    mock_remove.assert_called_once_with(f_kwargs)
    assert isinstance(result, ConnexionResponse)


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["decoder_controller"], indirect=True)
@patch('api.controllers.decoder_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.decoder_controller.remove_nones_to_dict')
@patch('api.controllers.decoder_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.decoder_controller.raise_if_exc', return_value=CustomAffectedItems())
@pytest.mark.parametrize('mock_bool', [True, False])
async def test_get_file(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_bool, mock_request):
    """Verify 'get_file' endpoint is working as expected."""
    with patch('api.controllers.decoder_controller.isinstance', return_value=mock_bool) as mock_isinstance:
        result = await get_file()
        f_kwargs = {'filename': None,
                    'raw': False,
                    'relative_dirname': None
                    }
        mock_dapi.assert_called_once_with(f=decoder_framework.get_decoder_file,
                                          f_kwargs=mock_remove.return_value,
                                          request_type='local_master',
                                          is_async=False,
                                          wait_for_complete=False,
                                          logger=ANY,
                                          rbac_permissions=mock_request.context['token_info']['rbac_policies']
                                          )
        mock_exc.assert_called_once_with(mock_dfunc.return_value)
        mock_remove.assert_called_once_with(f_kwargs)
        if mock_isinstance.return_value:
            assert isinstance(result, ConnexionResponse)
        else:
            assert isinstance(result, ConnexionResponse)


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["decoder_controller"], indirect=True)
@patch('api.controllers.decoder_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.decoder_controller.remove_nones_to_dict')
@patch('api.controllers.decoder_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.decoder_controller.raise_if_exc', return_value=CustomAffectedItems())
async def test_put_file(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_request):
    """Verify 'put_file' endpoint is working as expected."""
    with patch('api.controllers.decoder_controller.Body.validate_content_type'):
        with patch('api.controllers.decoder_controller.Body.decode_body') as mock_dbody:
            result = await put_file(
                                    body={})
            f_kwargs = {'filename': None,
                        'relative_dirname': None,
                        'overwrite': False,
                        'content': mock_dbody.return_value
                        }
            mock_dapi.assert_called_once_with(f=decoder_framework.upload_decoder_file,
                                              f_kwargs=mock_remove.return_value,
                                              request_type='local_master',
                                              is_async=False,
                                              wait_for_complete=False,
                                              logger=ANY,
                                              rbac_permissions=mock_request.context['token_info']['rbac_policies']
                                              )
            mock_exc.assert_called_once_with(mock_dfunc.return_value)
            mock_remove.assert_called_once_with(f_kwargs)
            assert isinstance(result, ConnexionResponse)


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_request", ["decoder_controller"], indirect=True)
@patch('api.controllers.decoder_controller.DistributedAPI.distribute_function', return_value=AsyncMock())
@patch('api.controllers.decoder_controller.remove_nones_to_dict')
@patch('api.controllers.decoder_controller.DistributedAPI.__init__', return_value=None)
@patch('api.controllers.decoder_controller.raise_if_exc', return_value=CustomAffectedItems())
async def test_delete_file(mock_exc, mock_dapi, mock_remove, mock_dfunc, mock_request):
    """Verify 'delete_file' endpoint is working as expected."""
    result = await delete_file()
    f_kwargs = {'filename': None,
                'relative_dirname': None}
    
    mock_dapi.assert_called_once_with(f=decoder_framework.delete_decoder_file,
                                      f_kwargs=mock_remove.return_value,
                                      request_type='local_master',
                                      is_async=False,
                                      wait_for_complete=False,
                                      logger=ANY,
                                      rbac_permissions=mock_request.context['token_info']['rbac_policies']
                                      )
    mock_exc.assert_called_once_with(mock_dfunc.return_value)
    mock_remove.assert_called_once_with(f_kwargs)
    assert isinstance(result, ConnexionResponse)
