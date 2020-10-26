from .exceptions import (
    ParserTypeError,
    ParserInvalidChoiceError,
    ParserRequiredKeyError,
    ParserInvalidKeyError,
    ParserDuplicateKeyError,
    ParserInvalidDataTypeError
)

from typing import Optional, Callable, List, Any, Union, Dict, Type
from distutils.util import strtobool
import keyword
import re


class Param(object):

    def __init__(
            self,
            name: str,
            type_: Optional[Union[Type[str], Type[int], Type[float], Type[bool], Type[list], Type[dict], Type[set], Type[tuple]]] = None,
            dest: Optional[str] = None,
            required: Optional[bool] = False,
            choices: Optional[Union[list, set, tuple]] = None,
            action: Optional[Callable] = None,
            description: Optional[str] = None,
            default: Optional[Any] = None,
            regex: Optional[str] = None,
            value: Optional[Any] = None
    ):
        """ Param object

        Args:
            name (required): The name of the expected parameter
            type_: The type to convert the parameter to
            dest: The destination attribute name attached to the NameSpace returned
            required: True if the parameter is required, otherwise raises ParserRequiredParameterError
            choices: A list, set or tuple of values which the parameter must be in, otherwise raises
                     ParserInvalidChoiceError
            action: A callable which will be applied to the parameter value
            description: A description of the parameter
            default: A default value for the parameter, defaults to None
            regex: A regular expression string which the parameter value must match, otherwise the value is None
            value: The parameter value, defaults to None
        """
        self.name = name
        self.type_ = type_
        self.dest = dest or self.name
        self.required = required
        self.choices = choices or []
        self.action = action
        self.description = description
        self.default = default
        self.regex = regex
        self.value = value


class NameSpace(object):

    def __init__(self, params: List[Param]):
        """ NameSpace object

        Args:
            params: A list of Param objects
        """
        self._fields: List[str] = []
        self._params: Dict[str, Param] = {}
        for param in params:
            self._fields.append(param.dest or param.name)
            self._params.update({param.dest or param.name: param})
            setattr(self, param.dest or param.name, param.value)

    def get(self, name: str, default: Optional[Any] = None) -> Union[None, Any]:
        """ Get a parameter, returns the parameter value or None, unless a default is supplied """
        return getattr(self, name, default)

    def get_param(self, name: str, default: Optional[Any] = None) -> Union[Param, Any]:
        """ Get a Param, returns the Param object or None, unless a default is supplied """
        return self._params.get(name, default)

    def to_dict(self, exclude: Optional[list] = None) -> dict:
        """ Returns the NameSpace as a dictionary

        Args:
            exclude (list): A list of keys to exclude from the returned dictionary
        """
        exclude = exclude if exclude is not None else []
        return {
            k: getattr(self, k) for k in self._fields if k not in exclude
        }


class DictionaryParser(object):
    """ Dictionary parser class """

    _valid_types: List[type] = [str, int, float, bool, list, tuple, set, dict]

    def __init__(self, description: Optional[str] = None):
        self.description = description
        self._required_keys: List[str] = []
        self._params: Dict[str, Param] = {}

    @staticmethod
    def _is_valid_name(n: str) -> bool:
        """ Test to see if the value for 'name' or 'dest' is allowed when calling add_param """

        if n in ("get", "get_param", "to_dict"):
            return False
        elif n.startswith("__") and n.endswith("__"):
            return False
        elif keyword.iskeyword(n):
            return False
        elif not n.isidentifier():
            return False
        else:
            return True

    def _validate_add_key_params(
            self,
            name: str,
            type_: Optional[Union[Type[str], Type[int], Type[float], Type[bool], Type[list], Type[dict], Type[set], Type[tuple]]],
            dest: Optional[str] = None,
            choices: Optional[Union[list, set, tuple]] = None,
            action: Optional[Callable] = None,
    ):
        """ Validate params when calling add_param """

        if not isinstance(name, str):
            raise TypeError(f"Parameter 'name' must be of type 'str', not '{type(name)}'")

        if not self._is_valid_name(name):
            raise ValueError(
                f"Invalid value '{name}' for parameter 'name'. Must comply with Python variable naming rules"
            )

        if type_ and type_ not in self._valid_types:
            raise TypeError(f"Parameter 'type_' must be one of '{self._valid_types}', not '{type_}'")

        if dest:
            if not isinstance(dest, str):
                raise TypeError(f"Parameter 'dest' must be of type string, not '{type(dest)}'")
            if not self._is_valid_name(dest):
                raise ValueError(
                    f"Invalid value '{dest}' for parameter 'dest'. Must comply with Python variable naming rules"
                )

        if choices and not isinstance(choices, (list, tuple, set)):
            raise TypeError(f"Parameter 'choices' must be of type 'list', 'tuple' or 'set', not '{type(choices)}'")

        if action and not callable(action):
            raise TypeError("Parameter 'action' must be callable")

    def add_param(
            self,
            name: str,
            type_: Optional[Union[Type[str], Type[int], Type[float], Type[bool], Type[list], Type[dict], Type[set], Type[tuple]]] = None,
            dest: Optional[str] = None,
            required: Optional[bool] = False,
            choices: Optional[Union[list, set, tuple]] = None,
            action: Optional[Callable] = None,
            description: Optional[str] = None,
            default: Optional[Any] = None,
            regex: Optional[str] = None
    ) -> None:
        """ Add a key to the parser

        Args:
            name (required): The name of the expected parameter
            type_: The common Python type to convert the parameter to (str, int, float, bool, list, tuple, set, dict)
            dest: The destination attribute name attached to the NameSpace returned
            required: True if the parameter is required, otherwise raises ParserRequiredParameterError
            choices: A list, set or tuple of values which the parameter must be in, otherwise raises
                     ParserInvalidChoiceError
            action: A callable which will be applied to the parameter value
            description: A description of the parameter
            default: A default value for the parameter, defaults to None
            regex: A regular expression string which the parameter value must match, otherwise the value is None
        Returns:
            None
        """

        self._validate_add_key_params(name, type_, dest, choices, action)

        if name in self._params:
            raise ParserDuplicateKeyError(name)

        param: Param = Param(
            name,
            dest=dest,
            type_=type_,
            required=required,
            choices=choices,
            action=action,
            description=description,
            default=default,
            regex=regex
        )

        if param.required:
            self._required_keys.append(name)

        self._params.update({name: param})

    def parse_dict(
            self,
            data: Dict[str, Any],
            strict: Optional[bool] = False,
            action: Optional[Callable] = None
    ) -> NameSpace:
        """ Parse a dictionary or dictionary-like object, returning a NameSpace object

        Args:
            data: A dict or dict-like object. Raises ParserInvalidDataTypeError if not a valid subclass of dict
            strict: If a key not added to the parser is received, raises a ParserInvalidParameterError, defaults to False
            action: A function to apply to all values (applied after type conversion)
        Returns:
            NameSpace
        """

        if not issubclass(type(data), dict):
            raise ParserInvalidDataTypeError(data)

        if action and not callable(action):
            raise TypeError(f"Invalid value for 'map_', must be callable, not '{action}'")

        for r in self._required_keys:
            if r not in data:
                raise ParserRequiredKeyError(r)

        if strict:
            for k in data.keys():
                if k not in self._params.keys():
                    raise ParserInvalidKeyError(k)

        for name, param in self._params.items():

            value: Any = data.get(name)

            if value in ("", None):
                param.value = param.default
                continue

            if param.regex:
                match = re.match(param.regex, str(value))
                if not match:
                    param.value = param.default
                    continue

            if param.type_:
                if param.type_ == bool:
                    try:
                        value = bool(strtobool(str(value)))
                    except ValueError:
                        raise ParserTypeError(name, value, param.type_)
                else:
                    try:
                        value = param.type_(value)
                    except ValueError:
                        raise ParserTypeError(name, value, param.type_)

            if param.action:
                value = param.action(value)

            if param.choices and value not in param.choices:
                raise ParserInvalidChoiceError(name, value, param.choices)

            if action:
                value = action(value)

            param.value = value

        return NameSpace(list(self._params.values()))
