import json
import argparse
import sys

def build_parser():
    parser = argparse.ArgumentParser(description='A succinct language for json schema', prog='short_schema')
    parser.add_argument('--pretty', '-p', action='store_true', default=False, help='Spread the output over multiple lines')
    return parser

class Encoder(object):

    def __init__(self, pretty):
        self.pretty = pretty

    def encode(self, item):
        if item['type'] == 'array':
            return self.encode_array(item)
        elif item['type'] == 'object':
            return self.encode_object(item)
        else:
            return self.encode_type(item['type'])

    def encode_type(self, _type):
        if _type == 'string':
            return 'str'
        elif _type == 'integer':
            return 'integer'
        elif _type == 'number':
            return 'number'
        elif _type == 'null':
            return 'null'
        elif isinstance(_type, list):
            return ' | '.join(map(self.encode_type, _type))
        else:
            raise NotImplementedError(_type)

    def encode_type_arrays(self, array):
        return '[{}]'.format(', '.join(map(self.encode, array)))

    def encode_object(self, item):
        properties = item.get('properties', {})
        required = set(item.get('required', []))
        text = [self.encode_property(name, schema, name not in required) for name, schema in sorted(properties.items())]
        return '{}{}{}'.format('{', ', '.join(text), '}')

    def encode_array(self, item):
        if not item['items']:
            return '[]'
        if 'properties' not in item['items']:
            return '[{}]'.format(self.encode(item['items']))
        else:
            return '[{}]'.format(self.encode_object(item['items']))

    def encode_property(self, name, schema, optional):
        optional_flag = '?' if optional else ''
        return optional_flag + '{}: {}'.format(name, self.encode(schema))

def main():
    args = build_parser().parse_args()
    data = json.loads(sys.stdin.read())
    print encode(data)
