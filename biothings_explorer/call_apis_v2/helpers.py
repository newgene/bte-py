import yaml


def yaml_2_json(_input):
    doc = yaml.load(_input)
    return doc
