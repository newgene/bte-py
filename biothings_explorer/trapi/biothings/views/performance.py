import os
import json
from tornado.web import RequestHandler


class RoutePerformance(RequestHandler):
    def get(self):
        try:
            self.set_header('Content-Type', 'text/html')
            file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir, 'performance_test', 'report.html'))
            file = open(file_path)
            data = file.read()
            self.write(data)
            file.close()
        except Exception as e:
            print(e)
            self.set_header('Content-Type', 'application/json')
            self.set_status(404)
            self.write({'error': json.dumps(str(e))})
