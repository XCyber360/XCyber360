#!/usr/bin/env python


import os
import sys
from unittest.mock import patch, MagicMock
from xcyber360.core.exception import Xcyber360InternalError

import pytest

pytest.skip("This module it is deprecated.", allow_module_level=True)

DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "test_cdb_list")

with patch('xcyber360.core.common.getgrnam'):
    with patch('xcyber360.core.common.getpwnam'):
        sys.modules['xcyber360.rbac.orm'] = MagicMock()
        import xcyber360.rbac.decorators
        from xcyber360.tests.util import RBAC_bypasser

        del sys.modules['xcyber360.rbac.orm']
        xcyber360.rbac.decorators.expose_resources = RBAC_bypasser

        from xcyber360.cdb_list import get_lists, get_path_lists, iterate_lists, get_list_file, upload_list_file,\
            delete_list_file
        from xcyber360.core import common
        from xcyber360.core.results import AffectedItemsXcyber360Result

RELATIVE_PATH = os.path.join("framework", "xcyber360", "tests", "data", "test_cdb_list")
NAME_FILE_1 = "test_lists_1"
NAME_FILE_2 = "test_lists_2"
NAME_FILES = [NAME_FILE_1, NAME_FILE_2]

RESULT_GET_LIST_FILE_1 = [{'items': [{'key': 'test-xcyber360-w', 'value': 'write'},
                                     {'key': 'test-xcyber360-r', 'value': 'read'},
                                     {'key': 'test-xcyber360-a', 'value': 'attribute'},
                                     {'key': 'test-xcyber360-x', 'value': 'execute'},
                                     {'key': 'test-xcyber360-c', 'value': 'command'}
                                     ],
                           'relative_dirname': RELATIVE_PATH,
                           'filename': NAME_FILE_1
                           }]
RESULT_GET_LIST_FILE_2 = [{'items': [{'key': 'test-ossec-w', 'value': 'write'},
                                     {'key': 'test-ossec-r', 'value': 'read'},
                                     {'key': 'test-ossec-x', 'value': 'execute'}
                                     ],
                           'relative_dirname': RELATIVE_PATH,
                           'filename': NAME_FILE_2
                           }]
RESULT_GET_PATH_LIST_FILE_1 = [{'filename': NAME_FILE_1, 'relative_dirname': RELATIVE_PATH}]
RESULT_GET_PATH_LIST_FILE_2 = [{'filename': NAME_FILE_2, 'relative_dirname': RELATIVE_PATH}]

RESULTS_GET_LIST = RESULT_GET_LIST_FILE_1 + RESULT_GET_LIST_FILE_2
RESULTS_GET_PATH_LIST = RESULT_GET_PATH_LIST_FILE_1 + RESULT_GET_PATH_LIST_FILE_2

TOTAL_LISTS = len(NAME_FILES)


def lists_path_mock(**kwargs):
    """Mock iterate_lists to avoid the default parameter."""
    kwargs['absolute_path'] = DATA_PATH
    return iterate_lists(**kwargs)


# Tests

@pytest.mark.parametrize("paths, expected_result", [
    ([NAME_FILE_1], RESULT_GET_LIST_FILE_1),
    (NAME_FILES, RESULTS_GET_LIST)
])
@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH)
def test_get_lists(paths, expected_result):
    """Test basic `get_list` functionality.

    This will obtain the content of some CDB lists using `get_list'' without any other parameter aside from `path`.

    Parameters
    ----------
    paths : list of str
        A list of CDB files to read, with their relative path.
    expected_result : list of dict
        The content of the CDB file or files read
    """
    result = get_lists(filename=paths)
    assert isinstance(result, AffectedItemsXcyber360Result)
    assert result.total_affected_items == len(paths)
    assert result.affected_items == expected_result


@pytest.mark.parametrize("limit", [1, 2])
@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH)
def test_get_lists_limit(limit):
    """Test `get_lists` functionality when using the `limit` parameter.

    Parameters
    ----------
    limit : int
        Maximum number of items to be returned by `get_lists`
    """
    result = get_lists(filename=NAME_FILES, limit=limit)
    assert limit > 0
    assert isinstance(result, AffectedItemsXcyber360Result)
    assert result.total_affected_items == TOTAL_LISTS
    assert result.affected_items == RESULTS_GET_LIST[:limit]


@pytest.mark.parametrize("offset", [0, 1])
@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH)
def test_get_lists_offset(offset):
    """Test `get_lists` functionality when using the `offset` parameter.

    Parameters
    ----------
    offset : int
         Indicates the first item to return.
    """
    result = get_lists(filename=NAME_FILES, offset=offset)
    assert isinstance(result, AffectedItemsXcyber360Result)
    assert result.total_affected_items == TOTAL_LISTS
    assert result.affected_items == RESULTS_GET_LIST[offset:]


@pytest.mark.parametrize("search_text, complementary_search, search_in_fields, paths, expected_result", [
    ("command", False, None, NAME_FILES, RESULT_GET_LIST_FILE_1),
    ("test-ossec-w", False, None, NAME_FILES, RESULT_GET_LIST_FILE_2),
    ("command", False, None, [NAME_FILE_2], []),
    ("command", False, None, NAME_FILES, RESULT_GET_LIST_FILE_1),
    ("command", False, "items", [NAME_FILE_2], []),
    ("write", False, "items", NAME_FILES, RESULTS_GET_LIST),
    ("test-xcyber360-w", False, "items", NAME_FILES, RESULT_GET_LIST_FILE_1),
    ("test-ossec-w", False, "items", NAME_FILES, RESULT_GET_LIST_FILE_2),
    ("test-xcyber360-w", False, "items", [NAME_FILE_2], []),
    ("command", True, None, NAME_FILES, RESULT_GET_LIST_FILE_2),
    ("test-ossec-w", True, None, NAME_FILES, RESULT_GET_LIST_FILE_1),
    ("command", True, None, [NAME_FILE_2], RESULT_GET_LIST_FILE_2),
    ("command", True, "items", NAME_FILES, RESULT_GET_LIST_FILE_2),
    ("command", True, "items", [NAME_FILE_2], RESULT_GET_LIST_FILE_2),
    ("command", True, "items", [NAME_FILE_1], []),
    ("write", True, "items", NAME_FILES, []),
    ("test-xcyber360-w", True, "items", NAME_FILES, RESULT_GET_LIST_FILE_2),
    ("test-ossec-w", True, "items", NAME_FILES, RESULT_GET_LIST_FILE_1),
    ("test-xcyber360-w", True, "items", [NAME_FILE_2], RESULT_GET_LIST_FILE_2),
])
@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH)
def test_get_lists_search(search_text, complementary_search, search_in_fields, paths, expected_result):
    """Test `get_lists` functionality when using the `search` parameter.

    Parameters
    ----------
    search_text : str
        The text to search.
    complementary_search : bool
        If True, only results NOT containing `search_text` will be returned. If False, only results that contains
        `search_text` will be returned.
    search_in_fields : str
        Name of the field to search in for the `search_text`.
    paths : list of str
        A list of CDB files to read, with their relative path.
    expected_result : list of dict
        The content expected to be returned by `get_lists` when using the specified search parameters.
    """
    result = get_lists(filename=paths, search_text=search_text, complementary_search=complementary_search,
                       search_in_fields=search_in_fields)
    assert isinstance(result, AffectedItemsXcyber360Result)
    assert result.total_affected_items == len(expected_result)
    assert result.affected_items == expected_result


@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH)
def test_get_lists_sort():
    """Test `get_lists` functionality when using the `sort` parameter."""
    result_a = get_lists(filename=NAME_FILES, sort_by=['filename'], sort_ascending=True)
    result_b = get_lists(filename=NAME_FILES, sort_by=['filename'], sort_ascending=False)

    assert isinstance(result_a, AffectedItemsXcyber360Result)
    assert isinstance(result_b, AffectedItemsXcyber360Result)
    assert result_a.affected_items != result_b.affected_items
    assert result_a.affected_items == RESULT_GET_LIST_FILE_1 + RESULT_GET_LIST_FILE_2
    assert result_b.affected_items == RESULT_GET_LIST_FILE_2 + RESULT_GET_LIST_FILE_1


@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH)
@patch('xcyber360.cdb_list.iterate_lists', side_effect=lists_path_mock)
def test_get_path_lists(iterate_mock):
    """Test `get_path_lists` functionality without any other parameter aside from `path`.

    `get_path_lists` works different than `get_lists` as it will read every CDB file from the default path (mocked to
    `DATA_PATH`) and will remove from the result any file that is not in the `path` parameter provided.
    """
    common.reset_context_cache()
    result = get_path_lists(filename=[NAME_FILE_1])

    assert isinstance(result, AffectedItemsXcyber360Result)
    assert result.total_affected_items == len(RESULT_GET_PATH_LIST_FILE_1)
    assert result.affected_items == RESULT_GET_PATH_LIST_FILE_1


@pytest.mark.parametrize("limit", [1, 2])
@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH)
@patch('xcyber360.cdb_list.iterate_lists', side_effect=lists_path_mock)
def test_get_path_lists_limit(iterate_mock, limit):
    """Test `get_path_lists` functionality when using the `limit` parameter.

    Parameters
    ----------
    limit : int
        Maximum number of items to be returned by `get_path_lists`
    """
    common.reset_context_cache()
    result = get_path_lists(filename=NAME_FILES, limit=limit, sort_by=['filename'])

    assert isinstance(result, AffectedItemsXcyber360Result)
    assert result.total_affected_items == TOTAL_LISTS
    assert result.affected_items == RESULTS_GET_PATH_LIST[:limit]


@pytest.mark.parametrize("offset", [0, 1])
@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH)
@patch('xcyber360.cdb_list.iterate_lists', side_effect=lists_path_mock)
def test_get_path_lists_offset(iterate_mock, offset):
    """Test `get__path_lists` functionality when using the `offset` parameter.

    Parameters
    ----------
    offset : int
         Indicates the first item to return.
    """
    common.reset_context_cache()
    result = get_path_lists(filename=NAME_FILES, offset=offset, sort_by=['filename'])

    assert isinstance(result, AffectedItemsXcyber360Result)
    assert result.total_affected_items == TOTAL_LISTS
    assert result.affected_items == RESULTS_GET_PATH_LIST[offset:]


@pytest.mark.parametrize("search_text, complementary_search, search_in_fields, paths, expected_result", [
    ("lists_1", False, None, NAME_FILES, RESULT_GET_PATH_LIST_FILE_1),
    ("lists_2", False, None, NAME_FILES, RESULT_GET_PATH_LIST_FILE_2),
    ("invalid", False, None, NAME_FILES, []),
    ("test_cdb_list", False, "relative_dirname", NAME_FILES, RESULTS_GET_PATH_LIST),
    ("invalid", False, "relative_dirname", NAME_FILES, []),
    ("lists_1", False, "filename", NAME_FILES, RESULT_GET_PATH_LIST_FILE_1),
    ("lists_2", False, "filename", NAME_FILES, RESULT_GET_PATH_LIST_FILE_2),
    ("invalid", False, "filename", NAME_FILES, []),
    ("lists_1", True, None, NAME_FILES, RESULT_GET_PATH_LIST_FILE_2),
    ("lists_2", True, None, NAME_FILES, RESULT_GET_PATH_LIST_FILE_1),
    ("invalid", True, None, NAME_FILES, RESULTS_GET_PATH_LIST),
    ("invalid", True, "relative_dirname", NAME_FILES, RESULTS_GET_PATH_LIST),
    ("lists_1", True, "filename", NAME_FILES, RESULT_GET_PATH_LIST_FILE_2),
    ("lists_2", True, "filename", NAME_FILES, RESULT_GET_PATH_LIST_FILE_1),
    ("invalid", True, "filename", NAME_FILES, RESULTS_GET_PATH_LIST)
])
@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH)
@patch('xcyber360.cdb_list.iterate_lists', side_effect=lists_path_mock)
def test_get_path_lists_search(iterate_mock, search_text, complementary_search, search_in_fields, paths, expected_result):
    """Test `get_path_lists` functionality when using the `search` parameter.

    Parameters
    ----------
    search_text : str
        The text to search.
    complementary_search : bool
        If True, only results NOT containing `search_text` will be returned. If False, only results that contains
        `search_text` will be returned.
    search_in_fields : str
        Name of the field to search in for the `search_text`.
    paths : list of str
        A list of CDB files to read, with their relative path.
    expected_result : list of dict
        The content expected to be returned by `get_lists` when using the specified search parameters.
    """
    common.reset_context_cache()
    result = get_path_lists(filename=paths, search_text=search_text, complementary_search=complementary_search,
                            search_in_fields=search_in_fields, sort_by=['filename'])
    assert isinstance(result, AffectedItemsXcyber360Result)
    assert result.total_affected_items == len(expected_result)
    assert result.affected_items == expected_result


@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH)
@patch('xcyber360.cdb_list.iterate_lists', side_effect=lists_path_mock)
def test_get_path_lists_sort(iterate_mock):
    """Test `get_path_lists` functionality when using the `sort` parameter."""
    result_a = get_path_lists(filename=NAME_FILES, sort_by=['filename'], sort_ascending=True)
    result_b = get_path_lists(filename=NAME_FILES, sort_by=['filename'], sort_ascending=False)

    assert isinstance(result_a, AffectedItemsXcyber360Result)
    assert isinstance(result_b, AffectedItemsXcyber360Result)
    assert result_a.affected_items != result_b.affected_items
    assert result_a.affected_items == RESULT_GET_PATH_LIST_FILE_1 + RESULT_GET_PATH_LIST_FILE_2
    assert result_b.affected_items == RESULT_GET_PATH_LIST_FILE_2 + RESULT_GET_PATH_LIST_FILE_1


@pytest.mark.parametrize("filename, raw, expected_result, total_failed_items", [
    ('test_file', True, 'test-ossec-w:write\ntest-ossec-r:read\ntest-ossec-x:execute\n', 0),
    ('test_file', False, {'test-ossec-w': 'write', 'test-ossec-r': 'read', 'test-ossec-x': 'execute'}, 0),
])
def test_get_list_file(filename, raw, expected_result, total_failed_items):
    """Test that get_list_file calls functions with expected params and it searches filename recursively.

    Parameters
    ----------
    filename : str
        Name of the file to be searched
    raw : bool
        Whether to return content in raw format.
    expected_result : str, dict
        Result that should be returned.
    total_failed_items : int
        Expected number of failed items.
    """
    with patch('xcyber360.cdb_list.get_filenames_paths', return_value=[os.path.join(DATA_PATH, 'test_lists_2')]):
        result = get_list_file([filename], raw)
        if raw:
            assert result == expected_result
        else:
            isinstance(result, AffectedItemsXcyber360Result)
            assert result.render()['data']['total_failed_items'] == total_failed_items
            assert result.render()['data']['affected_items'][0] == expected_result


@patch('xcyber360.cdb_list.safe_move')
@patch('xcyber360.cdb_list.delete_file_with_backup')
@patch('xcyber360.cdb_list.upload_file')
@patch('xcyber360.cdb_list.delete_list_file')
@patch('xcyber360.cdb_list.remove')
@patch('xcyber360.cdb_list.exists', return_value=True)
def test_upload_list_file(mock_exists, mock_remove, mock_delete_list_file, mock_upload_file,
                          mock_delete_file_with_backup, mock_safe_move):
    """Check that functions inside upload_list_file are called with expected params"""
    filename = 'test_file'
    content = 'test_key:test_value\n'
    upload_list_file(filename, content, overwrite=True)

    mock_upload_file.assert_called_once_with(content, os.path.join('etc', 'lists', filename),
                                             check_xml_formula_values=False)
    mock_delete_file_with_backup.assert_called_once_with(os.path.join(common.USER_LISTS_PATH, filename + '.backup'),
                                                         os.path.join(common.USER_LISTS_PATH, filename),
                                                         mock_delete_list_file)


@patch('xcyber360.cdb_list.common.USER_LISTS_PATH', return_value='/test/path')
@patch('xcyber360.cdb_list.remove')
def test_upload_list_file_ko(mock_remove, mock_lists_path):
    """Check whether expected exceptions are raised."""
    result = upload_list_file(filename='test', content='')
    assert isinstance(result, AffectedItemsXcyber360Result)
    assert result.render()['data']['failed_items'][0]['error']['code'] == 1112

    with patch('xcyber360.cdb_list.safe_move') as mock_safe_move:
        with patch('xcyber360.cdb_list.exists', return_value=True):
            # File already exists and overwrite is False, raise exception
            result = upload_list_file(filename='test', content='test:content')
            assert result.render()['data']['failed_items'][0]['error']['code'] == 1905
            # Original file is restored with safe_move
            mock_safe_move.assert_called_once_with('', os.path.join(common.USER_LISTS_PATH, 'test'))

            # File with same name already exists in subdirectory, raise exception
            with patch('xcyber360.cdb_list.get_filenames_paths', return_value=['/test']):
                result = upload_list_file(filename='test', content='test:content', overwrite=True)
                assert result.render()['data']['failed_items'][0]['error']['code'] == 1805

            # Exception while trying to create back up
            result = upload_list_file(filename='test', content='test:content', overwrite=True)
            assert result.render()['data']['failed_items'][0]['error']['code'] == 1019

        # Exception while trying to create list file
        with patch('builtins.open'):
            with patch('xcyber360.cdb_list.exists', return_value=False):
                with patch('tempfile.mkstemp', return_value=['mock_handle', 'mock_tmp_file']):
                    with pytest.raises(Xcyber360InternalError, match=r'\b1005\b'):
                        upload_list_file(filename='test', content='test:content', overwrite=False)


@patch('xcyber360.core.cdb_list.delete_xcyber360_file')
def test_delete_list_file(mock_delete_file):
    """Check that expected result is returned when the file is deleted."""
    try:
        # Create directory for the test
        test_file = os.path.join(DATA_PATH, 'test_file')
        with open(test_file, 'a') as f:
            f.write('key:value\n"ke:y2":value2\n')

        with patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH):
            result = delete_list_file(['test_file'])
            assert result.render()['data']['affected_items'][0] ==\
                   'framework/xcyber360/tests/data/test_cdb_list/test_file'
    finally:
        try:
            os.remove(test_file)
        except Exception:
            pass

    mock_delete_file.assert_called_once_with(test_file)


def test_delete_list_file_ko():
    """Check that expected error code is returned when the file can't be deleted."""
    with patch('xcyber360.cdb_list.common.USER_LISTS_PATH', new=DATA_PATH):
        result = delete_list_file(['test_file'])
        assert result.render()['data']['failed_items'][0]['error']['code'] == 1906
