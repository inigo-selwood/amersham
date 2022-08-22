from amersham import Parser, ParseException


def test_flag():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(flag = None):
        return flag

    # Duplicate name definition
    try:
        overrides = {
            "flag_2": {
                "name": "flag",
            }
        }
        @parser.command(**overrides)
        def command(flag = None, flag_2 = None):
            pass
    except Exception as error:
        assert f"{error}" == "'--flag' already registered in 'command'"
    else:
        assert False

    # Duplicate alias
    try:
        overrides = {
            "flag": {
                "alias": "f",
            },
            "flag_2": {
                "alias": "f",
            }
        }

        @parser.command(**overrides)
        def command(flag = None, flag_2 = None):
            pass
    except Exception as error:
        assert f"{error}" == "'-f' already registered in 'command'"
    else:
        assert False

    # Multiple instances
    try:
        parser.run(["--flag", "--flag"])
    except ParseException as error:
        assert f"{error}" == "'--flag' defined more than once"
    else:
        assert False

    # Unknown flag
    try:
        parser.run(["--bad-flag"])
    except ParseException as error:
        assert f"{error}" == "'--bad-flag' flag unexpected"
    else:
        assert False

    # Invalid flags
    for flag in ["--", "-"]:
        try:
            parser.run([flag])
        except ParseException as error:
            assert f"{error}" == f"'{flag}' flag invalid"
        else:
            assert False

    # Badly formatted value
    try:
        parser.run(["--flag=value0=value1"])
    except ParseException as error:
        assert f"{error}" == f"'--flag' has multiple '=' instances"
    else:
        assert False


def test_flag_untyped():
    parser = Parser("test", raise_exceptions=True)

    overrides = {
        "flag": {
            "alias": "f",
        }
    }
    @parser.command(**overrides)
    def command(flag = None):
        return flag

    # Default
    assert parser.run([]) == False

    # Present
    assert parser.run(["--flag"]) == True
    assert parser.run(["-f"]) == True
    
    # Unexpected value
    try:
        parser.run(["--flag=value"])
    except ParseException as error:
        assert f"{error}" == "'--flag' expects no value"
    else:
        assert False


def test_flag_string():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(flag = ""):
        return flag

    # Default
    assert parser.run([]) == ""

    # Present
    result = parser.run(["--flag=value"])
    assert result == "value"

    # No value
    try:
        parser.run(["--flag="])
    except ParseException as error:
        assert f"{error}" == "'--flag' value specified but empty"
    else:
        assert False


def test_flag_integer():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(flag = 0):
        return flag

    # Default
    assert parser.run([]) == 0

    # Present
    result = parser.run(["--flag=1"])
    assert result == 1

    # Invalid value
    try:
        parser.run(["--flag=one"])
    except ParseException as error:
        assert f"{error}" == "'--flag' expects integer, got 'one'"
    else:
        assert False


def test_flag_boolean():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(flag = False):
        return flag

    # Default
    assert parser.run([]) == False

    # Present, true
    for value in ["1", "yes", "Y", "y", "true"]:
        result = parser.run([f"--flag={value}"])
        assert result == True

    # Present, false
    for value in ["0", "no", "N", "n", "false"]:
        result = parser.run([f"--flag={value}"])
        assert result == False
    
    # Present, invalid
    try:
        parser.run(["--flag=/etc/shadow"])
    except ParseException as error:
        message = "'--flag' expects boolean, got '/etc/shadow'"
        assert f"{error}" == message
    else:
        assert False


def test_flag_list():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(flag = []):
        return flag

    # Default
    assert parser.run([]) == []

    # Present, no values
    assert parser.run(["--flag=[]"]) == []

    # Present, 1 value
    assert parser.run(["--flag=value"]) == ["value"]

    # Present, multiple values
    assert parser.run(["--flag=value0,value1"]) == ["value0", "value1"]

    # Empty value
    try:
        parser.run(["--flag=,value"])
    except ParseException as error:
        message = "'--flag' empty token in list ',value'"
        assert f"{error}" == message
    else:
        assert False