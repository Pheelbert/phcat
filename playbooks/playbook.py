class Playbook:
    def __init__(self):
        self._has_run = False

    @staticmethod
    def description():
        raise NotImplementedError()

    def run(self, shell):
        raise NotImplementedError()

    def has_run(self):
        return self._has_run
