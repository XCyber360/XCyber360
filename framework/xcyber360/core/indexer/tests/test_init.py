from unittest import mock

import pytest
from opensearchpy import AsyncOpenSearch
from xcyber360.core.exception import Xcyber360IndexerError
from xcyber360.core.indexer import Indexer, create_indexer, get_indexer_client


@pytest.fixture
def indexer_instance_with_mocked_client() -> Indexer:
    indexer_instance = Indexer(host='test', user='user_test', password='password_test')
    indexer_instance._client = mock.AsyncMock()
    return indexer_instance


class TestIndexer:
    @pytest.mark.parametrize(
        'params',
        [
            {'user': 'user_test', 'password': 'password_test'},
            {'client_cert_path': '/tmp/client.pem', 'client_key_path': '/tmp/client-key.pem'},
        ],
    )
    def test_indexer_init(self, params: dict):
        """Check the correct initalization of the `Indexer` class."""
        indexer_instance = Indexer(host='test', **params)

        assert isinstance(indexer_instance._client, AsyncOpenSearch)

    @pytest.mark.parametrize(
        'params',
        [
            {'user': 'user_test'},
            {'password': 'password_test'},
            {'client_cert_path': '/tmp/client.pem'},
            {'client_key_path': '/tmp/client-key.pem'},
            {},
        ],
    )
    def test_indexer_init_ko(self, params: dict):
        """Check the correct initalization of the `Indexer` class."""
        with pytest.raises(Xcyber360IndexerError, match='.*2201.*'):
            Indexer(host='test', **params)

    async def test_connect(self, indexer_instance_with_mocked_client):
        """Check the correct function of `connect` method."""

        indexer_instance_with_mocked_client._client.ping.return_value = True
        await indexer_instance_with_mocked_client.connect()

        indexer_instance_with_mocked_client._client.ping.assert_called_once()

    async def test_connect_ko(self, indexer_instance_with_mocked_client):
        """Check the correct raise of `connect` method."""

        indexer_instance_with_mocked_client._client.ping.return_value = False

        with pytest.raises(Xcyber360IndexerError, match='.*2200.*'):
            await indexer_instance_with_mocked_client.connect()

    async def test_close(self, indexer_instance_with_mocked_client):
        """Check the correct function of `close` method."""

        await indexer_instance_with_mocked_client.close()

        indexer_instance_with_mocked_client._client.close.assert_called_once()


@mock.patch('xcyber360.core.indexer.Indexer', autospec=True)
async def test_create_indexer(indexer_mock: mock.AsyncMock):
    """Check the correct function of `create_index`."""

    host = 'test'
    user = 'user_test'
    password = 'password_test'

    instance_mock = await create_indexer(host=host, user=user, password=password)
    indexer_mock.assert_called_once_with(host=host, user=user, password=password, port=9200)
    instance_mock.connect.assert_called_once()


@pytest.mark.parametrize('retries', [2, 4])
@mock.patch('xcyber360.core.indexer.Indexer', autospec=True)
async def test_create_indexer_ko(indexer_mock: mock.AsyncMock, retries: int):
    """Check the correct raise of `create_index`."""

    host = 'test'
    user = 'user_test'
    password = 'password_test'

    instance_mock = mock.AsyncMock()
    instance_mock.connect.side_effect = Xcyber360IndexerError(2200)
    indexer_mock.return_value = instance_mock

    with mock.patch('xcyber360.core.indexer.sleep') as sleep_mock:
        with pytest.raises(Xcyber360IndexerError, match='.*2200.*'):
            instance_mock = await create_indexer(host=host, user=user, password=password, retries=retries)

        assert instance_mock.connect.call_count == retries + 1
        instance_mock.close.assert_called_once()
        assert sleep_mock.call_count == retries


@mock.patch('xcyber360.core.indexer.create_indexer')
async def test_get_indexer_client(create_indexer_mock):
    """Check the correct function of `get_indexer_client`."""

    client_mock = mock.AsyncMock()
    create_indexer_mock.return_value = client_mock
    async with get_indexer_client() as indexer:
        create_indexer_mock.assert_called_once_with(
            host='',
            user='',
            password='',
            use_ssl=True,
            client_cert_path='',
            client_key_path='',
            ca_certs_path='',
            retries=1,
        )
        assert indexer == client_mock
    client_mock.close.assert_called_once()
