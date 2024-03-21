from .pks.pks import init_dashboard
from .with_metadata import with_metadata


@with_metadata(title="Crime Stats", route="/pks/")
def init(flask_app, route):
    return init_dashboard(flask_app, route)
