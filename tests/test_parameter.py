from amersham import Parser, ParseException


def test_parameter():

    # Multiple definition
    parser = Parser("test", raise_exceptions=True)

    try:
        overrides = {
            "parameter_2": {
                "name": "parameter",
            }
        }
        @parser.command(**overrides)
        def command(parameter, parameter_2):
            pass
    except Exception as error:
        assert f"{error}" == "'parameter' already registered in 'command'"
    else:
        assert False


def test_parameter_untyped():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(parameter, other_parameter):
        return (parameter, other_parameter)

    # Default
    assert parser.run(["value0", "value1"]) == ("value0", "value1")

    # One not present
    try:
        parser.run(["value"])
    except ParseException as exception:
        assert exception.__str__() == "expected 'other-parameter'"
    else:
        assert False

    # Two not present
    try:
        parser.run([])
    except ParseException as exception:
        message = "expected 'parameter', 'other-parameter'"
        assert exception.__str__() == message
    else:
        assert False

    # Unexpected
    try:
        parser.run(["parameter", "other-parameter", "third-parameter"])
    except ParseException as exception:
        assert exception.__str__() == "unexpected parameter 'third-parameter'"
    else:
        assert False


def test_parameter_string():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(parameter: str):
        return parameter

    # Default
    assert parser.run(["value"]) == "value"


def test_parameter_integer():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(parameter: int):
        return parameter

    # Default
    assert parser.run(["0"]) == 0
    assert parser.run(["1"]) == 1

    # Invalid value
    try:
        parser.run(["one"])
    except ParseException as exception:
        message = "'parameter' expects integer, got 'one'"
        assert exception.__str__() == message
    else:
        assert False


def test_parameter_boolean():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(parameter: bool):
        return parameter
    
    # Present, true
    for value in ["1", "yes", "Y", "y", "true"]:
        result = parser.run([value])
        assert result == True

    # Present, false
    for value in ["0", "no", "N", "n", "false"]:
        result = parser.run([value])
        assert result == False
    
    # Present, invalid
    try:
        parser.run(["/etc/shadow"])
    except ParseException as exception:
        message = "'parameter' expects boolean, got '/etc/shadow'"
        assert exception.__str__() == message
    else:
        assert False


def test_parameter_list():
    parser = Parser("test", raise_exceptions=True)

    @parser.command()
    def command(parameter: list):
        return parameter

    # Present, no values
    assert parser.run(["[]"]) == []

    # Present, 1 value
    assert parser.run(["value"]) == ["value"]

    # Present, multiple values
    assert parser.run(["value0,value1"]) == ["value0", "value1"]