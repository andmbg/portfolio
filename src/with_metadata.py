def with_metadata(**metadata):
    """
    Decorator function that adds metadata to a Dash app.

    Args:
        **metadata: Keyword arguments representing the metadata to be added.

    Returns:
        A decorator function that takes an initialization function as input and returns a wrapped function.

    Example:
        @with_metadata(route="/myapp", title="My App")
        def init_app(flask_app, route):
            dash_app = Dash(__name__, server=flask_app, url_base_pathname=route)
            # Initialize the Dash app
            return dash_app
    """
    def decorator(init_func):
        def wrapper(flask_app):
            dash_app = init_func(flask_app, metadata.get('route', '/'))
            with open("templates/dashapp.html") as file:
                dash_app.index_string = file.read()
                for k, v in metadata.items():
                    dash_app.index_string = dash_app.index_string.replace(
                        f"{{{{{k}}}}}", v
                    )
            return dash_app

        return wrapper

    return decorator