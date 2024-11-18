

from xcyber360.core.common import QUEUE_SOCKET
from xcyber360.core.exception import Xcyber360Error
from xcyber360.core.results import Xcyber360Result, AffectedItemsXcyber360Result
from xcyber360.core.xcyber360_queue import Xcyber360AnalysisdQueue
from xcyber360.rbac.decorators import expose_resources

MSG_HEADER = '1:API-Webhook:'


@expose_resources(actions=["event:ingest"], resources=["*:*:*"], post_proc_func=None)
def send_event_to_analysisd(events: list) -> Xcyber360Result:
    """Send events to analysisd through the socket.

    Parameters
    ----------
    events : list
        List of events to send.

    Returns
    -------
    Xcyber360Result
        Confirmation message.
    """
    result = AffectedItemsXcyber360Result(
        all_msg="All events were forwarded to analisysd",
        some_msg="Some events were forwarded to analisysd",
        none_msg="No events were forwarded to analisysd"
    )

    with Xcyber360AnalysisdQueue(QUEUE_SOCKET) as queue:
        for event in events:
            try:
                queue.send_msg(msg_header=MSG_HEADER, msg=event)
                result.affected_items.append(event)
            except Xcyber360Error as error:
                result.add_failed_item(event, error=error)

    result.total_affected_items = len(result.affected_items)
    return result
