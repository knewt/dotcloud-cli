class BaseResponse(object):
    def __init__(self, obj=None):
        self.obj = obj
    
    @classmethod
    def create(cls, res=None, data=None):
        resp = None
        if 'object' in data:
            resp = ItemResponse(obj=data['object'])
        elif 'objects' in data:
            resp = ListResponse(obj=data['objects'])
        else:
            resp = NoItemResponse(obj=None)
        resp.res = res
        resp.data = data
        return resp
        
class ListResponse(BaseResponse):
    @property
    def items(self):
        return self.obj

    @property
    def item(self):
        return self.obj[0]
        
class ItemResponse(BaseResponse):
    @property
    def items(self):
        return [self.obj]

    @property
    def item(self):
        return self.obj

class NoItemResponse(BaseResponse):
    @property
    def items(self):
        return None

    @property
    def item(self):
        return None
