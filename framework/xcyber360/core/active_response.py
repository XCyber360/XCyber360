

import json

from xcyber360.core import common
from xcyber360.core.agent import Agent
from xcyber360.core.cluster.cluster import get_node
from xcyber360.core.exception import Xcyber360Error
from xcyber360.core.utils import Xcyber360Version
from xcyber360.core.xcyber360_queue import Xcyber360Queue
from xcyber360.core.xcyber360_socket import create_xcyber360_socket_message


def get_commands() -> list:
    """Get the available commands.

    Returns
    -------
    list
        List with the available commands.
    """
    commands = list()
    with open(common.AR_CONF) as f:
        for line in f:
            cmd = line.split(" - ")[0]
            commands.append(cmd)

    return commands


def shell_escape(command: str) -> str:
    """Escape some characters in the command before sending it.

    Parameters
    ----------
    command : str
        Command running in the agent. If this value starts with !, then it refers to a script name instead of a
        command name.

    Returns
    -------
    str
        Command with escape characters.
    """
    shell_escapes = \
        ['"', '\'', '\t', ';', '`', '>', '<', '|', '#', '*', '[', ']', '{', '}', '&', '$', '!', ':', '(', ')']
    for shell_esc_char in shell_escapes:
        command = command.replace(shell_esc_char, "\\" + shell_esc_char)

    return command


class ARMessageBuilder:
    @staticmethod
    def can_handle(agent_version: str) -> bool:
        """Check if the message builder can handle the given agent version.

        Parameters
        ----------
        agent_version : str
            The version of the agent.

        Returns
        -------
        bool
            True if the message builder can handle the agent version, False otherwise.
        """
        raise NotImplementedError

    def create_message(self, command: str = '', arguments: list = None, alert: dict = None) -> str:
        """Create the message with the Active Response format that will be sent to the socket.

        Parameters
        ----------
        command : str
            Command running in the agent. If this value starts with !, then it refers to a script name instead of a
            command name.
        arguments : list
            Command arguments.
        alert : dict
            Alert data that will be sent with the AR command.

        Returns
        -------
        str
            Message that will be sent to the socket.
        """
        raise NotImplementedError

    @classmethod
    def choose_builder(cls, agent_version: str):
        """Choose the appropriate message builder based on the agent version.

        Parameters
        ----------
        agent_version : str
            The version of the agent.

        Returns
        -------
        ARMessageBuilder
            An instance of the chosen message builder.

        Raises
        ------
        Xcyber360Error(1000)
            If no suitable message builder is found for the agent version.
        """

        for subclass in cls.__subclasses__():
            if subclass.can_handle(agent_version):
                return subclass()

        raise Xcyber360Error(1000, "No suitable message builder found for agent version: {}".format(agent_version))

    def validate_command(self, command: str):
        """Validate the command for Active Response.

        Parameters
        ----------
        command : str
            Command running in the agent. If this value starts with !, then it refers to a script name instead of a command
            name.

        Raises
        ------
        Xcyber360Error(1650)
            If the command is not specified.
        Xcyber360Error(1652)
            If the command is not custom and the command is not one of the available commands.
        """
        if not command:
            raise Xcyber360Error(1650)

        if not command.startswith('!'):
            commands = get_commands()
            if command not in commands:
                raise Xcyber360Error(1652)


class ARStrMessage(ARMessageBuilder):
    @staticmethod
    def can_handle(agent_version: str) -> bool:
        """Check if the ARStrMessage can handle the given agent version.

        Parameters
        ----------
        agent_version : str
            The version of the agent.

        Returns
        -------
        bool
            True if ARStrMessage can handle the agent version, False otherwise.
        """
        return Xcyber360Version(agent_version) < Xcyber360Version(common.AR_LEGACY_VERSION)

    def create_message(self, command: str = '', arguments: list = None, alert: dict = None) -> str:
        """Create the message with the Active Response format that will be sent to the socket.

        Parameters
        ----------
        command : str
            Command running in the agent. If this value starts with !, then it refers to a script name instead of a command
            name.
        arguments : list
            Command arguments.
        alert : dict
            Alert data that will be sent with the AR command.

        Raises
        ------
        Xcyber360Error(1650)
            If the command is not specified.
        Xcyber360Error(1652)
            If the command is not custom and the command is not one of the available commands.

        Returns
        -------
        str
            Message that will be sent to the socket.
        """
        self.validate_command(command)

        msg_queue = command
        msg_queue += " " + " ".join(shell_escape(str(x)) for x in arguments) if arguments else " - -"

        return msg_queue


class ARJsonMessage(ARMessageBuilder):
    @staticmethod
    def can_handle(agent_version: str) -> bool:
        """Check if the ARJsonMessage can handle the given agent version.

        Parameters
        ----------
        agent_version : str
            The version of the agent.

        Returns
        -------
        bool
            True if ARJsonMessage can handle the agent version, False otherwise.
        """
        return Xcyber360Version(agent_version) >= Xcyber360Version(common.AR_LEGACY_VERSION)

    def create_message(self, command: str = '', arguments: list = None, alert: dict = None) -> str:
        """Create the message with the Active Response format that will be sent to the socket.

        Parameters
        ----------
        command : str
            Command running in the agent. If this value starts by !, then it refers to a script name instead of a command
            name.
        arguments : list
            Command arguments.
        alert : dict
            Alert data that will be sent with the AR command.

        Raises
        ------
        Xcyber360Error(1650)
            If the command is not specified.
        Xcyber360Error(1652)
            If the command is not custom and the command is not one of the available commands.

        Returns
        -------
        str
            Message that will be sent to the socket.
        """
        self.validate_command(command)

        msg_queue = json.dumps(
            create_xcyber360_socket_message(origin={'name': get_node().get('node'), 'module': common.origin_module.get()},
                                        command=command,
                                        parameters={'extra_args': arguments if arguments else [],
                                                    'alert': alert if alert else {}}))

        return msg_queue


def send_ar_message(agent_id: str = '', wq: Xcyber360Queue = None, command: str = '', arguments: list = None,
                    alert: dict = None) -> None:
    """Send the active response message to the agent.

    Parameters
    ----------
    agent_id : str
        ID specifying the agent where the msg_queue will be sent to.
    wq : Xcyber360Queue
        Used for the active response messages.
    command : str
        Command running in the agents. If this value starts with !, then it refers to a script name instead of a
        command name.
    arguments : list
        Command arguments.
    alert : dict
        Alert information depending on the AR executed.

    Raises
    ------
    Xcyber360Error(1707)
        If the agent with ID agent_id is not active.
    Xcyber360Error(1750)
        If active response is disabled in the specified agent.
    """
    # Agent basic information
    agent_info = Agent(agent_id).get_basic_information()

    # Check if agent is active
    if agent_info['status'].lower() != 'active':
        raise Xcyber360Error(1707)

    # Once we know the agent is active, store version
    agent_version = agent_info['version']

    # Check if AR is enabled
    agent_conf = Agent(agent_id).get_config('com', 'active-response', agent_version)
    if agent_conf['active-response']['disabled'] == 'yes':
        raise Xcyber360Error(1750)

    # Create classic msg or JSON msg depending on the agent version
    message_builder = ARMessageBuilder.choose_builder(agent_version)
    msg_queue = message_builder.create_message(command=command, arguments=arguments, alert=alert)

    wq.send_msg_to_agent(msg=msg_queue, agent_id=agent_id, msg_type=Xcyber360Queue.AR_TYPE)



