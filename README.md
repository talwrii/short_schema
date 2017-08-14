<!-- This is generated by make-readme.py do not edit -->
# Short Schema

A proof-of-concept succinct [JSON schema](http://json-schema.org/) language.

# Motivation

JSON is a commonly used machine readable data format.
Placing your data in JSON makes it very easy for people to programmatically use your data.
It is, therefore, unsurprising that JSON schemas are written in JSON.

However, machine-readable is not the same as human-readable,
   and even though JSON is more readable than XML
   it is not as readable as a format explicitly designed to be read by a human.

# Installing

```
pip install git+https://github.com/talwrii/short_schema#egg=short_schema
```

# Examples / Cheat sheet

```bash
$ echo '{"one": 1}' | genson  | short_schema
{one: integer}
$ echo '[{"one": 1, "two": [1]}, {"one": 2}]' | genson  | short_schema
[{one: integer, ?two: [integer]}]

```

# Usage

```
usage: make-readme.py [-h]

A succinct language for json schema

optional arguments:
  -h, --help  show this help message and exit

```
