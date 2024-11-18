

import asyncio
import os
import signal
import sys
from unittest.mock import call, patch, Mock

import pytest

import scripts.xcyber360_server as xcyber360_server
from xcyber360.core import pyDaemonModule
from xcyber360.core.cluster.utils import HAPROXY_DISABLED, HAPROXY_HELPER

xcyber360_server.pyDaemonModule = pyDaemonModule


def test_set_logging():
    """Check and set the behavior of set_logging function."""
    import xcyber360.core.cluster.utils as cluster_utils

    xcyber360_server.cluster_utils = cluster_utils
    with patch.object(cluster_utils, 'ClusterLogger') as clusterlogger_mock:
        assert xcyber360_server.set_logging(foreground_mode=False, debug_mode=0)
        clusterlogger_mock.assert_called_once_with(
            foreground_mode=False, log_path='cluster.log', debug_level=0,
            tag='%(asctime)s %(levelname)s: [%(tag)s] [%(subtag)s] %(message)s')


@patch('builtins.print')
def test_print_version(print_mock):
    """Set the scheme to be printed."""
    with patch('xcyber360.core.cluster.__version__', 'TEST'):
        xcyber360_server.print_version()
        print_mock.assert_called_once_with(
            '\nXcyber360 TEST - Xcyber360 Inc\n\nThis program is free software; you can redistribute it and/or modify\n'
            'it under the terms of the GNU General Public License (version 2) as \npublished by the '
            'Free Software Foundation. For more details, go to \nhttps://www.gnu.org/licenses/gpl.html\n')


@patch('scripts.xcyber360_server.os.getpid', return_value=1001)
def test_exit_handler(os_getpid_mock):
    """Set the behavior when exiting the script."""

    class SignalMock:
        SIGTERM = 0
        SIG_DFL = 1

        class Signals:
            def __init__(self, signum):
                self.name = signum

        @staticmethod
        def signal(signalnum, handler):
            assert signalnum == 9
            assert handler == SignalMock.SIG_DFL

    class LoggerMock:
        def __init__(self):
            pass

        def info(self, msg):
            pass

    def original_sig_handler(signum, frame):
        pass

    original_sig_handler_not_callable = 1

    xcyber360_server.main_logger = LoggerMock()
    xcyber360_server.original_sig_handler = original_sig_handler
    with patch('scripts.xcyber360_server.signal', SignalMock), \
        patch.object(xcyber360_server, 'main_logger') as main_logger_mock, \
        patch.object(xcyber360_server.pyDaemonModule, 'delete_child_pids') as delete_child_pids_mock, \
        patch.object(xcyber360_server.pyDaemonModule, 'delete_pid') as delete_pid_mock, \
        patch.object(xcyber360_server, 'original_sig_handler') as original_sig_handler_mock, \
        patch.object(xcyber360_server.pyDaemonModule, 'get_parent_pid', return_value=999), \
        patch('scripts.xcyber360_server.os.kill') as os_kill_mock:
        xcyber360_server.exit_handler(9, 99)
        main_logger_mock.assert_has_calls([call.info('SIGNAL [(9)-(9)] received. Shutting down...')])
        os_kill_mock.assert_has_calls([
            call(999, SignalMock.SIGTERM),
            call(999, SignalMock.SIGTERM),
        ])
        delete_child_pids_mock.assert_has_calls([
            call('xcyber360-server', os_getpid_mock.return_value, main_logger_mock),
        ])
        delete_pid_mock.assert_has_calls([
            call('xcyber360-server', os_getpid_mock.return_value),
        ])
        original_sig_handler_mock.assert_called_once_with(9, 99)
        main_logger_mock.reset_mock()
        delete_child_pids_mock.reset_mock()
        delete_pid_mock.reset_mock()
        original_sig_handler_mock.reset_mock()

        xcyber360_server.original_sig_handler = original_sig_handler_not_callable
        xcyber360_server.exit_handler(9, 99)
        main_logger_mock.assert_has_calls([call.info('SIGNAL [(9)-(9)] received. Shutting down...')])
        os_kill_mock.assert_has_calls([
            call(999, SignalMock.SIGTERM),
            call(999, SignalMock.SIGTERM),
        ])
        delete_child_pids_mock.assert_has_calls([
            call('xcyber360-server', 1001, main_logger_mock),
        ])
        delete_pid_mock.assert_has_calls([
            call('xcyber360-server', 1001),
        ])
        original_sig_handler_mock.assert_not_called()


@pytest.mark.parametrize("foreground, root", [
    (True, True),
    (True, False),
    (False, True),
    (False, False),
])
@patch('subprocess.Popen')
def test_start_daemons(mock_popen, foreground, root):
    """Validate that `start_daemons` works as expected."""
    from xcyber360.core import pyDaemonModule

    class LoggerMock:
        def __init__(self):
            pass

        def info(self, msg):
            pass

    xcyber360_server.main_logger = LoggerMock
    pid = 2
    process_mock = Mock()
    attrs = {'poll.return_value': 0, 'wait.return_value': 0}
    process_mock.configure_mock(**attrs)
    mock_popen.return_value = process_mock


    with patch.object(xcyber360_server, 'main_logger') as main_logger_mock, \
        patch.object(xcyber360_server.pyDaemonModule, 'get_parent_pid', return_value=pid), \
        patch.object(xcyber360_server.pyDaemonModule, 'create_pid'):
        xcyber360_server.start_daemons(foreground, root)

    mock_popen.assert_has_calls([
        call([xcyber360_server.ENGINE_BINARY_PATH, 'server', 'start']),
        call([xcyber360_server.EMBEDDED_PYTHON_PATH, xcyber360_server.MANAGEMENT_API_SCRIPT_PATH] + \
              (['-r'] if root else []) + (['-f'] if foreground else [])),
        call([xcyber360_server.EMBEDDED_PYTHON_PATH, xcyber360_server.COMMS_API_SCRIPT_PATH] + \
              (['-r'] if root else []) + (['-f'] if foreground else [])),
    ], any_order=True)

    if foreground:
        pid = mock_popen().pid

    main_logger_mock.info.assert_has_calls([
        call(f'Started xcyber360-engined (pid: {mock_popen().pid})'),
        call(f'Started xcyber360-apid (pid: {pid})'),
        call(f'Started xcyber360-comms-apid (pid: {pid})'),
    ])


@patch('subprocess.Popen')
def test_start_daemons_ko(mock_popen):
    """Validate that `start_daemons` works as expected when the subprocesses fail."""
    class LoggerMock:
        def __init__(self):
            pass

        def info(self, msg):
            pass

    xcyber360_server.main_logger = LoggerMock
    pid = 2
    process_mock = Mock()
    attrs = {'poll.return_value': 1, 'wait.return_value': 1}
    process_mock.configure_mock(**attrs)
    mock_popen.return_value = process_mock

    with patch.object(xcyber360_server, 'main_logger') as main_logger_mock, \
        patch.object(xcyber360_server.pyDaemonModule, 'get_parent_pid', return_value=pid):
        xcyber360_server.start_daemons(False, False)

    mock_popen.assert_has_calls([
        call([xcyber360_server.ENGINE_BINARY_PATH, 'server', 'start']),
        call([xcyber360_server.EMBEDDED_PYTHON_PATH, xcyber360_server.MANAGEMENT_API_SCRIPT_PATH]),
        call([xcyber360_server.EMBEDDED_PYTHON_PATH, xcyber360_server.COMMS_API_SCRIPT_PATH]),
    ], any_order=True)

    main_logger_mock.error.assert_has_calls([
        call('Error starting xcyber360-engined: return code 1'),
        call('Error starting xcyber360-apid: return code 1'),
        call('Error starting xcyber360-comms-apid: return code 1'),
    ])


@patch('scripts.xcyber360_server.os.kill')
@patch('scripts.xcyber360_server.os.getpid', return_value=999)
def test_shutdown_daemon(os_getpid_mock, os_kill_mock):
    """Validate that `shutdown_daemon` works as expected."""
    class LoggerMock:
        def __init__(self):
            pass

        def info(self, msg):
            pass

    xcyber360_server.main_logger = LoggerMock

    with patch.object(xcyber360_server, 'main_logger') as main_logger_mock, \
        patch.object(xcyber360_server.pyDaemonModule, 'get_parent_pid', return_value=os_getpid_mock.return_value):
        xcyber360_server.shutdown_daemon(xcyber360_server.MANAGEMENT_API_DAEMON_NAME)

    os_kill_mock.assert_called_once_with(999, signal.SIGTERM)
    main_logger_mock.info.assert_has_calls([
        call(f'Shutting down {xcyber360_server.MANAGEMENT_API_DAEMON_NAME} (pid: {os_getpid_mock.return_value})'),
    ])


@pytest.mark.asyncio
@pytest.mark.parametrize('helper_disabled', (True, False))
async def test_master_main(helper_disabled: bool):
    """Check and set the behavior of master_main function."""
    import xcyber360.core.cluster.utils as cluster_utils
    cluster_config = {'test': 'config', HAPROXY_HELPER: {HAPROXY_DISABLED: helper_disabled}}

    class Arguments:
        def __init__(self, performance_test, concurrency_test):
            self.performance_test = performance_test
            self.concurrency_test = concurrency_test

    class TaskPoolMock:
        def __init__(self):
            self._max_workers = 1

        def map(self, first, second):
            assert first == cluster_utils.process_spawn_sleep
            assert second == range(1)

    class MasterMock:
        def __init__(self, performance_test, concurrency_test, configuration, logger, cluster_items):
            assert performance_test == 'test_performance'
            assert concurrency_test == 'concurrency_test'
            assert configuration == cluster_config
            assert logger == 'test_logger'
            assert cluster_items == {'node': 'item'}
            self.task_pool = TaskPoolMock()

        def start(self):
            return 'MASTER_START'

    class LocalServerMasterMock:
        def __init__(self, performance_test, logger, concurrency_test, node, configuration, cluster_items):
            assert performance_test == 'test_performance'
            assert logger == 'test_logger'
            assert concurrency_test == 'concurrency_test'
            assert configuration == cluster_config
            assert cluster_items == {'node': 'item'}

        def start(self):
            return 'LOCALSERVER_START'

    class HAPHElperMock:
        @classmethod
        def start(cls):
            return 'HAPHELPER_START'


    async def gather(first, second, third=None):
        assert first == 'MASTER_START'
        assert second == 'LOCALSERVER_START'
        if third is not None:
            assert third == 'HAPHELPER_START'


    xcyber360_server.cluster_utils = cluster_utils
    args = Arguments(performance_test='test_performance', concurrency_test='concurrency_test')
    with patch('scripts.xcyber360_server.asyncio.gather', gather), \
        patch('xcyber360.core.cluster.master.Master', MasterMock), \
        patch('xcyber360.core.cluster.local_server.LocalServerMaster', LocalServerMasterMock), \
        patch('xcyber360.core.cluster.hap_helper.hap_helper.HAPHelper', HAPHElperMock):
        await xcyber360_server.master_main(
            args=args,
            cluster_config=cluster_config,
            cluster_items={'node': 'item'},
            logger='test_logger'
        )

@pytest.mark.asyncio
@patch("asyncio.sleep", side_effect=IndexError)
async def test_worker_main(asyncio_sleep_mock):
    """Check and set the behavior of worker_main function."""
    import xcyber360.core.cluster.utils as cluster_utils

    class Arguments:
        def __init__(self, performance_test, concurrency_test, send_file, send_string):
            self.performance_test = performance_test
            self.concurrency_test = concurrency_test
            self.send_file = send_file
            self.send_string = send_string

    class TaskPoolMock:
        def __init__(self):
            self._max_workers = 1

        def map(self, first, second):
            assert first == cluster_utils.process_spawn_sleep
            assert second == range(1)

    class LoggerMock:
        def __init__(self):
            pass

        def warning(self, msg):
            pass

    class WorkerMock:
        def __init__(self, performance_test, concurrency_test, configuration, logger, cluster_items, file, string,
                     task_pool):
            assert performance_test == 'test_performance'
            assert concurrency_test == 'concurrency_test'
            assert configuration == {'test': 'config'}
            assert file is True
            assert string is True
            assert logger == 'test_logger'
            assert cluster_items == {'intervals': {'worker': {'connection_retry': 34}}}
            assert task_pool is None
            self.task_pool = TaskPoolMock()

        def start(self):
            return 'WORKER_START'

    class LocalServerWorkerMock:
        def __init__(self, performance_test, logger, concurrency_test, node, configuration, cluster_items):
            assert performance_test == 'test_performance'
            assert logger == 'test_logger'
            assert concurrency_test == 'concurrency_test'
            assert configuration == {'test': 'config'}
            assert cluster_items == {'intervals': {'worker': {'connection_retry': 34}}}

        def start(self):
            return 'LOCALSERVER_START'

    async def gather(first, second):
        assert first == 'WORKER_START'
        assert second == 'LOCALSERVER_START'
        raise asyncio.CancelledError()

    xcyber360_server.cluster_utils = cluster_utils
    xcyber360_server.main_logger = LoggerMock
    args = Arguments(performance_test='test_performance', concurrency_test='concurrency_test',
                     send_file=True, send_string=True)

    with patch.object(xcyber360_server, 'main_logger') as main_logger_mock:
        with patch('concurrent.futures.ProcessPoolExecutor', side_effect=FileNotFoundError) as processpoolexecutor_mock:
            with patch('scripts.xcyber360_server.asyncio.gather', gather):
                with patch('scripts.xcyber360_server.logging.info') as logging_info_mock:
                    with patch('xcyber360.core.cluster.worker.Worker', WorkerMock):
                        with patch('xcyber360.core.cluster.local_server.LocalServerWorker', LocalServerWorkerMock):
                            with pytest.raises(IndexError):
                                await xcyber360_server.worker_main(
                                    args=args, cluster_config={'test': 'config'},
                                    cluster_items={'intervals': {'worker': {'connection_retry': 34}}},
                                    logger='test_logger')
                            processpoolexecutor_mock.assert_called_once_with(max_workers=1)
                            main_logger_mock.assert_has_calls([
                                call.warning(
                                    "In order to take advantage of Xcyber360 4.3.0 cluster improvements, the directory "
                                    "'/dev/shm' must be accessible by the 'xcyber360' user. Check that this file has "
                                    "permissions to be accessed by all users. Changing the file permissions to 777 "
                                    "will solve this issue."),
                                call.warning(
                                    'The Xcyber360 cluster will be run without the improvements added in Xcyber360 4.3.0 and '
                                    'higher versions.')
                            ])
                            logging_info_mock.assert_called_once_with('Connection with server has been lost. '
                                                                      'Reconnecting in 10 seconds.')
                            asyncio_sleep_mock.assert_called_once_with(34)


@pytest.mark.parametrize(
        'command,expected_args',
        [
            (
                'start',
                [
                    'func',
                    'foreground',
                    'performance_test',
                    'concurrency_test',
                    'send_string',
                    'send_file',
                    'root',
                    'config_file',
                    'test_config'
                ]
            ),
            ('stop', ['func', 'foreground']),
            ('status', ['func']),
        ]
)
def test_get_script_arguments(command, expected_args):
    """Set the xcyber360_server script parameters."""
    from xcyber360.core import common

    xcyber360_server.common = common

    expected_args.extend(['version', 'debug_level'])
    with patch('argparse._sys.argv', ['xcyber360_server.py', command]):
        with patch.object(xcyber360_server.common, 'XCYBER360_CONF', 'testing/path'):
            parsed_args = xcyber360_server.get_script_arguments().parse_args()

            for arg in expected_args:
                assert hasattr(parsed_args, arg)


@patch('scripts.xcyber360_server.sys.exit', side_effect=sys.exit)
@patch('scripts.xcyber360_server.os.getpid', return_value=543)
@patch('scripts.xcyber360_server.os.setgid')
@patch('scripts.xcyber360_server.os.setuid')
@patch('scripts.xcyber360_server.os.chmod')
@patch('scripts.xcyber360_server.os.chown')
@patch('scripts.xcyber360_server.os.path.exists', return_value=True)
@patch('builtins.print')
def test_main(print_mock, path_exists_mock, chown_mock, chmod_mock, setuid_mock, setgid_mock, getpid_mock, exit_mock):
    """Check and set the behavior of xcyber360_server main function."""
    import xcyber360.core.cluster.utils as cluster_utils
    from xcyber360.core import common, pyDaemonModule

    class Arguments:
        def __init__(self, config_file, test_config, foreground, root):
            self.config_file = config_file
            self.test_config = test_config
            self.foreground = foreground
            self.root = root

    class LoggerMock:
        def __init__(self):
            pass

        def info(self, msg):
            pass

        def error(self, msg):
            pass

    args = Arguments(config_file='test', test_config=True, foreground=False, root=False)
    xcyber360_server.main_logger = LoggerMock()
    xcyber360_server.args = args
    xcyber360_server.common = common
    xcyber360_server.cluster_utils = cluster_utils
    with patch.object(common, 'xcyber360_uid', return_value='uid_test'), \
        patch.object(common, 'xcyber360_gid', return_value='gid_test'), \
        patch.object(xcyber360_server.cluster_utils, 'read_config', return_value={'node_type': 'master'}), \
        patch.object(xcyber360_server.main_logger, 'error') as main_logger_mock, \
        patch.object(xcyber360_server.main_logger, 'info') as main_logger_info_mock:

        with patch.object(xcyber360_server.cluster_utils, 'read_config', side_effect=Exception):
            with pytest.raises(SystemExit):
                xcyber360_server.main()
            main_logger_mock.assert_called_once()
            main_logger_mock.reset_mock()
            path_exists_mock.assert_any_call(xcyber360_server.CLUSTER_LOG)
            chown_mock.assert_called_with(xcyber360_server.CLUSTER_LOG, 'uid_test', 'gid_test')
            chmod_mock.assert_called_with(xcyber360_server.CLUSTER_LOG, 432)
            exit_mock.assert_called_once_with(1)
            exit_mock.reset_mock()

        with patch('xcyber360.core.cluster.cluster.check_cluster_config', side_effect=IndexError):
            with pytest.raises(SystemExit):
                xcyber360_server.main()
            main_logger_mock.assert_called_once()
            exit_mock.assert_called_once_with(1)
            exit_mock.reset_mock()

        with patch('xcyber360.core.cluster.cluster.check_cluster_config', return_value=None):
            with pytest.raises(SystemExit):
                xcyber360_server.main()
            main_logger_mock.assert_called_once()
            exit_mock.assert_called_once_with(0)
            main_logger_mock.reset_mock()
            exit_mock.reset_mock()

            args.test_config = False
            xcyber360_server.args = args
            with patch('xcyber360.core.cluster.cluster.clean_up') as clean_up_mock, \
                patch('scripts.xcyber360_server.clean_pid_files') as clean_pid_files_mock, \
                patch('xcyber360.core.authentication.keypair_exists', return_value=False), \
                patch('xcyber360.core.authentication.generate_keypair') as generate_keypair_mock, \
                patch('scripts.xcyber360_server.start_daemons') as start_daemons_mock, \
                patch.object(xcyber360_server.pyDaemonModule, 'get_parent_pid', return_value=999), \
                patch('os.kill') as os_kill_mock, \
                patch.object(xcyber360_server.pyDaemonModule, 'pyDaemon') as pyDaemon_mock, \
                patch.object(xcyber360_server.pyDaemonModule, 'create_pid') as create_pid_mock, \
                patch.object(xcyber360_server.pyDaemonModule, 'delete_child_pids'), \
                patch.object(xcyber360_server.pyDaemonModule,'delete_pid') as delete_pid_mock:
                xcyber360_server.main()
                main_logger_mock.assert_any_call(
                    "Unhandled exception: name 'cluster_items' is not defined")
                main_logger_mock.reset_mock()
                clean_up_mock.assert_called_once()
                clean_pid_files_mock.assert_called_once_with('xcyber360-server')
                pyDaemon_mock.assert_called_once()
                setuid_mock.assert_called_once_with('uid_test')
                setgid_mock.assert_called_once_with('gid_test')
                getpid_mock.assert_called()
                os_kill_mock.assert_has_calls([
                    call(999, signal.SIGTERM),
                    call(999, signal.SIGTERM),
                ])
                create_pid_mock.assert_called_once_with('xcyber360-server', 543)
                delete_pid_mock.assert_has_calls([
                    call('xcyber360-server', 543),
                ])
                main_logger_info_mock.assert_has_calls([
                    call('Generating JWT signing key pair'),
                    call('Shutting down xcyber360-engined (pid: 999)'),
                    call('Shutting down xcyber360-apid (pid: 999)'),
                    call('Shutting down xcyber360-comms-apid (pid: 999)'),
                ])
                generate_keypair_mock.assert_called_once()
                start_daemons_mock.assert_called_once()

                args.foreground = True
                xcyber360_server.main()
                print_mock.assert_called_once_with('Starting cluster in foreground (pid: 543)')

                xcyber360_server.cluster_items = {}
                with patch('scripts.xcyber360_server.master_main', side_effect=KeyboardInterrupt('TESTING')):
                    xcyber360_server.main()
                    main_logger_info_mock.assert_any_call('SIGINT received. Shutting down...')

                with patch('scripts.xcyber360_server.master_main', side_effect=MemoryError('TESTING')):
                    xcyber360_server.main()
                    main_logger_mock.assert_any_call(
                        "Directory '/tmp' needs read, write & execution "
                        "permission for 'xcyber360' user")


@patch('scripts.xcyber360_server.shutdown_cluster')
@patch('scripts.xcyber360_server.os.kill')
def test_stop(os_mock, shutdown_mock):
    """Check and set the behavior of xcyber360_server stop function."""
    from xcyber360.core import common

    xcyber360_server.common = common
    pid = 123

    with patch.object(pyDaemonModule, 'get_xcyber360_server_pid', return_value=pid):
        xcyber360_server.stop()

    shutdown_mock.assert_called_once_with(pid)
    os_mock.assert_called_once_with(pid, signal.SIGKILL)


def test_stop_ko():
    """Validate that `stop` works as expected when the server is not running."""
    from xcyber360.core import common

    xcyber360_server.common = common
    xcyber360_server.main_logger = Mock()

    with patch.object(pyDaemonModule, 'get_xcyber360_server_pid', side_effect=StopIteration):
        with pytest.raises(SystemExit, match='1'):
            xcyber360_server.stop()

    xcyber360_server.main_logger.error.assert_called_once_with('Xcyber360 server is not running.')


@pytest.mark.parametrize(
        'daemons,expected',
        [
            (
                [
                    xcyber360_server.SERVER_DAEMON_NAME,
                    xcyber360_server.COMMS_API_DAEMON_NAME,
                    xcyber360_server.ENGINE_DAEMON_NAME,
                    xcyber360_server.MANAGEMENT_API_DAEMON_NAME,
                ],
                [
                    f'{xcyber360_server.SERVER_DAEMON_NAME} is running...',
                    f'{xcyber360_server.COMMS_API_DAEMON_NAME} is running...',
                    f'{xcyber360_server.ENGINE_DAEMON_NAME} is running...',
                    f'{xcyber360_server.MANAGEMENT_API_DAEMON_NAME} is running...',
                ]
            ),
            (
                [
                    xcyber360_server.COMMS_API_DAEMON_NAME,
                    xcyber360_server.ENGINE_DAEMON_NAME,
                    xcyber360_server.MANAGEMENT_API_DAEMON_NAME,
                ],
                [
                    f'{xcyber360_server.SERVER_DAEMON_NAME} is not running...',
                    f'{xcyber360_server.COMMS_API_DAEMON_NAME} is running...',
                    f'{xcyber360_server.ENGINE_DAEMON_NAME} is running...',
                    f'{xcyber360_server.MANAGEMENT_API_DAEMON_NAME} is running...',
                ]
            ),
            (
                [
                    xcyber360_server.SERVER_DAEMON_NAME,
                    xcyber360_server.COMMS_API_DAEMON_NAME,
                ],
                [
                    f'{xcyber360_server.SERVER_DAEMON_NAME} is running...',
                    f'{xcyber360_server.COMMS_API_DAEMON_NAME} is running...',
                    f'{xcyber360_server.ENGINE_DAEMON_NAME} is not running...',
                    f'{xcyber360_server.MANAGEMENT_API_DAEMON_NAME} is not running...',
                ]
            ),
        ]
)
def test_status(capsys, daemons, expected):
    """Check and set the behavior of xcyber360_server `status` function."""
    from xcyber360.core import common

    xcyber360_server.common = common

    with patch.object(pyDaemonModule, 'get_running_processes', return_value=daemons):
        xcyber360_server.status()

    captured = capsys.readouterr().out.split('\n')

    for e in expected:
        assert e in captured
