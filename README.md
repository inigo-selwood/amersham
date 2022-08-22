# Amersham

<p align="end">
    <img src="https://github.com/inigo-selwood/amersham/actions/workflows/test.yaml/badge.svg?event=push" alt="Test" />
    <img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/inigo-selwood/a15864cab2eed694c754703ad4b73181/raw/amersham-coverage-badge.json" alt="Coverage" />
</p>

**Amersham:** The name of a London Underground station which alliterates with "argument parser"

## Motivation

Every CLI application wants two things:

1. Sanitized user input
2. Descriptive usage and help messages

Amersham implements both with minimal boilerplate.

## Quick Start

Install

```
pip3 install amersham
```

Import

```python
import sys

from amersham import Parser
```

Create a parser and command

```python
parser = Parser("app")

@parser.command()
def command(parameter, flag = None):
    pass
```

Run the parser

```python
if __name__ == "__main__":
    parser.run(sys.argv[1:])
```

Run your program

```
user:~$ python3 app.py --help
usage
  app.py [--help] [--flag] PARAMETER

flags
  --help  -h  displays this message
  --flag

parameters
  PARAMETER  string
```

## Advanced Usage

### More Descriptive Help Messages

Add some context to our command and arguments

```python
overrides = {
    "description": "a command",

    "parameter": {
        "description": "a parameter",
    },
    "flag": {
        "description": "a flag",
        "alias": "f",
    }
}

@parser.command(**overrides)
def command(parameter, flag = ""):
    pass
```

And see the results

```
user:~$ python3 app.py --help
usage
  app.py [--help] [--flag] PARAMETER

description
  a command

flags
  --help  -h          displays this message
  --flag      string  a flag

parameters
  PARAMETER  string  a parameter
```
