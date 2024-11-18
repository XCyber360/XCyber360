#!/usr/bin/env python


from unittest.mock import patch

import pytest

from xcyber360.tests.util import InitWDBSocketMock

with patch('xcyber360.core.common.xcyber360_uid'):
    with patch('xcyber360.core.common.xcyber360_gid'):
        from xcyber360.core.mitre import *


@patch('xcyber360.core.utils.Xcyber360DBConnection', return_value=InitWDBSocketMock(sql_schema_file='schema_mitre_test.sql'))
def test_Xcyber360DBQueryMitreMetadata(mock_wdb):
    """Verify that the method connects correctly to the database and returns the correct type."""
    db_query = Xcyber360DBQueryMitreMetadata()
    data = db_query.run()

    assert isinstance(db_query, Xcyber360DBQueryMitre) and isinstance(data, dict)


@pytest.mark.parametrize('wdb_query_class', [
    Xcyber360DBQueryMitreGroups,
    Xcyber360DBQueryMitreMitigations,
    Xcyber360DBQueryMitreReferences,
    Xcyber360DBQueryMitreTactics,
    Xcyber360DBQueryMitreTechniques,
    Xcyber360DBQueryMitreSoftware

])
@patch('xcyber360.core.utils.Xcyber360DBConnection', return_value=InitWDBSocketMock(sql_schema_file='schema_mitre_test.sql'))
def test_Xcyber360DBQueryMitre_classes(mock_wdb, wdb_query_class):
    """Verify that the method connects correctly to the database and returns the correct types."""
    db_query = wdb_query_class()
    data = db_query.run()

    assert isinstance(db_query, Xcyber360DBQueryMitre) and isinstance(data, dict)

    # All items have all the related_items (relation_fields) and their type is list
    try:
        assert all(
            isinstance(data_item[related_item], list) for related_item in db_query.relation_fields for data_item in
            data['items'])
    except KeyError:
        pytest.fail("Related item not found in data obtained from query")


@pytest.mark.parametrize('mitre_wdb_query_class', [
    Xcyber360DBQueryMitreGroups,
    Xcyber360DBQueryMitreMitigations,
    Xcyber360DBQueryMitreReferences,
    Xcyber360DBQueryMitreTactics,
    Xcyber360DBQueryMitreTechniques,
    Xcyber360DBQueryMitreSoftware
])
@patch('xcyber360.core.utils.Xcyber360DBConnection')
def test_get_mitre_items(mock_wdb, mitre_wdb_query_class):
    """Test get_mitre_items function."""
    info, data = get_mitre_items(mitre_wdb_query_class)

    db_query_to_compare = mitre_wdb_query_class()

    assert isinstance(info['allowed_fields'], set) and info['allowed_fields'] == set(
        db_query_to_compare.fields.keys()).union(
        db_query_to_compare.relation_fields).union(db_query_to_compare.extra_fields)
    assert isinstance(info['min_select_fields'], set) and info[
        'min_select_fields'] == db_query_to_compare.min_select_fields
