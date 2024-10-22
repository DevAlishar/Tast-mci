from lxml import etree
import json

def extractNode(node):
    base = node.text
    for ch in node.getchildren():
        base += extractNode(ch)
    return base

async def extract(html, xpath):
        dom = etree.HTML(html)
        nodes = dom.xpath(xpath)
        result = []
        for node in nodes:
            if hasattr(node, 'text'):
                result.append(extractNode(node))
            else:
                if isinstance(node, str):
                    result.append(node)
                elif isinstance(node, bytes):
                    result.append(node.decode())
                else:
                    result.append(str(node))
        return result
