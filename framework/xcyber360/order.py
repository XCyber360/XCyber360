from typing import List

from api.models.order_model import Order
from xcyber360.core.cluster import local_client
from xcyber360.core.cluster.control import distribute_orders
from xcyber360.core.exception import Xcyber360Error, Xcyber360ClusterError
from xcyber360.core.results import AffectedItemsXcyber360Result
from xcyber360.rbac.decorators import expose_resources


@expose_resources(actions=["order:send"], resources=["*:*:*"], post_proc_func=None)
async def send_orders(orders: List[Order]) -> AffectedItemsXcyber360Result:
    """Send orders to the local server and distribute them to other nodes and components.

    Parameters
    ----------
    orders : List[Order]
        Orders object holding a list of orders.

    Returns
    -------
    AffectedItemsXcyber360Result
        Result with the published orders.
    """
    result = AffectedItemsXcyber360Result(
        all_msg="All orders were published",
        some_msg="Some orders were published",
        none_msg="No orders were published"
    )

    order_ids = [item['order_id'] for item in orders]
    try:
        lc = local_client.LocalClient()
        await distribute_orders(lc, orders)
        result.affected_items.extend(order_ids)
    except (Xcyber360Error, Xcyber360ClusterError) as e:
        for id_ in order_ids:
            result.add_failed_item(id_=id_, error=e)

    result.total_affected_items = len(result.affected_items)

    return result