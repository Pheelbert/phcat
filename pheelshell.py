class Pheelshell():
    def __init__(self, socket_wrapper):
        self.socket_wrapper = socket_wrapper
        self.playbooks = {}

    def execute_command(self, command, single_line_output=False):
        if single_line_output:
            return self.socket_wrapper.send_command_read_output(command.encode(), single_line_output=True)
        else:
            return self.socket_wrapper.send_command_read_cached_temporary_file(command.encode())

    def run_playbook(self, playbook):
        playbook.run(self)

        playbook_class_name = playbook.__class__.__name__
        self.playbooks[playbook_class_name] = playbook

    def get_playbook(self, playbook_class):
        playbook_class_name = playbook_class.__name__
        if playbook_class_name in self.playbooks:
            return self.playbooks[playbook_class_name]

        return None
