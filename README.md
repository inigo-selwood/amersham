# Amersham

![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/inigo-selwood/a15864cab2eed694c754703ad4b73181/raw/test.json)

**Amersham:** The name of a London Underground station which alliterates with "argument parser"

## Motivation

Every CLI application wants two things:

1. Vetted user input
2. Descriptive usage and help messages

Amersham takes care of both with minimal boilerplate.

## Installation

```
user:app$ git clone git@github.com:inigo-selwood/amersham.git
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
        parameter = Parameter("a parameter))
def command(parameter: str, flag: str):
    print(parameter, flag)
```

> Why the duplication? The same could be acheived with type annotations

Take away the decorator, and it's just a normal function. The signature stays descriptive; changing parser is painless.

---

Run the parser

``` python
if __name__ == "__main__":
    parser.run(sys.argv[1:])
```

## Help

Amersham generates descriptive help messages, so you don't have to.

For the application:

```
user:app$ python3 app --help
usage
  app [--help] {command} ...

description
  a parser

commands
  command  a command
```

And for each command:

```
user:app$ python3 app command --help
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

## Overriding Defaults

Amersham infers the names of your commands, arguments, and flag aliases. You can override that behaviour should you want to.

Rename a command:

``` python
@parser.command("a command", name="a-different-name")
def command():
    pass
```

Or a flag/parameter:

``` python
@parser.command("a command",
        flag = Flag("a flag", name="flag-name"),
        parameter = Parameter("a parameter, name="parameter-name"))
def command(parameter: str, flag: str):
    print(parameter, flag)
```