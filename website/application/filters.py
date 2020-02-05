from jinja2 import Undefined
from flask import Blueprint

filter = Blueprint("filter", __name__)

# JINJA TEMPLATE FILTERS
@filter.context_processor
def slice():
    def _slice(iterable, pattern):
        if iterable is None or isinstance(iterable, Undefined):
            return iterable

        # convert to list so we can slice
        items = str(iterable)

        start = None
        end = None
        stride = None

        # split pattern into slice components
        if pattern:
            tokens = pattern.split(':')
            print(tokens)
            if len(tokens) > 1:
                start = int(tokens[0])
            if len(tokens) > 2:
                end = int(tokens[1])
            if len(tokens) > 3:
                stride = int(tokens[2])

        return items[start:end:stride]
    return dict(slice=_slice)