

import copy
import os
import sys
from datetime import datetime
from unittest.mock import MagicMock, patch
import pytest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'))
import aws_utils as utils
import aws_constants as test_constants

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
import xcyber360_integration
import constants

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'services'))
import aws_service

TEST_DATETIME = datetime.now()
TEST_DATETIME_STR = datetime.strftime(TEST_DATETIME, '%Y-%m-%dT%H:%M:%SZ')


@patch('xcyber360_integration.Xcyber360Integration.get_sts_client')
@patch('xcyber360_integration.Xcyber360AWSDatabase.check_metadata_version')
@patch('xcyber360_integration.sqlite3.connect')
@patch('xcyber360_integration.Xcyber360Integration.get_client')
@patch('xcyber360_integration.utils.find_xcyber360_path', return_value=test_constants.TEST_XCYBER360_PATH)
@patch('xcyber360_integration.utils.get_xcyber360_version')
@patch('xcyber360_integration.Xcyber360Integration.__init__', side_effect=xcyber360_integration.Xcyber360Integration.__init__)
def test_aws_service_initializes_properly(mock_xcyber360_integration, mock_version, mock_path, mock_client, mock_connect,
                                         mock_metadata, mock_sts):
    """Test if the instances of 'AWSService' are created properly."""
    mock_client = MagicMock()
    mock_sts.return_value = mock_client
    kwargs = utils.get_aws_service_parameters(db_table_name=test_constants.TEST_TABLE_NAME,
                                              service_name=test_constants.TEST_SERVICE_NAME, reparse=True,
                                              profile=test_constants.TEST_AWS_PROFILE, iam_role_arn=test_constants.TEST_IAM_ROLE_ARN,
                                              only_logs_after=test_constants.TEST_ONLY_LOGS_AFTER,
                                              account_alias=test_constants.TEST_ACCOUNT_ALIAS,
                                              region=test_constants.TEST_REGION,
                                              discard_field=test_constants.TEST_DISCARD_FIELD,
                                              discard_regex=test_constants.TEST_DISCARD_REGEX,
                                              sts_endpoint=test_constants.TEST_STS_ENDPOINT,
                                              service_endpoint=test_constants.TEST_SERVICE_ENDPOINT,
                                              iam_role_duration=test_constants.TEST_IAM_ROLE_DURATION)
    instance = aws_service.AWSService(**kwargs)
    mock_xcyber360_integration.assert_called_with(instance, service_name=test_constants.TEST_SERVICE_NAME,
                                              profile=kwargs["profile"], iam_role_arn=kwargs["iam_role_arn"],
                                              region=kwargs["region"], discard_field=kwargs["discard_field"],
                                              discard_regex=kwargs["discard_regex"],
                                              sts_endpoint=kwargs["sts_endpoint"],
                                              service_endpoint=kwargs["service_endpoint"],
                                              iam_role_duration=kwargs["iam_role_duration"], external_id=None,
                                              skip_on_error=False)
    assert instance.service_name == test_constants.TEST_SERVICE_NAME
    assert instance.reparse
    assert instance.region == test_constants.TEST_REGION
    assert instance.only_logs_after == test_constants.TEST_ONLY_LOGS_AFTER
    mock_sts.assert_called_with(kwargs["profile"])
    mock_client.get_caller_identity.assert_called_once()


def test_aws_service_check_region():
    """Test 'check_region' function raises exception when an incorrect region is passed."""
    with pytest.raises(ValueError) as e:
        aws_service.AWSService.check_region('no-region')


@patch('xcyber360_integration.Xcyber360Integration.get_sts_client')
@patch('xcyber360_integration.Xcyber360AWSDatabase.__init__')
@patch('xcyber360_integration.Xcyber360Integration.__init__', side_effect=xcyber360_integration.Xcyber360Integration.__init__)
def test_aws_service_get_last_log_date(mock_xcyber360_integration, mock_xcyber360_aws_database, mock_sts):
    """Test 'get_last_log_date' function returns a date with the expected format."""
    instance = utils.get_mocked_service(only_logs_after=test_constants.TEST_ONLY_LOGS_AFTER)
    assert instance.get_last_log_date() == test_constants.TEST_ONLY_LOGS_AFTER_WITH_FORMAT


@patch('xcyber360_integration.Xcyber360Integration.get_sts_client')
@patch('xcyber360_integration.Xcyber360AWSDatabase.__init__')
@patch('xcyber360_integration.Xcyber360Integration.__init__', side_effect=xcyber360_integration.Xcyber360Integration.__init__)
def test_aws_service_format_message(mock_xcyber360_integration, mock_xcyber360_aws_database, mock_sts):
    """Test 'format_message' function updates the expected fields of an event."""
    input_msg = {'service': 'service_name', 'createdAt': TEST_DATETIME, 'updatedAt': TEST_DATETIME, 'key': 'value'}
    output_msg = {'source': 'service_name', 'createdAt': TEST_DATETIME_STR, 'updatedAt': TEST_DATETIME_STR,
                  'key': 'value'}
    instance = utils.get_mocked_service(only_logs_after=test_constants.TEST_ONLY_LOGS_AFTER)
    expected_msg = copy.deepcopy(constants.AWS_SERVICE_MSG_TEMPLATE)
    expected_msg['aws'] = output_msg
    assert instance.format_message(input_msg) == expected_msg
