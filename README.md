# requestparser

A simple, slim and useful, zero dependency parser for parsing dictionaries or dictionary-like objects (think Flask's
 `request.form`, `request.json` or `request.get_json()`).

`requestparser` borrows inspiration from Python's own `argparse` library similar to the `ArgumentParser` class
, taking input as a dictionary like object, enforcing rules, types, actions, default values and returning a
 `NameSpace`, with values mapped to attributes.
 
### Installation

```shell script
pip install requestparser
```

### Usage

```py3
from requestparser import Parser

parser = Parser(description="Create a new user")

parser.add_param("name", str, required=True)
parser.add_param("age", int)
parser.add_param("password", str, required=True, action=lambda x: x.encode("utf-8"))
parser.add_param("interests", list, action=lambda x: [i.strip() for i in x])
parser.add_param("level", float, default=1.5)
parser.add_param("stage", str, choices=["alpha", "beta"])

parser.parse_args(
    {
        "name": "foo", 
        "password": "123", 
        "interests": ["cats ", "dogs"], 
        "stage": "production"
    }
)

```