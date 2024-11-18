import logging
import socket
from datetime import datetime

from connexion.lifecycle import ConnexionResponse

from api.controllers.util import json_response
from api.models.basic_info_model import BasicInfo
from xcyber360.core.common import DATE_FORMAT
from xcyber360.core.results import Xcyber360Result
from xcyber360.core.security import load_spec
from xcyber360.core.utils import get_utc_now

logger = logging.getLogger('xcyber360-api')


async def default_info(pretty: bool = False) -> ConnexionResponse:
    """Return basic information about the Xcyber360 API.

    Parameters
    ----------
    pretty: bool
        Show results in human-readable format.

    Returns
    -------
    ConnexionResponse
        API response.
    """
    info_data = load_spec()
    data = {
        'title': info_data['info']['title'],
        'api_version': info_data['info']['version'],
        'revision': info_data['info']['x-revision'],
        'license_name': info_data['info']['license']['name'],
        'license_url': info_data['info']['license']['url'],
        'hostname': socket.gethostname(),
        'timestamp': get_utc_now().strftime(DATE_FORMAT)
    }
    data = Xcyber360Result({'data': BasicInfo.from_dict(data)})

    return json_response(data, pretty=pretty)
