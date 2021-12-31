class InterpretatorCallback:
    def __init__(self, function, filter):
        self.function = function
        self.filter = filter if filter is not None else lambda x: True

    def __call__(self, string):
        if self.allowed(string):
            self.function(string)

    def allowed(self, string):
        try:
            result = bool(self.filter(string))
            return result
        except:
            return False
