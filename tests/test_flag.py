from amersham import Parser, ParseException


def test_flag():
    parser = Parser("test")

    @parser.command()
    def command(flag = None):
        return flag

    # Redefinition
    try:
        parser.run(["--flag", "--flag"])
    except ParseException as exception:
        assert exception.__str__() == "multiple '--flag' instances"
    else:
        assert False

    # Unknown flag
    try:
        parser.run(["--bad-flag"])
    except ParseException as exception:
        assert exception.__str__() == "unexpected flag '--bad-flag'"
    else:
        assert False

    # Invalid flags
    for flag in ["--", "-"]:
        try:
            parser.run([flag])
        except ParseException as exception:
            assert exception.__str__() == f"invalid flag '{flag}'"
        else:
            assert False


def test_flag_untyped():
    parser = Parser("test")

    @parser.command()
    def command(flag = None):
        return flag

    # Default
    assert parser.run([]) == False

    # Present
    result = parser.run(["--flag"]) == True
    assert isinstance(result, bool)
    assert result == True
    
    # Unexpected value
    try:
        parser.run(["--flag=value"])
    except ParseException as exception:
        assert exception.__str__() == "'--flag' expects no value"
    else:
        assert False


def test_flag_string():
    parser = Parser("test")

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
    except ParseException as exception:
        assert exception.__str__() == "'--flag' expects a value"
    else:
        assert False


def test_flag_integer():
    parser = Parser("test")

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
    except ParseException as exception:
        assert exception.__str__() == "'--flag' expects integer, got 'one'"
    else:
        assert False


def test_flag_boolean():
    parser = Parser("test")

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
    except ParseException as exception:
        message = "'--flag' expects boolean, got '/etc/shadow'"
        assert exception.__str__() == message
    else:
        assert False


def test_flag_list():
    parser = Parser("test")

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
    except ParseException as exception:
        message = "empty value in flag list '--flag=,value'"
        assert exception.__str__() == message
    else:
        assert False