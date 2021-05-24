def underscore(_input):
    if isinstance(_input, str):
        return _input.replace(' ', '_').replace(',', '')
    return None


def smart_title(s):
    return ' '.join(w if w.isupper() else w.capitalize() for w in s.split())


def pascal_case(s):
    return ' '.join([w.capitalize() if w.islower() else w for w in s.split()]).replace(' ', '')
