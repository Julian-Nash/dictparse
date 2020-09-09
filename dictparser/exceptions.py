from typing import Any, Union, Optional


class ParserException(Exception):
    ...


class ParserTypeError(ParserException):

    def __init__(self, param: str, value: Any):
        self.param = param
        self.value = value
        super().__init__(f"Invalid type '{type(self.value)}' for param '{self.param}'")


class ParserDuplicateParameterError(ParserException):

    def __init__(self, param: str):
        self.param = param
        super().__init__(f"Duplicate parameter '{self.param}'")


class ParserRequiredParameterError(ParserException):

    def __init__(self, param: str):
        self.param = param
        super().__init__(f"Missing required parameter '{self.param}'")


class ParserInvalidChoiceError(ParserException):

    def __init__(self, param: str, value: Any, choices: Union[list, tuple, set]):
        self.param = param
        self.value = value
        self.choices = choices
        super().__init__(f"Parameter '{self.param}' must be one of '{list(choices)}', not '{self.value}'")


class ParserInvalidParameterError(ParserException):

    def __init__(self, param: str):
        self.param = param
        super().__init__(f"Unrecognised parameter '{self.param}'")


class ParserInvalidDataTypeError(ParserException):

    def __init__(self, data: Any, msg: Optional[str] = None):
        self.data = data
        if msg:
            super().__init__(msg)
        else:
            super().__init__(f"Invalid type for 'data', must be a dict-like object, not '{type(self.data)}'")
