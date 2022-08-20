from amersham import Flag


def test_create_flag():
    flag = Flag("a flag", name="A_Flag")
    assert flag.name == "a-flag"


def test_parse_flag():

    # Basic flag or alias
    name, is_alias, value = Flag.parse("--flag")
    assert name == "flag"
    assert not is_alias
    assert not value

    name, is_alias, value = Flag.parse("-f")
    assert name == "f"
    assert is_alias
    assert not value

    # Flag with value
    name, is_alias, value = Flag.parse("--flag=value")
    assert name == "flag"
    assert not is_alias
    assert value == "value"

    name, is_alias, value = Flag.parse("-f=value")
    assert name == "f"
    assert is_alias
    assert value == "value"

    # Flag with multiple value tokens
    name, is_alias, value = Flag.parse("--flag=value0,value1")
    assert name == "flag"
    assert not is_alias
    assert value == ["value0", "value1"]

    # Multiple assignments
    try:
        name, is_alias, value = Flag.parse("--flag=value0=value1")
    except Exception as error:
        message = "multiple '=' instances in '--flag=value0=value1'"
        assert error.__str__() == message

    # Invalid flags ('--' and '-')
    try:
        name, is_alias, value = Flag.parse("--")
    except Exception as error:
        message = "invalid flag '--'"
        assert error.__str__() == message

    try:
        name, is_alias, value = Flag.parse("-")
    except Exception as error:
        message = "invalid flag '-'"
        assert error.__str__() == message

    # Empty value
    try:
        name, is_alias, value = Flag.parse("--flag=")
    except Exception as error:
        message = "empty value in '--flag='"
        assert error.__str__() == message

    # Empty value token
    try:
        name, is_alias, value = Flag.parse("--flag=value0,")
    except Exception as error:
        message = "empty value token in '--flag=value0,'"
        assert error.__str__() == message