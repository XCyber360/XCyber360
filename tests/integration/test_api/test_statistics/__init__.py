"""
Copyright (C) 2015-2024, Xcyber360 Inc.
Created by Xcyber360, Inc. <info@xcyber360.com>.
This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
"""
from pathlib import Path


# Constants & base paths
TEST_DATA_PATH = Path(Path(__file__).parent, 'data')
CONFIGURATION_FOLDER_PATH = Path(TEST_DATA_PATH, 'configuration_templates')
TEST_CASES_FOLDER_PATH = Path(TEST_DATA_PATH, 'test_cases')
