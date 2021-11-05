import re

def underscore(_input):
    if isinstance(_input, str):
        return _input.replace(' ', '_').replace(',', '')
    return None


def smart_title(s):
    return ' '.join(w if w.isupper() else w.capitalize() for w in s.split())


def pascal_case(s):
    # converts strings like microRNA to "micro RNA"
    rx = re.compile(r'(?<=[a-z])(?=[A-Z])')
    s = rx.sub(' ', s)

    return ' '.join([w.lower().capitalize() for w in s.split()]).replace(' ', '')
