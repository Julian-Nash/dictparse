from .exceptions import (
    ParserTypeError,
    ParserInvalidChoiceError,
    ParserRequiredParameterError,
    ParserInvalidParameterError,
    ParserDuplicateParameterError,
    ParserInvalidDataTypeError
)

from typing import Optional, Collection, Callable, List, Any, Union, Dict


class Param(object):

    def __init__(
            self,
            name: str,
            dest: Optional[str] = None,
            type_: Optional[type] = None,
            required: Optional[bool] = False,
            choices: Optional[Collection] = None,
            action: Optional[Callable] = None,
            description: Optional[str] = None,
            default: Optional[Any] = None,
            value: Optional[Any] = None
    ):
        self.name = name
        self.dest = dest or self.name
        self.type_ = type_
        self.required = required
        self.choices = choices or []
        self.action = action
        self.description = description
        self.default = default
        self.value = value


class NameSpace(object):

    def __init__(self, params: List[Param]):
        self._fields: List[str] = []
        self._params: Dict[str, Param] = {}
        for param in params:
            self._fields.append(param.name)
            self._params.update({param.dest or param.name: param})
            setattr(self, param.dest or param.name, param.value)

    def get(self, name: str, default: Optional[Any] = None) -> Union[Any]:
        """ Get a parameter, returns the parameter value or None, unless a default is supplied """
        return getattr(self, name, default)

    def to_dict(self) -> dict:
        """ Returns the NameSpace as a dictionary """
        return {k: getattr(self, k) for k in self._fields if getattr(self, k, None)}


class Parser(object):

    _allowed_types: list = [str, int, float, bool, list, dict, None]

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
            default: Optional[Any] = None
    ) -> None:

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
            default=default
        )

        if param.required:
            self._required_keys.append(name)

        self._params.update({name: param})

    def parse_params(self, data: dict, strict: Optional[bool] = False) -> NameSpace:
        """ Parse a dict of parameters, returns a NameSpace object

        Args:
            data: A dict or dict-like object, raises ValueError if not correct type
            strict: If an undefined parameter is received, raise ParserInvalidParameterError
        Returns:
            NameSpace
        """

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
