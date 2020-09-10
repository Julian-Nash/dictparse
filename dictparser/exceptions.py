from typing import Any, Union, Optional


class ParserException(Exception):
    ...


class ParserTypeError(ParserException):
    """ Raised when a parameter cannot be parsed to the type defined in DictionaryParser.add_param    """

    def __init__(self, param: str, value: Any):
        self.param = param
        self.value = value
        super().__init__(f"Invalid type '{type(self.value)}' for param '{self.param}'")


class ParserDuplicateParameterError(ParserException):
    """ Raised when a duplicate parameter name is added to DictionaryParser.add_param """

    def __init__(self, param: str):
        self.param = param
        super().__init__(f"Duplicate parameter '{self.param}'")


class ParserRequiredParameterError(ParserException):
    """ Raised when a required parameter is not found """

    def __init__(self, param: str):
        self.param = param
        super().__init__(f"Missing required parameter '{self.param}'")


class ParserInvalidChoiceError(ParserException):
    """ Raised when the parameter value is not in the list of choices added in DictionaryParser.add_param """

    def __init__(self, param: str, value: Any, choices: Union[list, set, tuple]):
        self.param = param
        self.value = value
        self.choices = choices
        super().__init__(f"Parameter '{self.param}' must be one of '{list(choices)}', not '{self.value}'")


class ParserInvalidParameterError(ParserException):
    """ Raised when the parser parses an undefined parameter. Only enforced when strict = True
        in DictionaryParser.parse_params
    """

    def __init__(self, param: str):
        self.param = param
        super().__init__(f"Unrecognised parameter '{self.param}'")
