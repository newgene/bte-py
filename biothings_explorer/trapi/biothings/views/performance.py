import os
import json
from tornado.web import RequestHandler


class RoutePerformance(RequestHandler):
    def get(self):
        try:
            file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'performance-test', 'report.html'))
            file = open(file_path)
            data = file.read()
            self.write(data)
        except Exception as e:
            print(e)
            self.set_header('Content-Type', 'application/json')
            self.set_status(404)
            self.write({'error': json.dumps(str(e))})
