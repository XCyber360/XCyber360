

from unittest.mock import MagicMock, patch
import pytest

from connexion.testing import TestContext


@pytest.fixture
def mock_request(request):
    """fixture to wrap functions with request."""
    controller_name = request.param
    operation = MagicMock(name="operation")
    operation.method = "post"
    with TestContext(operation=operation):
        with patch(f'api.controllers.{controller_name}.request') as m_req:
            m_req.query_params.get = lambda key, default: None
            m_req.context = {'token_info': {'rbac_policies': {}}}
            yield m_req
