from amersham import Parser, Command


def test_parser_help():
    parser = Parser("test")

    def help():
        return parser.help()
    parser.help_callback = help

    # With one command, no details
    @parser.command()
    def command(parameter: str, flag = ""):
        pass

    help_message = \
"""usage
  test [--help] [--flag=] PARAMETER

flags
  --help  -h          displays this message
  --flag  -f  string

parameters
  PARAMETER  string"""
    assert parser.run(["--help"]) == help_message

    # With two commands, and some details
    @parser.command(detail="another command")
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
    assert parser.run(["--help"]) == help_message


def test_command_help():
    parser = Parser("test")

    def help(command: Command):
        return command.help()

    @parser.command(name="command",
            detail="a command",
            help_callback=help,
            parameter={
                "detail": "a parameter",
            },
            flag={
                "detail": "a flag",
            })
    def callback(parameter: str, flag = ""):
        pass

    help_message = \
"""usage
  test command [--help] [--flag=] PARAMETER

description
  a command

flags
  --help  -h          displays this message
  --flag  -f  string  a flag

parameters
  parameter  string  a parameter"""
    assert parser.run(["--help"]) == help_message
