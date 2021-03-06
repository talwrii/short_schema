# This file is documented in README.md

import json
import subprocess
import unittest

from short_schema import short_schema


def backticks(command, stdin=None, shell=False):
    stdin_arg = subprocess.PIPE if stdin is not None else None

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=stdin_arg, shell=shell)
    result, _ = process.communicate(stdin)
    if process.returncode != 0:
        raise Exception('{!r} returned non-zero return code {!r}'.format(command, process.returncode))
    return result


class Test(unittest.TestCase):
    def encode(self, encoder, input_object, one_line):

        return encoder.encode(json.loads(backticks([b'genson'], stdin=json.dumps(input_object).encode('utf8')).decode('utf8')), one_line=one_line)

    def test_trivial(self):
        return self.assert_encoding({}, '{}', '{}')

    def test_array_singleton(self):
        input_object = dict(a=[1])
        expected_multi = '''\
{
    a: [integer]
}'''
        expected_single = '{a: [integer]}'
        return self.assert_encoding(input_object, expected_single, expected_multi)

    def test_singleton_array(self):
        input_object = dict(a=1)
        expected_multi = '''\
{
    a: integer
}'''
        expected_single = '{a: integer}'
        return self.assert_encoding(input_object, expected_single, expected_multi)

    def test_nested(self):
        input_object = dict(a=dict(b=1))
        expected_single = '{a: {b: integer}}'
        expected_multi = '''\
{
    a: {
        b: integer
    }
}'''
        return self.assert_encoding(input_object, expected_single, expected_multi)

    def test_object_union_types(self):
        input_object = [{"a": 1}, {"a": {"b":2}}]
        expected_single = '[{a: integer | {b: integer}}]'
        expected_multi = '''\
[
    {
        a: integer | {b: integer}
    }
]'''
        return self.assert_encoding(input_object, expected_single, expected_multi)

    def test_complex_array_singleton(self):
        input_object = dict(a=[dict(b=1)])
        expected_single = '{a: [{b: integer}]}'
        expected_multi = '''\
{
    a: [
        {
            b: integer
        }
    ]
}'''
        return self.assert_encoding(input_object, expected_single, expected_multi)

    def test_complex_array_multiple(self):
        input_object = dict(a=[dict(b=1, c=None)], d='hello')
        expected_single = '{a: [{b: integer, c: null}], d: string}'
        expected_multi = '''\
{
    a: [
        {
            b: integer,
            c: null
        }
    ],
    d: string
}'''
        return self.assert_encoding(input_object, expected_single, expected_multi)

    def assert_encoding(self, input_object, expected_single, expected_multi):
        encoder = short_schema.Encoder()
        result_multi = self.encode(encoder, input_object, one_line=False)
        result_single = self.encode(encoder, input_object, one_line=True)

        self.assertEquals(result_single, expected_single, '\n{}\n{}\n{!r}'.format(expected_single, result_single, expected_single))
        self.assertEquals(result_multi, expected_multi, '\n{}\n{}\n{!r}'.format(expected_multi, result_multi, expected_multi))

if __name__ == "__main__":
	unittest.main()
