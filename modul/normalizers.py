import re
from lxml import etree

class BaseNormalizer:
    async def normalize(self, data, dd):
        raise NotImplementedError()

class CurrencyNormalizer(BaseNormalizer):
    async def normalize(self, data: list[str], dd:dict):
        ndata = []
        for d in data:
            dom = etree.HTML(d)
            if dom is None:
                continue

            text_content = ''.join(dom.itertext())
            text_content = text_content.replace(
                ',', '').replace(
                    '،', '').replace(
                        '٬', '').replace(
                            '.', '')
            number_str = re.findall(r'\d+', text_content)
            if number_str:
                number = int(''.join(number_str))  
                ndata.append(str(number))
        return ndata


class StripNormalizer(BaseNormalizer):
    async def normalize(self, data: list[str], dd):
        ndata = []
        for d in data:
            nd = d.strip()
            nd = nd.replace('\t', '')
            ndata.append(nd)
        return ndata

class EmptyNormalizer(BaseNormalizer):
    async def normalize(self, data: list[str], dd):
        ndata = []
        for d in data:
            if d:
                ndata.append(d)
        return ndata

class PCNormalizer(BaseNormalizer):
    async def normalize(self, data:list[str], dd):
        ndata = []
        for d in data:
            nd = int(d)
            if dd['pc'] < .5 :
                nd /= 10
            nd = int(nd)
            nd = str(nd)
            ndata.append(nd)
        return ndata
