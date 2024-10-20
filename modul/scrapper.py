from pathlib import Path
import json
import asyncio
from fetch import fetcher, ConnectionError
from datacore import JsonWebRepo, NoXPathError
from exporter import JsonExporter
from extract import extract
from exceptions import ScrapException
from normalizers import StripNormalizer, EmptyNormalizer, CurrencyNormalizer

from urllib.parse import urlparse

BASE_DIR = Path(__file__).parent
XPATHS_FILE = BASE_DIR / 'xpath_data.json'
EXPORT_FILE = BASE_DIR / 'output.json'
URL_FILE = BASE_DIR / "urls.json"

urls = json.loads(open(URL_FILE, 'r+', encoding='utf-8').read())

class scrapper:
    def __init__(self) -> None:
        self.repo = JsonWebRepo(XPATHS_FILE)
        self.fetcher = fetcher()
        self.exporter = JsonExporter(EXPORT_FILE)
        self.failed_urls = []
        self.successful_urls = []  
        self.normalizers = [
            EmptyNormalizer(),
            StripNormalizer(),
            CurrencyNormalizer(),  
        ]

    async def scrap(self, url):
        data = {}
        try:
            html = await self.fetcher.fetch(url)
            xpaths = await self.repo.GetXPaths(url)
            for tag, xpath in xpaths.items():
                result = await extract(html, xpath)
                

                for normalizer in self.normalizers:
                    result = await normalizer.normalize(result)


                data[tag] = result


            if any(data.values()):  
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                self.successful_urls.append({
                    "domain": domain,
                    "xpaths": list(xpaths.values())
                })
            else:
                raise ScrapException("Data extraction resulted in empty content.")

        except ScrapException as e:
            self.failed_urls.append({
                "url": url,
                "xpaths": list(xpaths.values()) if 'xpaths' in locals() else [],
                "error": e.msg
            })

        await self.exporter.export({'url': url, 'results': data})

    async def close(self):
        self.repo.close()
        await self.fetcher.close()
        self.exporter.close()


        with open(BASE_DIR / 'success_output.json', 'w', encoding='utf-8') as f:
            json.dump(self.successful_urls, f, indent=2, ensure_ascii=False)


        with open(BASE_DIR / 'faild_output.json', 'w', encoding='utf-8') as f:
            json.dump(self.failed_urls, f, indent=2, ensure_ascii=False)


        print(f"Total successful URLs: {len(self.successful_urls)}")
        print(f"Total failed URLs: {len(self.failed_urls)}")

async def main():
    tasks = []
    _scrapper = scrapper()
    for url in urls:
        tasks.append(_scrapper.scrap(url))
    await asyncio.gather(*tasks)
    await _scrapper.close()

if __name__ == "__main__":
    asyncio.run(main())
