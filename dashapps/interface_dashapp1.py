from .dashapp1 import dashapp1_init
from .dashapp1.metadata import metadata
from src.with_metadata import with_metadata


@with_metadata(
    title=metadata.get("title", "Default title"),
    route=metadata.get("route", "/dashapp1/"),
)
def init(flask_app, route):
    return dashapp1_init(flask_app, route)
