def slice(val, render):
    split = val.split(';')
    if len(split) < 2:
        return val
    string = split[0]
    begin = 0 if split[1] == '' else split[1]
    end = len(string) if split[2] == '' else split[2]
    return render(string)[begin:end]


def rm_prefix(val, render):
    split = render(val).split(':')
    if len(split) < 2:
        return val
    return split[1]


def repl_prefix(val, render):
    split = val.split(';')
    if len(split) < 2:
        return render(val)
    str_split = render(split[0]).split(':')
    new_prefix = render(split[1])
    return new_prefix + ':' + str_split[1] if len(str_split) > 1 else new_prefix + ':' + str_split[0]
