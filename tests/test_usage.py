from amersham import Parser


def test_parser_usage():
    parser = Parser("test", raise_exceptions=True)

    # With one command
    @parser.command()
    def command(parameter: str, flag = ""):
        pass
    assert parser.usage() == """usage
  test [--help] [--flag=] PARAMETER"""

    # With two
    @parser.command()
    def command_2():
        pass
    assert parser.usage() == """usage
  test [--help] {command, command-2} ..."""


def test_command_usage():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(parameter: str, flag = ""):
        pass

    usage = """usage
  test [--help] [--flag=] PARAMETER"""
    assert parser.get_command("command").usage(root=True) == usage