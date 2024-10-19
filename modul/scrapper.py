XPATHS_FILE = ''
EXPORT_FILE = ''
urls = []

import asyncio
from .fetch import fetcher
from .datacore import ExcelWebRepo
from .exporter import JsonExporter
from .extract import extract

class scrapper:
    def __init__(self) -> None:
        self.repo = ExcelWebRepo()
        self.fetcher = fetcher()
        self.exporter = JsonExporter()
    async def scrap(self, url):
        html = await self.fetcher.fetch(url)
        xpaths = await self.repo.GetXPaths(url)
        data = {}
        for tag, xpath in xpaths:
            data[tag] = (
                await extract(html, xpath)
            )
        await self.exporter.export(
            {
                'url': url,
                'xpaths': data
            }
        )

    def close(self):
        self.repo.close()
        self.fetcher.close()
        self.exporter.close()

async def main():
    tasks = []
    with scrapper() as _scrapper:
        for url in urls:
            tasks.append(
                _scrapper.scrap(url)
            )
        await asyncio.gather(
            *tasks
        )
