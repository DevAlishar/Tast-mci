import json
from asgiref.sync import sync_to_async

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
        dump = json.dump(self.data)
        self.file.write(dump)
        self.file.close()
