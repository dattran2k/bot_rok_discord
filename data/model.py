from this import d


from types import SimpleNamespace
import json

class DataTitle :
    def __init__(self,x,y,title,time,timeRequest):
        self.x = x
        self.y = y
        self.title = title
        self.time = time
        self.timeRequest = timeRequest
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def fromJSON(seft,data):
        result = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        seft = result
        