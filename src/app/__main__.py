from dotenv import load_dotenv
from flask import Flask
from flask_toastr import Toastr

import middlewares
import routes
from infrastructure.config.parsers import load_config
from infrastructure.database.session import create_sqlite_session_maker
from infrastructure.log.main import configure_logging


def main() -> Flask:
    load_dotenv()
    config = load_config()
    configure_logging(config.app_config)
    session_maker = create_sqlite_session_maker(config.db_config.full_url)

    app = Flask(__name__)

    app.secret_key = 'Secret key'  # TODO
    middlewares.register(app, session_maker)
    routes.register(app)
    toastr = Toastr()
    toastr.init_app(app)

    return app


def run():
    app = main()
    app.run("localhost", 5000)


if __name__ == "__main__":
    run()
