from .dashapp2 import dashapp2_init
from .with_metadata import with_metadata


@with_metadata(title="Dash App Dos", route="/dashapp2/")
def init(flask_app, route):
    return dashapp2_init(flask_app, route)
