import json
import argparse
import sys

def build_parser():
    parser = argparse.ArgumentParser(description='A succinct language for json schema', prog='short_schema')
    parser.add_argument('--debug', action='store_true', help='Print debug output')
    parser.add_argument('--one-line', '-1', action='store_true', default=False, help='Spread the output over multiple lines')
    return parser

class Encoder(object):
    def __init__(self, one_line):
        self.one_line = one_line
        self.indent_string = '    '

    def encode(self, item, indent=0):
        if item['type'] == 'array':
            return self.encode_array(item, indent)
        elif item['type'] == 'object':
            return self.encode_object(item, indent)
        else:
            return self.encode_type(item['type'], indent)

    def encode_type(self, _type, indent):
        # e.g. 1, "hello"
        total_indent_string = ''
        if _type == 'string':
            return total_indent_string + 'string'
        elif _type == 'integer':
            return total_indent_string + 'integer'
        elif _type == 'number':
            return total_indent_string + 'number'
        elif _type == 'null':
            return total_indent_string + 'null'
        elif isinstance(_type, list):
            return self.indent_string * indent + ' | '.join([self.encode_type(t, 0) for t in _type])
        else:
            raise NotImplementedError(_type)

    def encode_object(self, item, indent):
        # e.g {}, {a:1}
        properties = item.get('properties', {})
        required = set(item.get('required', []))
        new_indent = indent if self.one_line else indent + 1
        contents = [self.encode_property(name, schema, name not in required, new_indent) for name, schema in sorted(properties.items())]
        if not contents:
            return '{}'
        if not self.one_line:
            return '{}\n{}\n{}'.format(indent * self.indent_string + '{', ',\n'.join(contents), indent * self.indent_string + '}')
        else:
            return '{}{}{}'.format('{', ', '.join(contents), '}')

    def encode_array(self, item, indent):
        # e.g. [], [{}], [1, 2]
        if not item['items']:
            return '[]'
        if 'properties' not in item['items']:
            return self.encode_simple_array(item, indent)
        else:
            return self.encode_object_array(item, indent)

    def encode_object_array(self, item, indent):
        # e.g. [{}]
        if not self.one_line:
            return (
                '[\n{}'.format(self.encode_object(item['items'], indent + 1)) +
                '\n' + self.indent_string * indent + ']')
        else:
            return '[{}]'.format(self.encode_object(item['items'], indent + 1))

    def encode_simple_array(self, item, indent):
        # e.g. [1, 2]
        if not self.one_line:
            return (
                self.indent_string * indent +
                '[{}'.format(self.encode(item['items']), indent=indent) + ']'
            )
        else:
            return '[{}]'.format(self.encode(item['items']))

    def encode_property(self, name, schema, optional, indent):
        optional_flag = '?' if optional else ''
        encode_value = self.encode(schema, indent=indent).strip(' ')
        encode_pair = '{}: {}'.format(name, encode_value)
        if self.one_line:
            return encode_pair
        else:
            return self.indent_string * indent + optional_flag + encode_pair

def main():
    args = build_parser().parse_args()
    data = json.loads(sys.stdin.read())
    print(Encoder(args.one_line).encode(data))
