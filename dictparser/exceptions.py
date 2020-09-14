from typing import Any, Union, Optional


class ParserException(Exception):

    def _get_type_str(self, v: Any, from_type: Optional[bool] = False) -> Union[str, None]:
        m: dict = {
            str: "str",
            int: "int",
            float: "float",
            bool: "bool",
            list: "list",
            tuple: "list",
            set: "list",
            dict: "dict",
        }
        if from_type:
            return m.get(v, None)
        else:
            return m.get(type(v))


class ParserTypeError(ParserException):
    """ Raised when a parameter cannot be parsed to the type defined in DictionaryParser.add_param    """

    def __init__(self, param: str, value: Any, expected: Optional[type] = None):
        self.param = param
        self.value = value
        if expected:
            super().__init__(
                f"Invalid value '{self.value}' for parameter '{self.param}', expected "
                f"'{self._get_type_str(expected, from_type=True)}' not '{self._get_type_str(self.value)}'"
            )
        else:
            super().__init__(
                f"Invalid value '{self.value}' for parameter '{self.param}', expected"
                f" '{self._get_type_str(type(self.value))}'"
            )


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
        super().__init__(f"Invalid parameter '{self.param}'")


class ParserInvalidDataTypeError(ParserException, TypeError):
    """ Raised when `parse_params` is not given a dict or dict-like object for `data` """

    def __init__(self, data: Any):
        self.param = data
        super().__init__(f"Invalid type for 'data', must be a dict or dict-like object, not "
                         f"'{self._get_type_str(data)}'")
