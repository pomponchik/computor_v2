class Executor:
    def __init__(self, sg, context):
        self.sg = sg
        self.context = context

    def execute(self):
        return self.sg.root.calculate(self.context)
