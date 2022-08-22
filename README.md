# Amersham

<p align="end">
    <img src="https://github.com/inigo-selwood/amersham/actions/workflows/test.yaml/badge.svg?event=push" alt="Test" />
    <img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/inigo-selwood/a15864cab2eed694c754703ad4b73181/raw/b572b5120488b2f80bd3cc9ade3931db4d7d86ad/amersham-coverage-badge.json" alt="Coverage" />
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