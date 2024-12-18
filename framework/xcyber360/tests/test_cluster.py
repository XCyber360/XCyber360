

import sys
from unittest.mock import MagicMock, patch

import pytest

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        with patch('xcyber360.core.utils.load_xcyber360_xml'):
            sys.modules['xcyber360.rbac.orm'] = MagicMock()
            import xcyber360.rbac.decorators

            del sys.modules['xcyber360.rbac.orm']

            from xcyber360.tests.util import RBAC_bypasser

            xcyber360.rbac.decorators.expose_resources = RBAC_bypasser
            from xcyber360 import cluster
            from xcyber360.core import common
            from xcyber360.core.exception import Xcyber360Error, Xcyber360ResourceNotFound
            from xcyber360.core.cluster.local_client import LocalClient
            from xcyber360.core.results import Xcyber360Result

default_config = {'disabled': True, 'node_type': 'master', 'name': 'xcyber360', 'node_name': 'node01',
                  'key': '', 'port': 1516, 'bind_addr': 'localhost', 'nodes': ['127.0.0.1'], 'hidden': 'no'}


@patch('xcyber360.cluster.read_config', return_value=default_config)
async def test_read_config_wrapper(mock_read_config):
    """Verify that the read_config_wrapper returns the default configuration."""
    result = await cluster.read_config_wrapper()
    assert result.affected_items == [default_config]


@patch('xcyber360.cluster.read_config', side_effect=Xcyber360Error(1001))
async def test_read_config_wrapper_exception(mock_read_config):
    """Verify the exceptions raised in read_config_wrapper."""
    result = await cluster.read_config_wrapper()
    assert list(result.failed_items.keys())[0] == Xcyber360Error(1001)


@patch('xcyber360.cluster.read_config', return_value=default_config)
async def test_node_wrapper(mock_read_config):
    """Verify that the node_wrapper returns the default node information."""
    result = await cluster.get_node_wrapper()
    assert result.affected_items == [{'node': default_config["node_name"],
                                      'type': default_config["node_type"]}]


@patch('xcyber360.cluster.get_node', side_effect=Xcyber360Error(1001))
async def test_node_wrapper_exception(mock_get_node):
    """Verify the exceptions raised in get_node_wrapper."""
    result = await cluster.get_node_wrapper()
    assert list(result.failed_items.keys())[0] == Xcyber360Error(1001)


async def test_get_status_json():
    """Verify that get_status_json returns the default status information."""
    result = await cluster.get_status_json()
    expected = Xcyber360Result({'data': {"running": "no"}})
    assert result == expected


@pytest.mark.asyncio
@patch('xcyber360.core.cluster.utils.get_cluster_items')
@patch('xcyber360.core.cluster.local_client.LocalClient.start', side_effect=None)
async def test_get_health_nodes(mock_unix_connection, get_cluster_items_mock):
    """Verify that get_health_nodes returns the health of all nodes."""

    async def async_mock(lc=None, filter_node=None):
        return {'nodes': {'manager': {'info': {'name': 'master'}}}}

    local_client = LocalClient()
    with patch('xcyber360.cluster.get_health', side_effect=async_mock):
        result = await cluster.get_health_nodes(lc=local_client)
    expected = await async_mock()

    assert result.affected_items == [expected['nodes']['manager']]


@pytest.mark.asyncio
@patch('xcyber360.core.cluster.utils.get_cluster_items')
async def test_get_nodes_info(get_cluster_items):
    """Verify that get_nodes_info returns the information of all nodes."""

    async def valid_node(lc=None, filter_node=None):
        return {'items': ['master', 'worker1'], 'totalItems': 2}

    local_client = LocalClient()
    common.cluster_nodes.set(['master', 'worker1', 'worker2'])
    with patch('xcyber360.cluster.get_nodes', side_effect=valid_node):
        result = await cluster.get_nodes_info(lc=local_client, filter_node=['master', 'worker1', 'noexists'])
    expected = await valid_node()

    assert result.affected_items == expected['items']
    assert result.total_affected_items == expected['totalItems']
    assert result.failed_items[Xcyber360ResourceNotFound(1730)] == {'noexists'}
    assert result.total_failed_items == 1


@pytest.mark.parametrize("ruleset_integrity", [
    True,
    False
])
@patch("xcyber360.cluster.node_id", new="testing_node")
@pytest.mark.asyncio
@pytest.mark.skip('This modile its deprecated.')
async def test_get_ruleset_sync_status(ruleset_integrity):
    """Verify that `get_ruleset_sync_status` function correctly returns node ruleset synchronization status."""
    master_md5 = {'key1': 'value1'}
    with patch("xcyber360.cluster.get_node_ruleset_integrity",
               return_value=master_md5 if ruleset_integrity else {}) as ruleset_integrity_mock:
        result = await cluster.get_ruleset_sync_status(master_md5=master_md5)
        assert result.total_affected_items == 1
        assert result.total_failed_items == 0
        assert result.affected_items[0]['name'] == "testing_node"
        assert result.affected_items[0]['synced'] is ruleset_integrity


@patch("xcyber360.cluster.node_id", new="testing_node")
@pytest.mark.asyncio
@pytest.mark.skip('This modile its deprecated.')
async def test_get_ruleset_sync_status_ko():
    """Verify proper exceptions behavior with `get_ruleset_sync_status`."""
    exc = Xcyber360Error(1000)
    with patch("xcyber360.cluster.get_node_ruleset_integrity", side_effect=exc):
        result = await cluster.get_ruleset_sync_status(master_md5={})
        assert result.total_affected_items == 0
        assert result.total_failed_items == 1
        assert result.failed_items[exc] == {"testing_node"}
