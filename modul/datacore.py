import re
import pandas as pd
from urllib.parse import urlparse
import json
from exceptions import ScrapException

class NoXPathError(ScrapException): ...

class BaseWebRepo:
    async def GetXPaths(self, url):
        raise NotImplementedError()
    def close(self): 
        pass
class PandasWebRepo(BaseWebRepo):
    def __init__(self, dataframe:pd.DataFrame):
        self.df = dataframe
        keys = list(self.df.columns)
        xpathRegex = r'xpath.*'
        for item in keys.copy():
            if not re.match(xpathRegex, item.lower()):
                keys.remove(item)
        self.keys = keys
    async def GetXPaths(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        result = {
            key: "" for key in self.keys
        }
        for _, data in self.df.iterrows():
            if data['Domain'] == domain:
                for key in self.keys:
                    result[key] = data[key]
                break
        return result


class JsonWebRepo(BaseWebRepo):
    def __init__(self, json_file):
        self.json = json.loads(open(json_file, 'r+').read())
    async def GetXPaths(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        dataFilter=filter(lambda x:x['domain'].lower()==domain, self.json)
        try:
            domainData = next(iter(dataFilter))
        except:
            raise NoXPathError("XPath not exists")
        result={}
        for i, xpath in enumerate(domainData['xpaths']):
            result[str(i)]=xpath
        pc = domainData['price_currency']
        if isinstance(pc, list):
            pc = pc[0]
        result = {
            'xpath': result,
            'pc': pc
        }
        return result
class ExcelWebRepo(PandasWebRepo):
    def __init__(self, ExcelFileRepo):
        df = pd.read_excel(ExcelFileRepo)
        super().__init__(df)
