#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module contains tools for processing events from a Google Cloud subscription."""  # noqa: E501

import logging
import socket
from sys import path
from os.path import dirname, abspath
path.insert(0, dirname(dirname(abspath(__file__))))
import exceptions
from utils import ANALYSISD, MAX_EVENT_SIZE


class Xcyber360GCloudIntegration:
    """Class for sending events from Google Cloud to Xcyber360."""

    header = '1:Xcyber360-GCloud:'
    key_name = 'gcp'

    def __init__(self, logger: logging.Logger):
        """Instantiate a Xcyber360GCloudIntegration object.

        Parameters
        ----------
        logger: logging.Logger
            The logger that will be used to send messages to stdout.
        """
        self.logger = logger
        self.socket = None

    def check_permissions(self):
        raise NotImplementedError

    def format_msg(self, msg: str) -> str:
        """Format a message.

        Parameters
        ----------
        msg : str
            Message to be formatted.

        Returns
        -------
        str
            The formatted message.
        """
        # Insert msg as value of self.key_name key.
        return f'{{"integration": "gcp", "{self.key_name}": {msg}}}'

    def initialize_socket(self):
        """Initialize a socket and connect it to an address.

        Returns
        -------
        socket
            The initialized socket to be able to use it as a context manager.

        Raises
        ------
        exceptions.Xcyber360IntegrationInternalError
            If the socket is unable to establish a connection or send a message
             to analysisd.
        """
        try:
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self.socket.connect(ANALYSISD)
            return self.socket
        except ConnectionRefusedError:
            raise exceptions.Xcyber360IntegrationInternalError(1)
        except OSError:
            raise exceptions.Xcyber360IntegrationInternalError(2, socket_path=ANALYSISD)

    def process_data(self):
        raise NotImplementedError

    def send_msg(self, msg: str):
        """Send an event to the Xcyber360 queue.

        Parameters
        ----------
        msg : str
            Event to be sent.

        Raises
        ------
        exceptions.Xcyber360IntegrationInternalError
            If the socket is unable to send the message to analysisd.
        """
        event_json = f'{self.header}{msg}'.encode(errors='replace')

        # Logs warning if event is bigger than max size
        if len(event_json) > MAX_EVENT_SIZE:
            logging.warning(f"WARNING: Event size exceeds the maximum allowed limit of {MAX_EVENT_SIZE} bytes.")

        self.logger.debug(f'Sending msg to analysisd: "{event_json}"')
        try:
            self.socket.send(event_json)
        except OSError:
            raise exceptions.Xcyber360IntegrationInternalError(3)
