

import json
from contextvars import ContextVar
from grp import getgrnam
from pwd import getpwnam
from unittest.mock import patch

import pytest

from xcyber360.core.common import find_xcyber360_path, xcyber360_uid, xcyber360_gid, async_context_cached, context_cached, \
    reset_context_cache, get_context_cache


@pytest.mark.parametrize('fake_path, expected', [
    ('/var/ossec/framework/python/lib/python3.7/site-packages/xcyber360-3.10.0-py3.7.egg/xcyber360', '/var/ossec'),
    ('/my/custom/path/framework/python/lib/python3.7/site-packages/xcyber360-3.10.0-py3.7.egg/xcyber360', '/my/custom/path'),
    ('/my/fake/path', '')
])
def test_find_xcyber360_path(fake_path, expected):
    with patch('xcyber360.core.common.__file__', new=fake_path):
        assert (find_xcyber360_path.__wrapped__() == expected)


def test_find_xcyber360_path_relative_path():
    with patch('os.path.abspath', return_value='~/framework'):
        assert (find_xcyber360_path.__wrapped__() == '~')


def test_xcyber360_uid():
    with patch('xcyber360.core.common.getpwnam', return_value=getpwnam("root")):
        xcyber360_uid()


def test_xcyber360_gid():
    with patch('xcyber360.core.common.getgrnam', return_value=getgrnam("root")):
        xcyber360_gid()


async def test_async_context_cached():
    """Verify that async_context_cached decorator correctly saves and returns saved value when called again."""

    test_async_context_cached.calls_to_foo = 0

    @async_context_cached('foobar')
    async def foo(arg='bar', **data):
        test_async_context_cached.calls_to_foo += 1
        return arg

    # The result of function 'foo' is being cached and it has been called once
    assert await foo() == 'bar' and test_async_context_cached.calls_to_foo == 1
    assert await foo() == 'bar' and test_async_context_cached.calls_to_foo == 1
    assert isinstance(get_context_cache()[json.dumps({"key": "foobar", "args": [], "kwargs": {}})], ContextVar)

    # foo called with an argument
    assert await foo('other_arg') == 'other_arg' and test_async_context_cached.calls_to_foo == 2
    assert isinstance(get_context_cache()[json.dumps({"key": "foobar", "args": ['other_arg'], "kwargs": {}})],
                      ContextVar)

    # foo called with the same argument as default, a new context var is created in the cache
    assert await foo('bar') == 'bar' and test_async_context_cached.calls_to_foo == 3
    assert isinstance(get_context_cache()[json.dumps({"key": "foobar", "args": ['bar'], "kwargs": {}})], ContextVar)

    # Reset cache and calls to foo
    reset_context_cache()
    test_async_context_cached.calls_to_foo = 0

    # foo called with kwargs, a new context var is created with kwargs not empty
    assert await foo(data='bar') == 'bar' and test_async_context_cached.calls_to_foo == 1
    assert isinstance(get_context_cache()[json.dumps({"key": "foobar", "args": [], "kwargs": {"data": "bar"}})],
                      ContextVar)


def test_context_cached():
    """Verify that context_cached decorator correctly saves and returns saved value when called again."""

    test_context_cached.calls_to_foo = 0

    @context_cached('foobar')
    def foo(arg='bar', **data):
        test_context_cached.calls_to_foo += 1
        return arg

    # The result of function 'foo' is being cached and it has been called once
    assert foo() == 'bar' and test_context_cached.calls_to_foo == 1, '"bar" should be returned with 1 call to foo.'
    assert foo() == 'bar' and test_context_cached.calls_to_foo == 1, '"bar" should be returned with 1 call to foo.'
    assert isinstance(get_context_cache()[json.dumps({"key": "foobar", "args": [], "kwargs": {}})], ContextVar)

    # foo called with an argument
    assert foo('other_arg') == 'other_arg' and test_context_cached.calls_to_foo == 2, '"other_arg" should be ' \
                                                                                      'returned with 2 calls to foo. '
    assert isinstance(get_context_cache()[json.dumps({"key": "foobar", "args": ['other_arg'], "kwargs": {}})],
                      ContextVar)

    # foo called with the same argument as default, a new context var is created in the cache
    assert foo('bar') == 'bar' and test_context_cached.calls_to_foo == 3, '"bar" should be returned with 3 calls to ' \
                                                                          'foo. '
    assert isinstance(get_context_cache()[json.dumps({"key": "foobar", "args": ['bar'], "kwargs": {}})], ContextVar)

    # Reset cache and calls to foo
    reset_context_cache()
    test_context_cached.calls_to_foo = 0

    # foo called with kwargs, a new context var is created with kwargs not empty
    assert foo(data='bar') == 'bar' and test_context_cached.calls_to_foo == 1, '"bar" should be returned with 1 ' \
                                                                               'calls to foo. '
    assert isinstance(get_context_cache()[json.dumps({"key": "foobar", "args": [], "kwargs": {"data": "bar"}})],
                      ContextVar)

@pytest.mark.xfail(reason="This module it is deprecated.", run=False)
@patch('xcyber360.core.logtest.create_xcyber360_socket_message', side_effect=SystemExit)
def test_origin_module_context_var_framework(mock_create_socket_msg):
    """Test that the origin_module context variable is being set to framework."""
    from xcyber360 import logtest

    # side_effect used to avoid mocking the rest of functions
    with pytest.raises(SystemExit):
        logtest.run_logtest()

    assert mock_create_socket_msg.call_args[1]['origin']['module'] == 'framework'


@pytest.mark.asyncio
@pytest.mark.xfail(reason="This module it is deprecated.", run=False)
@patch('xcyber360.core.logtest.create_xcyber360_socket_message', side_effect=SystemExit)
@patch('xcyber360.core.cluster.dapi.dapi.DistributedAPI.check_xcyber360_status', side_effect=None)
async def test_origin_module_context_var_api(mock_check_xcyber360_status, mock_create_socket_msg):
    """Test that the origin_module context variable is being set to API."""
    import logging
    from xcyber360.core.cluster.dapi import dapi
    from xcyber360 import logtest

    # side_effect used to avoid mocking the rest of functions
    with pytest.raises(SystemExit):
        d = dapi.DistributedAPI(f=logtest.run_logtest, logger=logging.getLogger('xcyber360'), is_async=True)
        await d.distribute_function()

    assert mock_create_socket_msg.call_args[1]['origin']['module'] == 'API'
