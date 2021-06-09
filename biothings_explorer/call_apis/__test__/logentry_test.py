import unittest
from ..log_entry import LogEntry


class TestLogEntryModule(unittest.TestCase):
    def test_if_no_optional_param_passed_should_return_default_value(self):
        log = LogEntry().get_log()
        self.assertEqual(log['code'], None)
        self.assertEqual(log['level'], 'DEBUG')
        self.assertEqual(log['message'], None)
        self.assertIn('timestamp', log)

    def test_if_code_is_correctly_set(self):
        log = LogEntry('DEBUG', 404).get_log()
        self.assertEqual(log['code'], 404)
        self.assertEqual(log['level'], 'DEBUG')
        self.assertEqual(log['message'], None)
        self.assertIn('timestamp', log)

    def test_if_message_is_correctly_set(self):
        log = LogEntry('DEBUG', None, 'yes').get_log()
        self.assertEqual(log['code'], None)
        self.assertEqual(log['level'], 'DEBUG')
        self.assertEqual(log['message'], 'yes')
        self.assertIn('timestamp', log)
