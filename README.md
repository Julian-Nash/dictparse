# dictparser

A simple, slim and useful, zero-dependency utility for parsing JSON strings, dictionaries or dictionary-like objects
 (think Flask's `request.form`, `request.json` or `request.get_json()`).

`dictparser` borrows a slimmed down design from Python's own `argparse` library, similar to the `ArgumentParser` class
, taking input as a dictionary like object or a dictionary string as JSON, enforcing rules, types, actions, default
 values and returning a `NameSpace`, with values mapped to attributes.
 
### Installation

```shell script
pip install requestparser
```

### Usage


### Flask example

An example of parsing JSON data sent in a POST request to a Flask route:

```py3
from app.users import create_user

from flask import Flask, request
from respond import JSONResponse
from dictparser import DictionaryParser


def create_app():

    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def post():

        parser = DictionaryParser(description="Create a new user")

        parser.add_param("name", str, required=True)
        parser.add_param("age", int)
        parser.add_param("password", str, required=True, action=lambda x: x.encode("utf-8"))
        parser.add_param("interests", list, action=lambda x: [i.strip() for i in x])
        parser.add_param("level", float, default=1.5)
        parser.add_param("stage", str, choices=["alpha", "beta"])

        try:
            params = parser.parse_params(request.get_json())
        except Exception as e:
            return JSONResponse.bad_request(str(e))

        user = create_user(
            name=params.name,
            age=params.age,
            password=params.password,
            interests=params.interests,
            level=params.level,
            stage=params.stage
        )

        return JSONResponse.created(user.to_dict())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()

```