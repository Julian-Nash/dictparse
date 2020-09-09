from .exceptions import (
    ParserTypeError,
    ParserInvalidChoiceError,
    ParserRequiredParameterError,
    ParserInvalidParameterError,
    ParserDuplicateParameterError,
    ParserInvalidDataTypeError
)

from typing import Optional, Collection, Callable, List, Any, Union, Dict
from json.decoder import JSONDecodeError
import json
import re


class Param(object):

    def __init__(
            self,
            name: str,
            type_: Optional[type] = None,
            dest: Optional[str] = None,
            required: Optional[bool] = False,
            choices: Optional[Collection] = None,
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
            self._fields.append(param.name)
            self._params.update({param.dest or param.name: param})
            setattr(self, param.dest or param.name, param.value)

    def get(self, name: str, default: Optional[Any] = None) -> Union[None, Any]:
        """ Get a parameter, returns the parameter value or None, unless a default is supplied """
        return getattr(self, name, default)

    def get_param(self, name: str, default: Optional[Any] = None) -> Union[Param, Any]:
        """ Get a Param, returns the Param object or None, unless a default is supplied """
        return self._params.get(name, default)

    def to_dict(self) -> dict:
        """ Returns the NameSpace as a dictionary """
        return {k: getattr(self, k) for k in self._fields if getattr(self, k, None)}


class DictionaryParser(object):
    """ Dictionary parser class """

    def __init__(self, description: Optional[str] = None):
        self.description = description
        self._required_keys: List[str] = []
        self._params: Dict[str, Param] = {}

    def _validate_add_param_opts(
            self,
            name: str,
            type_: Optional[type] = None,
            dest: Optional[str] = None,
            choices: Optional[Union[list, set, tuple]] = None,
            action: Optional[Callable] = None,
    ):
        """ Validate params passed into add_param """
        if not isinstance(name, str):
            raise TypeError(f"Parameter 'name' must be of type 'str', not '{type(name)}'")

        if type_ and not isinstance(type_, type):
            raise TypeError(f"Parameter 'type_' must be a valid type, not '{type(type_)}'")

        if dest and not isinstance(dest, str):
            raise TypeError(f"Parameter 'dest' must be of type string, not '{type(dest)}'")

        if choices and not isinstance(choices, (list, tuple, set)):
            raise TypeError("Parameter 'choices' must be of type 'list', 'tuple' or 'set'")

        if action and not callable(action):
            raise TypeError("Parameter 'action' must be callable")

    def add_param(
            self,
            name: str,
            type_: Optional[type] = None,
            dest: Optional[str] = None,
            required: Optional[bool] = False,
            choices: Optional[Union[list, set, tuple]] = None,
            action: Optional[Callable] = None,
            description: Optional[str] = None,
            default: Optional[Any] = None,
            regex: Optional[str] = None
    ) -> None:
        """ Add a parameter to the parser

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
        Returns:
            None
        """

        self._validate_add_param_opts(name, type_, dest, choices, action)

        if name in self._params:
            raise ParserDuplicateParameterError(name)

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

    def parse_params(self, data: Union[dict, str], strict: Optional[bool] = False) -> NameSpace:
        """ Parse a dictionary or dictionary-like object of parameters, returning a NameSpace object

        Args:
            data: A dict or dict-like object. Raises ParserInvalidDataTypeError if not correct type, can also be a
                  JSON string as long as it can be decoded to a dict
            strict: If an undefined parameter is received, raises a ParserInvalidParameterError, defaults to False
        Returns:
            NameSpace
        """

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except JSONDecodeError:
                raise ParserInvalidDataTypeError(
                    "Invalid JSON string for param 'data'. Could not decode JSON to dict"
                )

        if not issubclass(type(data), dict):
            raise ParserInvalidDataTypeError(data)

        for r in self._required_keys:
            if r not in data:
                raise ParserRequiredParameterError(r)

        if strict:
            for k in data.keys():
                if k not in self._params.keys():
                    raise ParserInvalidParameterError(k)

        for name, param in self._params.items():

            value: Any = data.get(name)

            if not value:
                param.value = param.default
                continue

            if param.regex:
                match = re.match(param.regex, str(value))
                if not match:
                    param.value = param.default
                    continue

            if param.type_:
                try:
                    value = param.type_(value)
                except TypeError:
                    raise ParserTypeError(name, value)

            if param.action:
                value = param.action(value)

            if param.choices and value not in param.choices:
                raise ParserInvalidChoiceError(name, value, param.choices)

            param.value = value

        return NameSpace(list(self._params.values()))
