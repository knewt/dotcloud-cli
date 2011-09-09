class RESTAPIError(Exception):
    def __init__(self, code=None, desc=None):
        self.code = code
        self.desc = desc

    def __str__(self):
        return self.desc
