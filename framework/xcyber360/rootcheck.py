

from xcyber360 import common
from xcyber360.core.agent import get_agents_info, get_rbac_filters, Xcyber360DBQueryAgents
from xcyber360.core.exception import Xcyber360Error, Xcyber360ResourceNotFound
from xcyber360.core.results import AffectedItemsXcyber360Result
from xcyber360.core.rootcheck import Xcyber360DBQueryRootcheck, last_scan, rootcheck_delete_agent
from xcyber360.core.xcyber360_queue import Xcyber360Queue
from xcyber360.core.wdb import Xcyber360DBConnection
from xcyber360.rbac.decorators import expose_resources


@expose_resources(actions=["rootcheck:run"], resources=["agent:id:{agent_list}"],
                  post_proc_kwargs={'exclude_codes': [1701, 1707]})
def run(agent_list: list = None) -> AffectedItemsXcyber360Result:
    """Run a rootcheck scan in the specified agents.

    Parameters
    ----------
    agent_list : list
         List of the agents IDs to run the scan for.

    Returns
    -------
    AffectedItemsXcyber360Result
        JSON containing the affected agents.
    """
    result = AffectedItemsXcyber360Result(all_msg='Rootcheck scan was restarted on returned agents',
                                      some_msg='Rootcheck scan was not restarted on some agents',
                                      none_msg='No rootcheck scan was restarted')

    system_agents = get_agents_info()
    rbac_filters = get_rbac_filters(system_resources=system_agents, permitted_resources=agent_list)
    agent_list = set(agent_list)
    not_found_agents = agent_list - system_agents

    # Add non existent agents to failed_items
    [result.add_failed_item(id_=agent, error=Xcyber360ResourceNotFound(1701)) for agent in not_found_agents]

    # Add non eligible agents to failed_items
    with Xcyber360DBQueryAgents(limit=None, select=["id", "status"], query=f'status!=active', **rbac_filters) as db_query:
        non_eligible_agents = db_query.run()['items']

    [result.add_failed_item(
        id_=agent['id'],
        error=Xcyber360Error(1707)) for agent in non_eligible_agents]

    with Xcyber360Queue(common.AR_SOCKET) as wq:
        eligible_agents = agent_list - not_found_agents - {d['id'] for d in non_eligible_agents}
        for agent_id in eligible_agents:
            try:
                wq.send_msg_to_agent(Xcyber360Queue.HC_SK_RESTART, agent_id)
                result.affected_items.append(agent_id)
            except Xcyber360Error as e:
                result.add_failed_item(id_=agent_id, error=e)

    result.affected_items.sort(key=int)
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=["rootcheck:clear"], resources=["agent:id:{agent_list}"])
def clear(agent_list: list = None) -> AffectedItemsXcyber360Result:
    """Clear the rootcheck database for a list of agents.

    Parameters
    ----------
    agent_list : list
        List of agent ids.

    Returns
    -------
    AffectedItemsXcyber360Result
        JSON containing the affected agents.
    """
    result = AffectedItemsXcyber360Result(all_msg='Rootcheck database was cleared on returned agents',
                                      some_msg='Rootcheck database was not cleared on some agents',
                                      none_msg="No rootcheck database was cleared")

    wdb_conn = Xcyber360DBConnection()
    system_agents = get_agents_info()
    agent_list = set(agent_list)
    not_found_agents = agent_list - system_agents
    # Add non existent agents to failed_items
    [result.add_failed_item(id_=agent_id, error=Xcyber360ResourceNotFound(1701)) for agent_id in not_found_agents]

    eligible_agents = agent_list - not_found_agents
    for agent_id in eligible_agents:
        try:
            rootcheck_delete_agent(agent_id, wdb_conn)
            result.affected_items.append(agent_id)
        except Xcyber360Error as e:
            result.add_failed_item(id_=agent_id, error=e)

    result.affected_items.sort(key=int)
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=["rootcheck:read"], resources=["agent:id:{agent_list}"])
def get_last_scan(agent_list: list) -> AffectedItemsXcyber360Result:
    """Get the last rootcheck scan of an agent.

    Parameters
    ----------
    agent_list : list
        List with the agent ID to get the last scan date from.

    Returns
    -------
    AffectedItemsXcyber360Result
        JSON containing the scan date.
    """
    result = AffectedItemsXcyber360Result(all_msg='Last rootcheck scan of the agent was returned',
                                      none_msg='No last scan information was returned')

    result.affected_items.append(last_scan(agent_list[0]))
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=["rootcheck:read"], resources=["agent:id:{agent_list}"])
def get_rootcheck_agent(agent_list: list = None, offset: int = 0, limit: int = common.DATABASE_LIMIT, sort: str = None,
                        search: str = None, select: str = None, filters: dict = None, q: str = '',
                        distinct: bool = False) -> AffectedItemsXcyber360Result:
    """Return a list of events from the rootcheck database.

    Parameters
    ----------
    agent_list : list
        Agent ID to get the rootcheck events from.
    offset : int
        First element to return in the collection.
    limit : int
        Maximum number of elements to return.
    sort : str
        Sort the collection by a field or fields (separated by comma). Use +/- at the beginning to list in
        ascending or descending order.
    search : str
        Look for elements with the specified string.
    select : str
        Select which fields to return (separated by comma).
    q : str
        Query to filter results by.
    distinct : bool
        Look for distinct values.
    filters : dict
        Fields to filter by.

    Returns
    -------
    AffectedItemsXcyber360Result
        JSON containing the rootcheck events.
    """
    if filters is None:
        filters = {}
    result = AffectedItemsXcyber360Result(all_msg='All selected rootcheck information was returned',
                                      some_msg='Some rootcheck information was not returned',
                                      none_msg='No rootcheck information was returned'
                                      )

    with Xcyber360DBQueryRootcheck(agent_id=agent_list[0], offset=offset, limit=limit, sort=sort, search=search,
                               select=select, count=True, get_data=True, query=q, filters=filters,
                               distinct=distinct) as db_query:
        data = db_query.run()

    result.affected_items.extend(data['items'])
    result.total_affected_items = data['totalItems']

    return result
