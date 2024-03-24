from .pks.pks import init_dashboard
from .pks.metadata import metadata
from src.with_metadata import with_metadata


@with_metadata(title=metadata.get("title", "Default title"), route=metadata.get("route", "/default/"))
def init(flask_app, route):
    return init_dashboard(flask_app, route)
