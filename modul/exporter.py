import json
from asgiref.sync import sync_to_async
from exceptions import ScrapException

adump = sync_to_async(json.dumps)

class BaseExporter:
    async def export(self, data):
        '''
        data = {
            "url": ...,
            "data": {
                "xpath": ...,
                "value": ...
            }
        }
        '''
        raise NotImplementedError()

class JsonExporter:
    def __init__(self, filePath):
        self.file = open(filePath, 'w+')
        self.data = []
    async def export(self, data):
        self.data.append(data)
    def close(self):
        dump = json.dumps(self.data, indent=2, ensure_ascii=False)
        self.file.write(dump)
        self.file.close()
