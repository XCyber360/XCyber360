"""
Module to wrapp the Xcyber360 API requests. Normally, the developers should not use this class but Xcyber360API one. This class
is used by Xcyber360API to make and send the API requests.

This module contains the following:

- Xcyber360APIRequest:
    - send
"""
import json
import requests

from xcyber360_qa_framework.generic_modules.request.request import Request
from xcyber360_qa_framework.generic_modules.exceptions.exceptions import ConnectionError
from xcyber360_qa_framework.xcyber360_components.api.xcyber360_api_response import Xcyber360APIResponse


class Xcyber360APIRequest:
    """Wrapper class to manage requests to the Xcyber360 API.

    Args:
        endpoint (str): Target API endpoint.
        method (str): Request method (GET, POST, PUT, DELETE).
        payload (dict): Request data.
        headers (dict): Request headers.
        verify (boolean): False for ignore making insecure requests, False otherwise.

    Attributes:
        endpoint (str): Target API endpoint.
        method (str): Request method (GET, POST, PUT, DELETE).
        payload (dict): Request data.
        headers (dict): Request headers.
        verify (boolean): False for ignore making insecure requests, False otherwise.
    """
    def __init__(self, endpoint, method, payload=None, headers=None, verify=False):
        self.endpoint = endpoint
        self.method = method.upper()
        self.payload = payload
        self.headers = headers
        self.verify = verify

    def __get_request_parameters(self, xcyber360_api_object):
        """Build the request parameters.

        Args:
            xcyber360_api_object (Xcyber360API): Xcyber360 API object.
        """
        # Get the token if we have not got it before.
        if xcyber360_api_object.token is None:
            xcyber360_api_object.token = xcyber360_api_object.get_token()

        self.headers = {} if self.headers is None else self.headers
        self.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {xcyber360_api_object.token}'
        })

        request_args = {
            'method': self.method,
            'url': f"{xcyber360_api_object.url}{self.endpoint}",
            'headers': self.headers,
            'verify': self.verify
        }

        if self.payload is not None:
            request_args['payload'] = self.payload

        return request_args

    def __call__(self, func):
        """Perform directly the Xcyber360 API call and add the response object to the function parameters. Useful to run
        the request using only a python decorator.

        Args:
            func (function): Function object.
        """
        def wrapper(obj, *args, **kwargs):
            kwargs['response'] = self.send(obj)

            return func(obj, *args, **kwargs)

        return wrapper

    def __str__(self):
        """Overwrite the print object representation"""
        return json.dumps(self.__dict__)

    def send(self, xcyber360_api_object):
        """Send the API request.

        Args:
            xcyber360_api_object (Xcyber360API): Xcyber360 API object.

        Returns:
            Xcyber360APIResponse: Xcyber360 API response object.

        Raises:
            exceptions.RuntimeError: Cannot establish connection with the API.
        """
        request_parameters = self.__get_request_parameters(xcyber360_api_object)

        try:
            return Xcyber360APIResponse(Request(**request_parameters).send())
        except requests.exceptions.ConnectionError as exception:
            raise ConnectionError(f"Cannot establish connection with {xcyber360_api_object.url}") from exception
