def underscore(_input):
    if isinstance(_input, str):
        return _input.replace(' ', '_').replace(',', '')
    return None


def smart_title(s):
    return ' '.join(w if w.isupper() else w.capitalize() for w in s.split())


def pascal_case(s):
    # if s == 'Microrna':
    #     print(s)
    #
    if len(s.split()) == 1 and s[0].isupper():
        return s
    return ' '.join([w.lower().capitalize() for w in s.split()]).replace(' ', '')
