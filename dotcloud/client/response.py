class ErrorResponse(object):
    def __init__(self, code=None, desc=None):
        self.code = code
        self.desc = desc

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
    def __iter__(self):
        for obj in self.obj:
            yield obj
        
class ItemResponse(BaseResponse):
    def __iter__(self):
        yield self.obj

class NoItemResponse(BaseResponse):
    def __iter__(self):
        return None
