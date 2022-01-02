class InterpretatorCallback:
    def __init__(self, function, filter):
        self.function = function
        self.filter = filter if filter is not None else lambda x: True

    def __call__(self, string, string_number, context):
        if self.allowed(string):
            try:
                return self.function(string, string_number, context)
            except Exception as e:
                return f'oops! internal error ({e})'

    def allowed(self, string):
        try:
            result = bool(self.filter(string))
            return result
        except:
            return False
