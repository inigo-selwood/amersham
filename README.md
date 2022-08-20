# Amersham

<p align="end">
    <img src="https://github.com/inigo-selwood/amersham/actions/workflows/test.yaml/badge.svg?event=push" alt="Test" />
    <img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/inigo-selwood/a15864cab2eed694c754703ad4b73181/raw/b572b5120488b2f80bd3cc9ade3931db4d7d86ad/amersham-coverage-badge.json" alt="Coverage" />
</p>

**Amersham:** The name of a London Underground station which alliterates with "argument parser"

## Motivation

Every CLI application wants two things:

1. Vetted user input
2. Descriptive usage and help messages

Amersham takes care of both with minimal boilerplate.

## Examples

Amersham generates descriptive help messages, so you don't have to.

For the application:

```
user:app$ python3 app.py --help
usage
  app [--help] {command} ...

description
  a parser

commands
  command  a command
```

And for each command:

```
user:app$ python3 app.py command --help
usage
  app command [--help] {command} ...

description
  a command

flags
  --help  -h  displays this message
  --flag  -f  a flag

parameters
  parameter  a parameter
```

## Installation

```
user:app$ pip3 install amersham
```

## Quick Start

Import

``` python
import sys

from amersham import Parser, Flag, Parameter
```

Create a parser

``` python
parser = Parser("parser", "a parser")
```

Create a command

``` python
@parser.command("a command",
        flag = Flag("a flag"),
        parameter = Parameter("a parameter"))
def command(parameter: str, flag: str):
    print(parameter, flag)
```

Run the parser

``` python
if __name__ == "__main__":
    parser.run(sys.argv[1:])
```
