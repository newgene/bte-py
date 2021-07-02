from datetime import datetime


class LogEntry:
    def __init__(self, level='DEBUG', code=None, message=None):
        self.level = level
        self.message = message
        self.code = code

    def get_log(self):
        return {
            'timestamp': datetime.now(),
            'level': self.level,
            'message': self.message,
            'code': self.code,
        }
