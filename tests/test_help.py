from amersham import Parser, ParseException


def test_parser_help():
    parser = Parser("test", raise_exceptions=True)

    # With one command, no description
    @parser.command()
    def command(parameter: str, flag = ""):
        pass

    help_message = \
"""usage
  test [--help] [--flag=] PARAMETER

flags
  --help  -h          displays this message
  --flag      string

parameters
  PARAMETER  string"""
    assert parser.help() == help_message

    # With two commands, and description
    @parser.command(description="another command")
    def command_2():
        pass

    help_message = \
"""usage
  test [--help] {command, command-2} ...

flags
  --help  -h  displays this message

commands
  command
  command-2  another command"""
    assert parser.help() == help_message

    # Trailing garbage after "--help"
    for help_string in ["--help", "-h"]:
        try:
            arguments = [help_string, "garbage"]
            parser.run(arguments)
        except ParseException as error:
            assert f"{error}" == f"'{help_string}' followed by other arguments"
        else:
            assert False


def test_command_help():
    parser = Parser("test", raise_exceptions=True)

    @parser.command(name="command",
            description="a command",
            parameter={
                "description": "a parameter",
            },
            _flag={
                "name": "flag",
                "alias": "f",
                "description": "a flag",
            })
    def callback(parameter: str, _flag = ""):
        pass

    help_message = \
"""usage
  test [--help] [--flag=] PARAMETER

description
  a command

flags
  --help  -h          displays this message
  --flag  -f  string  a flag

parameters
  PARAMETER  string  a parameter"""
    assert parser.get_command("command").help(root=True) == help_message

    # Trailing garbage after "--help"
    for help_string in ["--help", "-h"]:
        try:
            arguments = [help_string, "garbage"]
            parser.get_command("command").run(arguments, root=True)
        except ParseException as error:
            assert f"{error}" == f"'{help_string}' followed by other arguments"
        else:
            assert False
