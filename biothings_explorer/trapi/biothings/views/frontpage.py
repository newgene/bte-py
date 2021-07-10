import os
import json
from tornado.web import RequestHandler


class RouteFrontPage(RequestHandler):
    def get(self):
        self.redirect('https://smart-api.info/ui/dc91716f44207d2e1287c727f281d339')
