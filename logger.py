from descriptor import Descriptor


class Logger:

    LOGS = []

    def add_log(self, turn_result):
        log = Descriptor.describe_as_log(turn_result)
        self.LOGS.append(log)

    def get_log(self, index: int):
        if len(self.LOGS) < index:
            return ''

        return '{}{} : {}'.format(
            " " * 5,
            len(self.LOGS)- index+1,
            self.LOGS[-index])
