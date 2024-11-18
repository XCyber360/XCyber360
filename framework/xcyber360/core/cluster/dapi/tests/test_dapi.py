

import json
import logging
import os
import sys
from asyncio import TimeoutError
from unittest.mock import call, MagicMock, patch, AsyncMock

import pytest
from connexion import ProblemException
from sqlalchemy.exc import OperationalError
from sqlite3 import OperationalError as SQLiteOperationalError, DatabaseError, Error

from xcyber360.core import common

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../../../../api'))

with patch('xcyber360.common.xcyber360_uid'):
    with patch('xcyber360.common.xcyber360_gid'):
        with patch('xcyber360.core.utils.load_xcyber360_xml'):
            sys.modules['xcyber360.rbac.orm'] = MagicMock()
            import xcyber360.rbac.decorators

            del sys.modules['xcyber360.rbac.orm']

            from xcyber360.tests.util import RBAC_bypasser

            xcyber360.rbac.decorators.expose_resources = RBAC_bypasser
            from xcyber360.core.cluster.dapi.dapi import DistributedAPI, APIRequestQueue
            from xcyber360.core.manager import get_manager_status
            from xcyber360.core.results import Xcyber360Result, AffectedItemsXcyber360Result
            from xcyber360 import agent, cluster, ciscat, manager, Xcyber360Error, Xcyber360InternalError
            from xcyber360.core.exception import Xcyber360ClusterError
            from api.util import raise_if_exc
            from xcyber360.core.cluster import local_client

logger = logging.getLogger('xcyber360')

DEFAULT_REQUEST_TIMEOUT = 10


@pytest.fixture(scope='module', autouse=True)
def path_get_cluset_items():
    with patch('xcyber360.core.cluster.utils.get_cluster_items'):
        yield


async def raise_if_exc_routine(dapi_kwargs, expected_error=None):
    dapi = DistributedAPI(**dapi_kwargs)
    try:
        raise_if_exc(await dapi.distribute_function())
        if expected_error:
            assert False, f'Expected exception not generated: {expected_error}'
    except ProblemException as e:
        if expected_error:
            assert e.ext['code'] == expected_error
        else:
            assert False, f'Unexpected exception: {e.ext}'


class TestingLoggerParent:
    """Class used to create the parent attribute of TestingLogger objects."""
    __test__ = False

    def __init__(self):
        self.handlers = []


class TestingLogger:
    """Class used to create custom Logger objects for testing purposes."""
    __test__ = False

    def __init__(self, logger_name):
        self.name = logger_name
        self.handlers = []
        self.parent = TestingLoggerParent()

    def error(self, message):
        pass

    def debug(self, message):
        pass

    def debug2(self, message):
        pass


@pytest.mark.parametrize('kwargs', [
    {'f_kwargs': {'select': ['id']}, 'rbac_permissions': {'mode': 'black'}, 'nodes': ['worker1'],
     'basic_services': ('xcyber360-clusterd',), 'request_type': 'local_master'},
    {'request_type': 'local_master'},
    {'api_timeout': 15},
    {'api_timeout': 5}
])
def test_DistributedAPI(kwargs):
    """Test constructor from DistributedAPI class.

    Parameters
    ----------
    kwargs : dict
        Dict with some kwargs to pass when instancing the class.
    """
    dapi = DistributedAPI(f=agent.get_agents_summary_status, logger=logger, **kwargs)
    assert isinstance(dapi, DistributedAPI)
    assert dapi.api_request_timeout == max(kwargs.get('api_timeout', 0), DEFAULT_REQUEST_TIMEOUT)


def test_DistributedAPI_debug_log():
    """Check that error messages are correctly sent to the logger in the DistributedAPI class."""
    logger_ = TestingLogger(logger_name="xcyber360-api")
    message = "Testing debug2"
    with patch.object(logger_, "debug2") as debug2_mock:
        dapi = DistributedAPI(f=agent.get_agents_summary_status, logger=logger_)
        dapi.debug_log(message)
        debug2_mock.assert_called_once_with(message)

    logger_ = TestingLogger(logger_name="xcyber360")
    message = "Testing debug"
    with patch.object(logger_, "debug") as debug_mock:
        dapi = DistributedAPI(f=agent.get_agents_summary_status, logger=logger_)
        dapi.debug_log(message)
        debug_mock.assert_called_once_with(message)


@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.execute_local_request',
       new=AsyncMock(return_value=Xcyber360Result({'result': 'local'})))
@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.forward_request',
       new=AsyncMock(return_value=Xcyber360Result({'result': 'forward'})))
@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.execute_remote_request',
       new=AsyncMock(return_value=Xcyber360Result({'result': 'remote'})))
@pytest.mark.parametrize('api_request, request_type, node, expected, f_kwargs', [
    (agent.get_agents_summary_status, 'local_master', 'master', 'local', None),
    (agent.restart_agents, 'distributed_master', 'master', 'forward', None),
    (cluster.get_node_wrapper, 'local_any', 'worker', 'local', 'token_nbf_time'),
    (ciscat.get_ciscat_results, 'distributed_master', 'worker', 'remote', None),
])
async def test_DistributedAPI_distribute_function(api_request, request_type, node, expected, f_kwargs):
    """Test distribute_function functionality with different test cases.

    Parameters
    ----------
    api_request : callable
        Function to be executed.
    request_type : str
        Request type (local_master, distributed_master, local_any).
    node : str
        Node type (Master and Workers).
    expected : str
        Expected result.
    """
    with patch('xcyber360.core.cluster.cluster.get_node', return_value={'type': node}):
        dapi = DistributedAPI(f=api_request, logger=logger, request_type=request_type, f_kwargs=f_kwargs)
        data = raise_if_exc(await dapi.distribute_function())
        assert data.render()['result'] == expected


@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.execute_local_request',
       new=AsyncMock(return_value=Xcyber360Result({'result': 'local'})))
@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.get_solver_node',
       new=AsyncMock(return_value=Xcyber360Result({'unknown': ['001', '002']})))
@pytest.mark.parametrize('api_request, request_type, node, expected', [
    (agent.restart_agents, 'distributed_master', 'master', 'local')
])
async def test_DistributedAPI_distribute_function_mock_solver(api_request, request_type, node, expected):
    """Test distribute_function functionality with unknown node.

    Parameters
    ----------
    api_request : callable
        Function to be executed
    request_type : str
        Request type (local_master, distributed_master, local_any)
    node : str
        Node type (Master and Workers)
    expected : str
        Expected result
    """
    with patch('xcyber360.core.cluster.cluster.get_node', return_value={'type': node, 'node': 'master'}):
        dapi = DistributedAPI(f=api_request, logger=logger, request_type=request_type, from_cluster=False)
        data = raise_if_exc(await dapi.distribute_function())
        assert data.render()['result'] == expected


async def test_DistributedAPI_distribute_function_exception():
    """Test distribute_function when an exception is raised."""

    class NodeWrapper:
        def __init__(self):
            self.affected_items = []
            self.failed_items = {Exception("test_get_error_info"): "abc"}

    dapi_kwargs = {'f': manager.restart, 'logger': logger}
    await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=1017)

    logger_ = logging.getLogger("xcyber360")
    with patch("xcyber360.core.cluster.dapi.dapi.get_node_wrapper", side_effect=Xcyber360Error(4000)):
        dapi = DistributedAPI(f=agent.get_agents_summary_status, logger=logger_)
        get_error_result = await dapi.get_error_info(Exception("testing"))
        assert 'unknown-node' in get_error_result
        assert get_error_result['unknown-node']['error'] == 'Xcyber360 Internal Error. See log for more detail'

    with patch("xcyber360.core.cluster.dapi.dapi.get_node_wrapper", side_effect=Xcyber360Error(4001)):
        dapi = DistributedAPI(f=agent.get_agents_summary_status, logger=logger_)
        with pytest.raises(Xcyber360Error, match='.* 4001 .*'):
            await dapi.get_error_info(Exception("testing"))

    with patch("xcyber360.core.cluster.dapi.dapi.get_node_wrapper", new=AsyncMock(return_value=NodeWrapper())):
        dapi = DistributedAPI(f=agent.get_agents_summary_status, logger=logger_)
        with pytest.raises(Exception, match='.*test_get_error_info.*'):
            await dapi.get_error_info(Exception("testing"))


@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.execute_local_request',
       new=AsyncMock(return_value='{wrong\': json}'))
async def test_DistributedAPI_invalid_json():
    """Check the behaviour of DistributedAPI when an invalid JSON is received."""
    dapi_kwargs = {'f': agent.get_agents_summary_status, 'logger': logger}
    assert await raise_if_exc_routine(dapi_kwargs=dapi_kwargs) is None


async def test_DistributedAPI_local_request_errors():
    """Check the behaviour when the local_request function raised an error."""
    with patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.execute_local_request',
               new=AsyncMock(side_effect=Xcyber360InternalError(1001))):
        dapi_kwargs = {'f': agent.get_agents_summary_status, 'logger': logger}
        await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=1001)

        dapi_kwargs['debug'] = True
        dapi = DistributedAPI(f=agent.get_agents_summary_status, logger=logger, debug=True)
        try:
            raise_if_exc(await dapi.distribute_function())
        except Xcyber360InternalError as e:
            assert e.code == 1001

    with patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.execute_local_request',
               new=AsyncMock(side_effect=KeyError('Testing'))):
        dapi_kwargs = {'f': agent.get_agents_summary_status, 'logger': logger}
        await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=1000)  # Specify KeyError

        dapi = DistributedAPI(f=agent.get_agents_summary_status, logger=logger, debug=True)
        try:
            raise_if_exc(await dapi.distribute_function())
        except KeyError as e:
            assert 'KeyError' in repr(e)

    # Test execute_local_request when the dapi function (dapi.f) raises a JSONDecodeError
    with patch('xcyber360.cluster.get_nodes_info', side_effect=json.decoder.JSONDecodeError('test', 'test', 1)):
        with patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.check_xcyber360_status'):
            dapi_kwargs = {'f': cluster.get_nodes_info, 'logger': logger, 'is_async': True}
            await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=3036)


@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.check_xcyber360_status', side_effect=None)
@patch('asyncio.wait_for', new=AsyncMock(return_value='Testing'))
async def test_DistributedAPI_local_request(mock_local_request):
    """Test `local_request` method from class DistributedAPI and check the behaviour when an error raises."""
    dapi_kwargs = {'f': manager.status, 'logger': logger}
    await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

    dapi_kwargs = {'f': cluster.get_nodes_info, 'logger': logger, 'local_client_arg': 'lc'}
    await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

    dapi_kwargs['is_async'] = True
    await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

    with patch('asyncio.wait_for', new=AsyncMock(side_effect=TimeoutError('Testing'))):
        dapi = DistributedAPI(f=manager.status, logger=logger, f_kwargs={'agent_list': '*'})
        try:
            raise_if_exc(await dapi.distribute_function())
        except ProblemException as e:
            assert 'agent_list' not in dapi.f_kwargs
            assert e.ext['dapi_errors'][list(e.ext['dapi_errors'].keys())[0]]['error'] == \
                   'Timeout executing API request'

    with patch('asyncio.wait_for', new=AsyncMock(side_effect=Xcyber360Error(1001))):
        dapi_kwargs = {'f': manager.status, 'logger': logger}
        await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=1001)

        dapi_kwargs['debug'] = True
        await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=1001)

    with patch('asyncio.wait_for', new=AsyncMock(side_effect=TimeoutError())):
        dapi_kwargs = {'f': manager.status, 'logger': logger}
        await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=3021)

    orig_message = 'database or disk is full'
    orig = SQLiteOperationalError(DatabaseError(Error(Exception(orig_message))))
    with patch('asyncio.wait_for', new=AsyncMock(side_effect=OperationalError(statement=None, params=[], orig=orig))):
        dapi_kwargs = {'f': manager.status, 'logger': logger}
        await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=2008)

        dapi = DistributedAPI(f=manager.status, logger=logger, debug=True)
        try:
            raise_if_exc(await dapi.distribute_function())
        except Xcyber360InternalError as e:
            assert e.code == 2008
            assert str(e).endswith(orig_message)

    with patch('asyncio.wait_for', new=AsyncMock(side_effect=Xcyber360InternalError(1001))):
        dapi_kwargs = {'f': manager.status, 'logger': logger}
        await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=1001)

        dapi = DistributedAPI(f=manager.status, logger=logger, debug=True)
        try:
            raise_if_exc(await dapi.distribute_function())
        except Xcyber360InternalError as e:
            assert e.code == 1001

    with patch('asyncio.wait_for', new=AsyncMock(side_effect=KeyError('Testing'))):
        dapi_kwargs = {'f': manager.status, 'logger': logger}
        await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=1000)

        dapi = DistributedAPI(f=manager.status, logger=logger, debug=True)
        try:
            raise_if_exc(await dapi.distribute_function())
        except Exception as e:
            assert type(e) == KeyError

    testing_logger = TestingLogger('test')
    exc_code = 3000
    cluster_exc = Xcyber360ClusterError(exc_code)
    with patch('asyncio.wait_for', new=AsyncMock(side_effect=cluster_exc)):
        with patch.object(TestingLogger, "error") as logger_error_mock:
            # Test Xcyber360ClusterError caught in execute_local_request and ProblemException raised
            dapi_kwargs = {'f': manager.status, 'logger': testing_logger}
            await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=exc_code)

            # Test Xcyber360ClusterError is raised when using debug in execute_local_request and distribute_function
            dapi = DistributedAPI(f=manager.status, logger=testing_logger, debug=True)
            try:
                raise_if_exc(await dapi.distribute_function())
            except Xcyber360ClusterError as e:
                assert e.dapi_errors == await dapi.get_error_info(e)

            # Test the logger `error` method was called for both distribute_function calls
            logger_error_mock.assert_has_calls([call(f"{cluster_exc.message}", exc_info=False),
                                                call(f"{cluster_exc.message}", exc_info=False)])


@patch("asyncio.get_running_loop")
def test_DistributedAPI_get_client(loop_mock):
    """Test get_client function from DistributedAPI."""

    class Node:
        def __init__(self):
            self.cluster_items = {"cluster_items": ["worker1", "worker2"]}

        def get_node(self):
            pass

    logger = logging.getLogger("test")
    dapi = DistributedAPI(f=agent.get_agents_summary_status, logger=logger)
    assert isinstance(dapi.get_client(), local_client.LocalClient)

    node = Node()
    dapi = DistributedAPI(f=agent.get_agents_summary_status, node=node, logger=logger)
    assert dapi.get_client()


@patch('xcyber360.core.cluster.cluster.get_node', return_value={'type': 'worker'})
@patch('xcyber360.core.cluster.local_client.LocalClient.execute', return_value='invalid_json')
async def test_DistributedAPI_remote_request_errors(mock_client_execute, mock_get_node):
    """Check the behaviour when the execute_remote_request function raised an error"""
    # Test execute_remote_request when it raises a JSONDecodeError
    dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'local_master'}
    await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=3036)


@patch('xcyber360.core.cluster.local_client.LocalClient.execute', new=AsyncMock(return_value='{"Testing": 1}'))
async def test_DistributedAPI_remote_request():
    """Test `execute_remote_request` method from class DistributedAPI."""
    dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'remote'}
    await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)


@patch('xcyber360.core.cluster.cluster.get_node', return_value={'type': 'master', 'node': 'master-node'})
@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.get_solver_node', return_value={'worker1': ['001', '002']})
@patch('xcyber360.core.cluster.local_client.LocalClient.execute', return_value='invalid_json')
async def test_DistributedAPI_forward_request_errors(mock_client_execute, mock_get_solver_node, mock_get_node):
    """Check the behaviour when the forward_request function raised an error"""
    # Test forward_request when it raises a JSONDecodeError
    dapi_kwargs = {'f': agent.reconnect_agents, 'logger': logger, 'request_type': 'distributed_master'}
    await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=3036)


@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.execute_local_request',
       new=AsyncMock(side_effect=Xcyber360InternalError(1001)))
async def test_DistributedAPI_logger():
    """Test custom logger inside DistributedAPI class."""
    log_file_path = '/tmp/dapi_test.log'
    try:
        new_logger = logging.getLogger('dapi_test')
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.DEBUG)
        new_logger.addHandler(fh)
        dapi_kwargs = {'f': agent.get_agents_summary_status, 'logger': new_logger}
        await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=1001)
    finally:
        os.remove(log_file_path)


@patch('xcyber360.core.cluster.local_client.LocalClient.send_file', new=AsyncMock(return_value='{"Testing": 1}'))
@patch('xcyber360.core.cluster.local_client.LocalClient.execute', new=AsyncMock(return_value='{"Testing": 1}'))
@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.get_solver_node',
       new=AsyncMock(return_value=Xcyber360Result({'testing': ['001', '002']})))
async def test_DistributedAPI_tmp_file():
    """Test the behaviour when processing temporal files to be send. Master node and unknown node."""
    open('/tmp/dapi_file.txt', 'a').close()
    with patch('xcyber360.core.cluster.cluster.get_node', return_value={'type': 'master', 'node': 'unknown'}):
        with patch('xcyber360.core.cluster.dapi.dapi.get_node_wrapper',
                   return_value=AffectedItemsXcyber360Result(affected_items=[{'type': 'master', 'node': 'unknown'}])):
            dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                           'f_kwargs': {'tmp_file': '/tmp/dapi_file.txt'}}
            await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

    open('/tmp/dapi_file.txt', 'a').close()
    with patch('xcyber360.core.cluster.cluster.get_node', return_value={'type': 'unk', 'node': 'master'}):
        await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)


@patch('xcyber360.core.cluster.local_client.LocalClient.send_file', new=AsyncMock(return_value='{"Testing": 1}'))
@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.get_solver_node',
       new=AsyncMock(return_value=Xcyber360Result({'testing': ['001', '002']})))
async def test_DistributedAPI_tmp_file_cluster_error():
    """Test the behaviour when an error raises with temporal files function."""
    open('/tmp/dapi_file.txt', 'a').close()
    with patch('xcyber360.core.cluster.cluster.get_node', return_value={'type': 'master', 'node': 'unknown'}):
        with patch('xcyber360.core.cluster.dapi.dapi.get_node_wrapper', new=AsyncMock(
            return_value=AffectedItemsXcyber360Result(affected_items=[{'type': 'master', 'node': 'unknown'}]))):
            with patch('xcyber360.core.cluster.local_client.LocalClient.execute',
                       new=AsyncMock(side_effect=Xcyber360ClusterError(3022))):
                dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                               'f_kwargs': {'tmp_file': '/tmp/dapi_file.txt'}}
                await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=3022)

            open('/tmp/dapi_file.txt', 'a').close()
            with patch('xcyber360.core.cluster.local_client.LocalClient.execute',
                       new=AsyncMock(side_effect=Xcyber360ClusterError(1000))):
                dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                               'f_kwargs': {'tmp_file': '/tmp/dapi_file.txt'}}
                await raise_if_exc_routine(dapi_kwargs=dapi_kwargs, expected_error=1000)


@patch('xcyber360.core.cluster.local_client.LocalClient.execute',
       new=AsyncMock(return_value='{"items": [{"name": "master"}], "totalItems": 1}'))
@patch('xcyber360.agent.Agent.get_agents_overview', return_value={'items': [{'id': '001', 'node_name': 'master'},
                                                                        {'id': '002', 'node_name': 'master'},
                                                                        {'id': '003', 'node_name': 'unknown'}]})
async def test_DistributedAPI_get_solver_node(mock_agents_overview):
    """Test `get_solver_node` function."""
    nodes_info_result = AffectedItemsXcyber360Result()
    nodes_info_result.affected_items.append({'name': 'master'})
    common.cluster_nodes.set(['master'])

    with patch('xcyber360.core.cluster.dapi.dapi.get_nodes_info', new=AsyncMock(return_value=nodes_info_result)):
        with patch('xcyber360.core.cluster.cluster.get_node', return_value={'type': 'master', 'node': 'unknown'}):
            dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                           'f_kwargs': {'agent_list': ['001', '002']}, 'nodes': ['master']}
            await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

            dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                           'f_kwargs': {'agent_list': ['003', '004']}, 'nodes': ['master']}
            await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

            dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                           'f_kwargs': {'agent_list': ['003', '004'], 'node_id': 'worker1'}, 'nodes': ['master']}
            await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

            dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                           'f_kwargs': {'agent_list': '*'}, 'nodes': ['master']}
            await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

            dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                           'f_kwargs': {'node_id': 'master'}, 'nodes': ['master']}
            await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

            expected = AffectedItemsXcyber360Result()
            expected.affected_items = [{'id': '001', 'node_name': 'master'}]
            with patch('xcyber360.agent.get_agents_in_group', return_value=expected):
                dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                               'f_kwargs': {'group_id': 'default'}, 'nodes': ['master']}
                await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

            expected.affected_items = []
            with patch('xcyber360.agent.get_agents_in_group', return_value=expected):
                dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                               'f_kwargs': {'group_id': 'noexist'}, 'nodes': ['master']}
                await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)

            dapi_kwargs = {'f': manager.status, 'logger': logger, 'request_type': 'distributed_master',
                           'f_kwargs': {'node_list': '*'}, 'broadcasting': True, 'nodes': ['master']}
            await raise_if_exc_routine(dapi_kwargs=dapi_kwargs)


@pytest.mark.parametrize('api_request', [
    agent.get_agents_summary_status,
    xcyber360.core.manager.status
])
@patch('xcyber360.core.manager.get_manager_status', return_value={process: 'running' for process in get_manager_status()})
def test_DistributedAPI_check_xcyber360_status(status_mock, api_request):
    """Test `check_xcyber360_status` method from class DistributedAPI."""
    dapi = DistributedAPI(f=api_request, logger=logger)
    data = dapi.check_xcyber360_status()
    assert data is None


@pytest.mark.parametrize('status_value', [
    'failed',
    'restarting',
    'stopped'
])
@patch('xcyber360.core.cluster.cluster.get_node', return_value={'node': 'random_node'})
def test_DistributedAPI_check_xcyber360_status_exception(node_info_mock, status_value):
    """Test exceptions from `check_xcyber360_status` method from class DistributedAPI."""
    statuses = {process: status_value for process in sorted(get_manager_status())}
    with patch('xcyber360.core.manager.get_manager_status',
               return_value=statuses):
        dapi = DistributedAPI(f=agent.get_agents_summary_status, logger=logger)
        try:
            dapi.check_xcyber360_status()
        except Xcyber360InternalError as e:
            assert e.code == 1017
            assert statuses
            assert e._extra_message['node_name'] == 'random_node'
            extra_message = ', '.join([f'{key}->{statuses[key]}' for key in dapi.basic_services if key in statuses])
            assert e._extra_message['not_ready_daemons'] == extra_message


@patch("asyncio.Queue")
def test_APIRequestQueue_init(queue_mock):
    """Test `APIRequestQueue` constructor."""
    server = DistributedAPI(f=agent.get_agents_summary_status, logger=logger)
    api_request_queue = APIRequestQueue(server=server)
    api_request_queue.add_request(b'testing')
    assert api_request_queue.server == server
    queue_mock.assert_called_once()


@patch("xcyber360.core.cluster.common.import_module", return_value="os.path")
@patch("asyncio.get_event_loop")
async def test_APIRequestQueue_run(loop_mock, import_module_mock):
    """Test `APIRequestQueue.run` function."""

    class DistributedAPI_mock:
        def __init__(self):
            pass

        async def distribute_function(self):
            pass

    class NodeMock:
        async def send_request(self, command, data):
            pass

        async def send_string(self, command):
            return command

    class ServerMock:
        def __init__(self):
            self.clients = {"names": ["w1", "w2"]}

    class RequestQueueMock:
        async def get(self):
            return 'xcyber360*request_queue*test ' \
                   '{"f": {"__callable__": {"__name__": "join", "__qualname__": "join", "__module__": "join"}}}'

    with patch.object(logger, "error", side_effect=Exception("break while true")) as logger_mock:
        server = ServerMock()
        apirequest = APIRequestQueue(server=server)
        apirequest.logger = logger
        apirequest.request_queue = RequestQueueMock()
        with pytest.raises(Exception, match=".*break while true.*"):
            await apirequest.run()
        logger_mock.assert_called_once_with("Error in DAPI request. The destination node is "
                                            "not connected or does not exist: 'xcyber360'.")

        node = NodeMock()
        with patch.object(node, "send_request", side_effect=Xcyber360ClusterError(3020, extra_message="test")):
            with patch.object(node, "send_string", return_value=b"noerror"):
                with patch("xcyber360.core.cluster.dapi.dapi.DistributedAPI", return_value=DistributedAPI_mock()):
                    server.clients = {"xcyber360": node}
                    with pytest.raises(Exception):
                        await apirequest.run()

            with patch.object(node, "send_string", Exception("break while true")):
                with patch("xcyber360.core.cluster.dapi.dapi.DistributedAPI", return_value=DistributedAPI_mock()):
                    with patch("xcyber360.core.cluster.dapi.dapi.contextlib.suppress", side_effect=Exception()):
                        apirequest.logger = logging.getLogger("apirequest")
                        with pytest.raises(Exception):
                            await apirequest.run()