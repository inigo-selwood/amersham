from amersham import Parser, ParseException


def test_run():
    
    parser = Parser("test", raise_exceptions=True)

    # No commands registered
    try:
        parser.run(["command"])
    except Exception as error:
        assert f"{error}" == "no registered commands"
    else:
        assert False

    # Arguments out-of-order
    @parser.command()
    def command(parameter, flag = None):
        pass
    
    try:
        parser.run(["parameter", "--flag"])
    except ParseException as error:
        assert f"{error}" == "'--flag' follows a parameter"
    else:
        assert False
    
    # Multiple command registrations
    try:

        @parser.command(name="command")
        def command_2():
            pass
    
    except Exception as error:
        assert f"{error}" == "'command' already registered"
    else:
        assert False
    
    # Empty argument
    try:
        parser.run([""])
    except ParseException as error:
        assert f"{error}" == "empty argument"
    else:
        assert False
    
    # Unrecognized command
    @parser.command()
    def other_command():
        pass
    
    try:
        parser.run(["bad-command"])
    except ParseException as error:
        assert f"{error}" == "unrecognized command 'bad-command'"
    else:
        assert False


    # Flag in place of command
    try:
        parser.run(["--flag-not-command"])
    except ParseException as error:
        assert f"{error}" == "expected command, not '--flag-not-command'"
    else:
        assert False
    