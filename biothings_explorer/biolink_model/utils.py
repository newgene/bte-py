def underscore(_input):
    if isinstance(_input, str):
        return _input.replace(' ', '_').replace(',', '')
    return None


def pascal_case(s):
    ''.join(x for x in s.title() if not x.isspace())
