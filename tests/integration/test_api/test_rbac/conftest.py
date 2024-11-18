"""
Copyright (C) 2015-2024, Xcyber360 Inc.
Created by Xcyber360, Inc. <info@xcyber360.com>.
This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
"""
import pytest

from xcyber360_testing.modules.api.utils import add_resources, relate_resources, remove_resources


@pytest.fixture
def set_security_resources(test_metadata: dict) -> None:
    """Configure the security resources using the API and clean the added resources.

    Args:
        test_metadata (dict): Test metadata.
    """
    remove_resources(test_metadata)
    test_metadata = add_resources(test_metadata)
    relate_resources(test_metadata)

    yield

    remove_resources(test_metadata)
