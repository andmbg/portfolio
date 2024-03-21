from .dashapp1 import dashapp1_init
from .with_metadata import with_metadata


@with_metadata(title="Dash App Uno", route="/dashapp1/")
def init(flask_app, route):
    return dashapp1_init(flask_app, route)
