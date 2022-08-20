from amersham import Command, Flag, Parameter


def test_create():

    def callback(parameter: str, flag: str = ""):
        pass

    # Simple command
    definitions = {
        "parameter": Parameter("a parameter"),
        "flag": Flag("a flag")
    }

    command = Command("a command", 
            "test", 
            callback, 
            definitions)
    
    assert command.name == "callback"
    assert command._flags
    assert command._parameters

    flag = command._flags[0]
    assert flag.name == "flag"
    assert flag.alias == "f"
    assert flag.value_count == 1

    parameter = command._parameters[0]
    assert parameter.name == "parameter"

    # Command with name overrides
    definitions = {
        "parameter": Parameter("a parameter", name="renamed-parameter"),
        "flag": Flag("a flag", alias="fl", name="renamed-flag")
    }

    command = Command("a command", 
            "test", 
            callback, 
            definitions,
            command_name="renamed-command")
    
    assert command.name == "renamed-command"
    assert command._parameters[0].name == "renamed-parameter"

    flag = command._flags[0]
    assert flag.name == "renamed-flag"
    assert flag.alias == "fl"

    # Command with no flag parameters
    def callback(flag: bool):
        pass

    definitions = {"flag": Flag("a flag")}
    command = Command("a command", 
            "test", 
            callback, 
            definitions)
    
    assert command._flags[0].value_count == 0

    # Command with flag parameter count override
    definitions = {"flag": Flag("a flag", value_count=1)}
    command = Command("a command", 
            "test", 
            callback, 
            definitions)
    
    assert command._flags[0].value_count == 1

    # Undefined flag
    try:
        command = Command("a command", 
                "test", 
                callback, 
                {})
    except Exception as error:
        assert error.__str__() == "'flag' undefined"
    else:
        assert False
    
    # Multiple flags with same name
    try:
        def callback(flag: bool, other_flag: bool):
            pass
        
        definitions = {
            "flag": Flag("a flag"),
            "other_flag": Flag("another flag", name="flag"),
        }
        command = Command("a command", 
                "test", 
                callback, 
                definitions)
    except Exception as error:
        assert error.__str__() == "'callback' already has flag 'flag'"
    else:
        assert False
    
    # No default for flag
    try:
        def callback(flag: str):
            pass
        
        definitions = {"flag": Flag("a flag")}
        command = Command("a command", 
                "test", 
                callback, 
                definitions)
    except Exception as error:
        assert error.__str__() == "'--flag' has no default value"
    else:
        assert False

    # Multiple definitions of same parameter name
    try:
        def callback(parameter: str, parameter1: str):
            pass
    
        definitions = {
            "parameter": Parameter("a parameter"),
            "parameter1": Parameter("another parameter", name="parameter"),
        }

        command = Command("a command", 
                "test", 
                callback, 
                definitions)
    except Exception as error:
        message = "'callback' already has parameter 'parameter'"
        assert error.__str__() == message
    else:
        assert False
    
    # Invalid definition type
    try:
        def callback(parameter: str):
            pass

        definitions = {"parameter": str}
        command = Command("a command", 
                "test", 
                callback, 
                definitions)
    except Exception as error:
        assert error.__str__() == "'parameter' definition not Flag or Parameter"
    else:
        assert False


def test_usage():

    def callback(parameter: str, flag: bool, other_flag: str = ""):
        pass

    definitions = {
        "parameter": Parameter("a parameter"),
        "flag": Flag("a flag"),
        "other_flag": Flag("another flag"),
    }

    command = Command("a command", "test", callback, definitions)

    assert command._usage() == """usage
  test callback [--help] [--flag] [--other-flag=_] PARAMETER"""


def test_help():

    def callback(parameter: str, flag: bool, other_flag: str = ""):
        pass

    definitions = {
        "parameter": Parameter("a parameter"),
        "flag": Flag("a flag"),
        "other_flag": Flag("another flag"),
    }

    command = Command("a command", "test", callback, definitions)

    assert command._help() == """usage
  test callback [--help] [--flag] [--other-flag=_] PARAMETER

description
  a command

flags
  --help        -h  displays this message
  --flag        -f  a flag
  --other-flag  -o  another flag

parameters
  parameter  a parameter"""


def test_parse():

    # Basic usage
    def callback(parameter: str, flag: str = ""):
        return (flag, parameter)

    definitions = {
        "parameter": Parameter("a parameter"),
        "flag": Flag("a flag"),
    }
    command = Command("a command", "test", callback, definitions)

    arguments = ["--flag=flag", "parameter"]
    assert command._parse(arguments) == ("flag", "parameter")