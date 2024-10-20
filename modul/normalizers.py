import re
from lxml import etree

class BaseNormalizer:
    async def normalize(self, data):
        raise NotImplementedError()

class CurrencyNormalizer(BaseNormalizer):
    async def normalize(self, data: list[str]):
        ndata = []
        for d in data:
            dom = etree.HTML(d)
            if dom is None:
                continue

            text_content = ''.join(dom.itertext())
            is_rial = 'ریال' in text_content or '&nbsp;' in text_content or 'nbsp' in text_content.lower()
            number_str = re.findall(r'\d+', text_content.replace(',', '').replace('،', '').replace('٬', '').replace('.', ''))
            if number_str:
                number = int(''.join(number_str))  
                if is_rial:
                    number //= 10
                ndata.append(number)
        return ndata


class StripNormalizer(BaseNormalizer):
    async def normalize(self, data: list[str]):
        ndata = []
        for d in data:
            nd = d.strip()
            nd = nd.replace('\t', '')
            ndata.append(nd)
        return ndata

class EmptyNormalizer(BaseNormalizer):
    async def normalize(self, data: list[str]):
        ndata = []
        for d in data:
            if d:
                ndata.append(d)
        return ndata
