"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment


def init_app():
    """
    Construct core Flask application with embedded Dash app.
    """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        # Import parts of our core Flask app
        import routes
        from assets import compile_static_assets

        # Import Dash application
        from .pks.pks import init_dashboard as init_pks
        from .wikimap.wikimap import init_dashboard as init_wikimap

        app = init_pks(app)
        app = init_wikimap(app)

        # Compile static assets
        compile_static_assets(assets)

        return app
