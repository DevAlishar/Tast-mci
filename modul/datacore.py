import re
import pandas as pd
from urllib.parse import urlparse

class BaseWebRepo:
    async def GetXPaths(self, url):
        raise NotImplementedError()

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

class ExcelWebRepo(PandasWebRepo):
    def __init__(self, ExcelFileRepo):
        df = pd.read_excel(ExcelFileRepo)
        super().__init__(df)
