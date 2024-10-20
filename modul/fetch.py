from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError, ConnectionTimeoutError, ClientPayloadError
from asgiref.sync import async_to_sync
from exceptions import ScrapException

class ConnectionError(ScrapException): ...

class fetcher:
    def __init__(self):
        self.session = ClientSession()

    async def fetch(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        try:
            response = await self.session.get(url, headers=headers)
        except (ClientConnectorError, ConnectionTimeoutError, ClientPayloadError):
            raise ConnectionError("Connection Failed")
        html = await response.text()
        response.close()
        return html

    async def close(self):
        await self.session.close()
