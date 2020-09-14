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
            params = parser.parse_dict(request.get_json())
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
