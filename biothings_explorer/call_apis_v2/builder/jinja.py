from jinja2 import Environment

from . import template_helpers

jinja_env = Environment()

# Register custom filters
for filter_func in template_helpers.all_filters:
    jinja_env.filters[filter_func.__name__] = filter_func
