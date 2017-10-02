import json
import argparse
import sys

def build_parser():
    return argparse.ArgumentParser(description='A succinct language for json schema', prog='short_schema')

def encode(item):
    if item['type'] == 'array':
        return encode_array(item)
    elif item['type'] == 'object':
        return encode_object(item)
    else:
        return encode_type(item['type'])

def encode_type(_type):
    if _type == 'string':
        return 'str'
    elif _type == 'integer':
        return 'integer'
    elif _type == 'number':
        return 'number'
    elif _type == 'null':
        return 'null'
    elif isinstance(_type, list):
        return ' | '.join(map(encode_type, _type))
    else:
        raise NotImplementedError(_type)

def encode_type_arrays(array):
    return '[{}]'.format(', '.join(map(encode, array)))

def encode_object(item):
    properties = item.get('properties', {})
    required = set(item.get('required', []))
    text = [encode_property(name, schema, name not in required) for name, schema in sorted(properties.items())]

    return '{}{}{}'.format('{', ', '.join(text), '}')

def encode_array(item):
    if not item['items']:
        return '[]'
    if 'properties' not in item['items']:
        return '[{}]'.format(encode(item['items']))
    else:
        return '[{}]'.format(encode_object(item['items']))

def encode_property(name, schema, optional):
    optional_flag = '?' if optional else ''
    return optional_flag + '{}: {}'.format(name, encode(schema))

def main():
    _args = build_parser().parse_args()
    data = json.loads(sys.stdin.read())
    print encode(data)
