from .dashapp2 import dashapp2_init
from .dashapp2.metadata import metadata
from src.with_metadata import with_metadata


@with_metadata(
    title=metadata.get("title", "Default title"),
    route=metadata.get("route", "/dashapp2/"),
)
def init(flask_app, route):
    return dashapp2_init(flask_app, route)
