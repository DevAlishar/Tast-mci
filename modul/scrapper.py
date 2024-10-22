from pathlib import Path
import json
import asyncio
from fetch import fetcher, ConnectionError
from datacore import JsonWebRepo, NoXPathError
from exporter import JsonExporter
from extract import extract
from exceptions import ScrapException
from normalizers import StripNormalizer, EmptyNormalizer, CurrencyNormalizer, PCNormalizer

from urllib.parse import urlparse

BASE_DIR = Path(__file__).parent
XPATHS_FILE = BASE_DIR / 'xpath_data.json'
EXPORT_FILE = BASE_DIR / 'output.json'
EXPORT_SUCCESS_FILE = BASE_DIR / 'output_success.json'
EXPORT_FAILS_FILE = BASE_DIR / 'output_fails.json'
URL_FILE = BASE_DIR / "urls.json"

urls = json.loads(open(URL_FILE, 'r+', encoding='utf-8').read())

# WHEN YOURE SEEING THIS

class scrapper:
    def __init__(self) -> None:
        self.repo = JsonWebRepo(XPATHS_FILE)
        self.fetcher = fetcher()
        self.exporter = JsonExporter(EXPORT_FILE)
        self.fails = JsonExporter(EXPORT_FAILS_FILE)
        self.success = JsonExporter(EXPORT_SUCCESS_FILE)
        self.normalizers = [
            EmptyNormalizer(),
            StripNormalizer(),
            CurrencyNormalizer(),
            PCNormalizer()
        ]

    async def scrap(self, url):
        data = {}
        domainData = 'not fetched'
        try:
            html = await self.fetcher.fetch(url)
            domainData = await self.repo.GetXPaths(url)
            xpaths = domainData['xpath']
            for tag, xpath in xpaths.items():
                result = await extract(html, xpath)

                for normalizer in self.normalizers:
                    result = await normalizer.normalize(result, domainData)

                data[tag] = result
    
            if any(data.values()):  
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                await self.success.export({
                    "domain": domain,
                    "xpaths": list(xpaths.values())
                })
            else:
                raise ScrapException("Data extraction resulted in empty content.")

        except ScrapException as e:
            await self.fails.export({
                "url": url,
                "data": domainData,
                "error": e.msg
            })
            
        await self.exporter.export({'url': url, 'results': data})

    async def close(self):
        self.repo.close()
        await self.fetcher.close()
        self.exporter.close()
        self.fails.close()
        self.success.close()

        print(f"Total successful URLs: {len(self.success)}")
        print(f"Total failed URLs: {len(self.fails)}")

async def main():
    tasks = []
    _scrapper = scrapper()
    for url in urls:
        tasks.append(_scrapper.scrap(url))
    await asyncio.gather(*tasks)
    await _scrapper.close()

if __name__ == "__main__":
    asyncio.run(main())
