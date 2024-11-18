from pydantic import PositiveInt

from xcyber360.core.config.models.base import Xcyber360ConfigBaseModel
from xcyber360.core.config.models.ssl_config import IndexerSSLConfig


class IndexerConfig(Xcyber360ConfigBaseModel):
    """Configuration for the Indexer.

    Parameters
    ----------
    host : str
        The host address of the indexer.
    port : PositiveInt
        The port number for the indexer.
    user : str
        The username for indexer authentication.
    password : str
        The password for indexer authentication.
    ssl : IndexerSSLConfig, optional
        SSL configuration for the indexer. Default is an instance of IndexerSSLConfig.
    """
    host: str
    port: PositiveInt
    user: str
    password: str
    ssl: IndexerSSLConfig = IndexerSSLConfig()
