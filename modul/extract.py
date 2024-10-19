from lxml import etree
import json

async def extract(html, xpath):
        dom = etree.HTML(html)
        price = dom.xpath(xpath)
        if not price or not isinstance(price[0], str) and not price[0].text:
            print("No price extracted or incorrect XPath.")
            return
        extracted_price = price[0].text if hasattr(price[0], 'text') else price[0]
        return extracted_price.strip() if extracted_price else None
