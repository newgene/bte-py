# import unittest
# from jinja2 import Environment, BaseLoader
#
#
# class TestTemplateFuncs(unittest.TestCase):
#     def test_substr_behavior(self):
#         string = 'abcdefghi'
#
#         def run(string, begin=None, end=None):
#             return Environment().from_string("{{ test | substr(" + f"{begin}" + ", " + f"{end}" + ")}}", {'test': string}).render()
#
#         res = run(string)
#         self.assertEqual(res, string)
