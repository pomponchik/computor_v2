from srcs.interpretator.interpretator_callback import InterpretatorCallback


class Interpretator:
    def __init__(self, runner, meta=None):
        self.runner = runner
        self.meta = meta
        self.callbacks = []

    def __call__(self, filter=None):
        def decorator(function):
            self.callbacks.append(InterpretatorCallback(function, filter))
            return function
        return decorator

    def execute(self, string):
        return string

    def run(self):
        self.runner(self)
