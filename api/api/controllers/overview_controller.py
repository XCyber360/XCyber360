

# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import logging

from connexion import request
from connexion.lifecycle import ConnexionResponse

from api.controllers.util import json_response
from api.util import raise_if_exc, remove_nones_to_dict
from xcyber360.agent import get_full_overview
from xcyber360.core.cluster.dapi.dapi import DistributedAPI

logger = logging.getLogger('xcyber360-api')


async def get_overview_agents(pretty: bool = False, wait_for_complete: bool = False) -> ConnexionResponse:
    """Get full summary of agents.

    Parameters
    ----------
    pretty: bool
        Show results in human-readable format.
    wait_for_complete : bool
        Disable timeout response.

    Returns
    -------
    ConnexionResponse
        API response.
    """
    f_kwargs = {}

    dapi = DistributedAPI(f=get_full_overview,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='local_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          logger=logger,
                          rbac_permissions=request.context['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return json_response(data, pretty=pretty)
