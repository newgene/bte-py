import os
import json
from .base_loader import Loader


class DefaultLoader(Loader):
    def load(self, _input=None):
        # file_path = os.path.abspath(
        #     os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'biolink.yaml'))
        biolink_path = os.path.abspath(os.getenv('BIOLINK_FILE')) if os.getenv('BIOLINK_FILE') else \
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'biolink.yaml'))
        #return self.yaml_2_json(file_path)
        extension = os.path.splitext(biolink_path)[1]

        if extension in ['.yaml', '.yml']:
            return self.yaml_2_json(biolink_path)
        else:
            with open(biolink_path) as f:
                return json.load(f)
