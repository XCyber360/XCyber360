

from xcyber360.core import active_response, common
from xcyber360.core.agent import get_agents_info
from xcyber360.core.exception import Xcyber360Exception, Xcyber360Error, Xcyber360ResourceNotFound
from xcyber360.core.xcyber360_queue import Xcyber360Queue
from xcyber360.core.results import AffectedItemsXcyber360Result
from xcyber360.rbac.decorators import expose_resources


@expose_resources(actions=['active-response:command'], resources=['agent:id:{agent_list}'],
                  post_proc_kwargs={'exclude_codes': [1701]})
def run_command(agent_list: list = None, command: str = '', arguments: list = None,
                alert: dict = None) -> AffectedItemsXcyber360Result:
    """Run AR command in a specific agent.

    Parameters
    ----------
    agent_list : list
        Agents list that will run the AR command.
    command : str
        Command running in the agents. If this value starts with !, then it refers to a script name instead of a
        command name.
    custom : bool
        Whether the specified command is a custom command or not.
    arguments : list
        Command arguments.
    alert : dict
        Alert information depending on the AR executed.

    Returns
    -------
    AffectedItemsXcyber360Result
        Affected items.
    """
    result = AffectedItemsXcyber360Result(all_msg='AR command was sent to all agents',
                                      some_msg='AR command was not sent to some agents',
                                      none_msg='AR command was not sent to any agent'
                                      )
    if agent_list:
        with Xcyber360Queue(common.AR_SOCKET) as wq:
            system_agents = get_agents_info()
            for agent_id in agent_list:
                try:
                    if agent_id not in system_agents:
                        raise Xcyber360ResourceNotFound(1701)
                    active_response.send_ar_message(agent_id, wq, command, arguments, alert)
                    result.affected_items.append(agent_id)
                    result.total_affected_items += 1
                except Xcyber360Exception as e:
                    result.add_failed_item(id_=agent_id, error=e)
            result.affected_items.sort(key=int)

    return result
