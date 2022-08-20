from amersham import Parser


def test_parser_usage():

    # Parser with no commands
    parser = Parser("parser", "a parser")
    assert parser._usage() == "usage\n  parser [--help]"

    # With one command
    @parser.command("a command", name="command")
    def callback():
        pass
    assert parser._usage() == "usage\n  parser [--help] {command} ..."

    # And with two
    @parser.command("another command", name="command-2")
    def other_callback():
        pass
    usage = "usage\n  parser [--help] {command, command-2} ..."
    assert parser._usage() == usage


def test_parser_help():

    # Parser with no commands
    parser = Parser("parser", "a parser")
    assert parser._help() == """usage
  parser [--help]

description
  a parser

flags
  --help  -h  displays this message"""

    # With one command
    @parser.command("a command", name="command")
    def callback():
        pass
    assert parser._help() == """usage
  parser [--help] {command} ...

description
  a parser

flags
  --help  -h  displays this message

commands
  command  a command"""

    # And with two
    @parser.command("another command", name="command-2")
    def other_callback():
        pass
    usage = "usage\n  parser [--help] {command, command-2} ..."
    assert parser._help() == """usage
  parser [--help] {command, command-2} ...

description
  a parser

flags
  --help  -h  displays this message

commands
  command    a command
  command-2  another command"""


def test_parser_run():

    parser = Parser("parser", "a parser")

    # Empty input
    try:
        parser.run([])
    except Exception as error:
        assert error.__str__() == "expected a command"

    # Trailing garbage after help flag
    try:
        parser.run(["--help", "stuff"])
    except Exception as error:
        assert error.__str__() == "'--help' expects no arguments"

    try:
        parser.run(["-h", "stuff"])
    except Exception as error:
        assert error.__str__() == "'-h' expects no arguments"
    
    # Flag instead of command
    try:
        parser.run(["--flag"])
    except Exception as error:
        assert error.__str__() == "unexpected flag '--flag'"
    
    # Unknown command
    try:
        parser.run(["command"])
    except Exception as error:
        assert error.__str__() == "unrecognized command 'command'"