from aiohttp import ClientSession

class fetcher:
    def __init__(self):
        self.session = ClientSession()

    async def fetch(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = await self.session.get(url, headers=headers)
        html = await response.text()
        return html

    def close(self):
        self.session.close()
