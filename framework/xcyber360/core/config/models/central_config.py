from xcyber360.core.config.models.base import Xcyber360ConfigBaseModel
from xcyber360.core.config.models.server import ServerConfig
from xcyber360.core.config.models.indexer import IndexerConfig
from xcyber360.core.config.models.engine import EngineConfig
from xcyber360.core.config.models.management_api import ManagementAPIConfig
from xcyber360.core.config.models.comms_api import CommsAPIConfig


class Config(Xcyber360ConfigBaseModel):
    """Main configuration class for the application.

    Parameters
    ----------
    server : ServerConfig
        Configuration for the server.
    indexer : IndexerConfig
        Configuration for the indexer.
    engine : EngineConfig, optional
        Configuration for the engine. Default is an instance of EngineConfig.
    management_api : ManagementAPIConfig, optional
        Configuration for the management API. Default is an instance of ManagementAPIConfig.
    communications_api : CommsAPIConfig, optional
        Configuration for the communications API. Default is an instance of CommsAPIConfig.
    """
    server: ServerConfig
    indexer: IndexerConfig
    engine: EngineConfig = EngineConfig()
    management_api: ManagementAPIConfig = ManagementAPIConfig()
    communications_api: CommsAPIConfig = CommsAPIConfig()
