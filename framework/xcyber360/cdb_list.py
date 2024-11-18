

from os import remove
from os.path import join, split, exists, isfile, dirname as path_dirname

from xcyber360.core import common
from xcyber360.core.cdb_list import iterate_lists, get_list_from_file, REQUIRED_FIELDS, SORT_FIELDS, delete_list, \
    get_filenames_paths, validate_cdb_list, LIST_FIELDS
from xcyber360.core.exception import Xcyber360Error
from xcyber360.core.results import AffectedItemsXcyber360Result
from xcyber360.core.utils import process_array, safe_move, delete_file_with_backup, upload_file, to_relative_path
from xcyber360.rbac.decorators import expose_resources


@expose_resources(actions=['lists:read'], resources=['list:file:{filename}'])
def get_lists(filename: list = None, offset: int = 0, limit: int = common.DATABASE_LIMIT, select: list = None,
              sort_by: dict = None, sort_ascending: bool = True, search_text: str = None,
              complementary_search: bool = False, search_in_fields: str = None,
              relative_dirname: str = None, q: str = None, distinct: bool = False) -> AffectedItemsXcyber360Result:
    """Get CDB lists content.

    Parameters
    ----------
    filename : list
        Filenames to filter by.
    offset : int
        First item to return.
    limit : int
        Maximum number of items to return. Default: common.DATABASE_LIMIT
    select : list
        List of selected fields to return.
    sort_by : dict
        Fields to sort the items by. Format: {"fields":["field1","field2"],"order":"asc|desc"}
    sort_ascending : bool
        Sort in ascending (true) or descending (false) order.
    search_text : str
        Find items with the specified string.
    complementary_search : bool
        If True, only results NOT containing `search_text` will be returned. If False, only results that contains
        `search_text` will be returned.
    search_in_fields : str
        Name of the field to search in for the `search_text`.
    relative_dirname : str
         Filter by relative dirname.
    q : str
        Query to filter results by.
    distinct : bool
        Look for distinct values.

    Returns
    -------
    AffectedItemsXcyber360Result
        Lists content.
    """
    result = AffectedItemsXcyber360Result(all_msg='All specified lists were returned',
                                      some_msg='Some lists were not returned',
                                      none_msg='No list was returned')
    dirname = join(common.XCYBER360_PATH, relative_dirname) if relative_dirname else None

    lists = list()
    for path in get_filenames_paths(filename):
        # Only files which exist and whose dirname is the one specified by the user (if any), will be added to response.
        if not any([dirname is not None and path_dirname(path) != dirname, not isfile(path)]):
            lists.append({'items': [{'key': key, 'value': value} for key, value in get_list_from_file(path).items()],
                          'relative_dirname': path_dirname(to_relative_path(path)),
                          'filename': split(to_relative_path(path))[1]})

    data = process_array(lists, search_text=search_text, search_in_fields=search_in_fields,
                         complementary_search=complementary_search, sort_by=sort_by, sort_ascending=sort_ascending,
                         offset=offset, limit=limit, select=select, allowed_sort_fields=SORT_FIELDS,
                         required_fields=REQUIRED_FIELDS, allowed_select_fields=LIST_FIELDS, q=q, distinct=distinct)
    result.affected_items = data['items']
    result.total_affected_items = data['totalItems']

    return result


@expose_resources(actions=['lists:read'], resources=['list:file:{filename}'])
def get_list_file(filename: list = None, raw: bool = None) -> AffectedItemsXcyber360Result:
    """Get a CDB list file content. The file is recursively searched.

    Parameters
    ----------
    filename : list
        Full path of CDB list file to get.
    raw : bool, optional
        Respond in raw format.

    Returns
    -------
    AffectedItemsXcyber360Result
        CDB list content.
    """
    result = AffectedItemsXcyber360Result(all_msg='CDB list was returned',
                                      none_msg='No list was returned')

    try:
        # Recursively search for filename inside {xcyber360_path}/etc/lists/
        content = get_list_from_file(get_filenames_paths(filename)[0], raw)
        if raw:
            result = content
        else:
            result.affected_items.append(content)
            result.total_affected_items = 1
    except Xcyber360Error as e:
        result.add_failed_item(id_=filename[0], error=e)

    return result


@expose_resources(actions=['lists:update'], resources=['*:*:*'])
def upload_list_file(filename: str = None, content: str = None, overwrite: bool = False) -> AffectedItemsXcyber360Result:
    """Upload a new list file.

    Parameters
    ----------
    filename : str
        Destination path of the new file.
    content : str
        Content of file to be uploaded.
    overwrite : bool
        True for updating existing files, false otherwise.

    Returns
    -------
    AffectedItemsXcyber360Result
        Confirmation message.
    """
    result = AffectedItemsXcyber360Result(all_msg='CDB list file uploaded successfully',
                                      none_msg='Could not upload CDB list file')
    full_path = join(common.USER_LISTS_PATH, filename)
    backup_file = ''

    try:
        # Raise Xcyber360Error if CDB list is not valid
        validate_cdb_list(content)

        # If file already exists and overwrite is False, raise exception.
        if not overwrite and exists(full_path):
            raise Xcyber360Error(1905)
        # If file with same name already exists in subdirectory.
        elif get_filenames_paths([filename])[0] != full_path:
            raise Xcyber360Error(1805)
        # Create backup and delete original CDB list.
        elif overwrite and exists(full_path):
            backup_file = f"{full_path}.backup"
            delete_file_with_backup(backup_file, full_path, delete_list_file)

        upload_file(content, to_relative_path(full_path), check_xml_formula_values=False)
        result.affected_items.append(to_relative_path(full_path))
        result.total_affected_items = len(result.affected_items)
        # Remove back up file if no exceptions were raised.
        exists(backup_file) and remove(backup_file)
    except Xcyber360Error as e:
        result.add_failed_item(id_=to_relative_path(full_path), error=e)
    finally:
        # If backup file was not deleted (any exception was raised), it should be restored.
        exists(backup_file) and safe_move(backup_file, full_path)

    return result


@expose_resources(actions=['lists:delete'], resources=['list:file:{filename}'])
def delete_list_file(filename: list) -> AffectedItemsXcyber360Result:
    """Delete a CDB list file.

    Parameters
    ----------
    filename : list
        Destination path of the new file.

    Returns
    -------
    AffectedItemsXcyber360Result
        Confirmation message.
    """
    result = AffectedItemsXcyber360Result(all_msg='CDB list file was successfully deleted',
                                      none_msg='Could not delete CDB list file')
    full_path = join(common.USER_LISTS_PATH, filename[0])

    try:
        delete_list(to_relative_path(full_path))
        result.affected_items.append(to_relative_path(full_path))
    except Xcyber360Error as e:
        result.add_failed_item(id_=to_relative_path(full_path), error=e)
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=['lists:read'], resources=['list:file:{filename}'])
def get_path_lists(filename: list = None, offset: int = 0, limit: int = common.DATABASE_LIMIT, sort_by: dict = None,
                   sort_ascending: bool = True, search_text: str = None, complementary_search: bool = False,
                   search_in_fields: str = None, relative_dirname: str = None) -> AffectedItemsXcyber360Result:
    """Get paths of all CDB lists.

    Parameters
    ----------
    filename : list
        List of filenames to filter by.
    offset : int
        First item to return.
    limit : int
        Maximum number of items to return.
    sort_by : dict
        Fields to sort the items by. Format: {"fields":["field1","field2"],"order":"asc|desc"}
    sort_ascending : bool
        Sort in ascending (true) or descending (false) order.
    search_text : str
        Find items with the specified string.
    complementary_search : bool
        If True, only results NOT containing `search_text` will be returned. If False, only results that contains
        `search_text` will be returned.
    search_in_fields : str
        Name of the field to search in for the `search_text`.
    relative_dirname : str
         Filter by relative dirname.

    Returns
    -------
    AffectedItemsXcyber360Result
        Paths of all CDB lists.
    """
    result = AffectedItemsXcyber360Result(all_msg='All specified paths were returned',
                                      some_msg='Some paths were not returned',
                                      none_msg='No path was returned')

    paths = get_filenames_paths(filename)
    lists = iterate_lists(only_names=True)
    for item in list(lists):
        if any([relative_dirname is not None and item['relative_dirname'] != relative_dirname,
                join(common.XCYBER360_PATH, item['relative_dirname'], item['filename']) not in paths]):
            lists.remove(item)

    data = process_array(lists, search_text=search_text, search_in_fields=search_in_fields,
                         complementary_search=complementary_search, sort_by=sort_by, sort_ascending=sort_ascending,
                         offset=offset, limit=limit)
    result.affected_items = data['items']
    result.total_affected_items = data['totalItems']

    return result
