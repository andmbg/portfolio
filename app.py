import base64
import os
from flask import Flask, render_template

from dashapps.pks.pks import init_dashboard
from dashapps.pks.metadata import metadata as metadata_pks
from dashapps.dashapp1 import dashapp1_init
from dashapps.dashapp1.metadata import metadata as metadata_dashapp1
from dashapps.dashapp2 import dashapp2_init
from dashapps.dashapp2.metadata import metadata as metadata_dashapp2


def read_png_file(file_path):
    """
    Return content of a png file as base64.
    """
    if file_path is None:
        return None

    with open(file_path, "rb") as file:
        png_content = base64.b64encode(file.read()).decode("utf-8")
    return png_content


flask_app = Flask(__name__)


nav_entries = {
    "Home": "/",
    "Contact": "/contact",
}

# NOTE: Wahrscheinlich müssen die Apps in ein Dict, dessen Werte ich als Variableninhalte behandeln kann, damit ich darüber iterieren kann.
# NOTE: + die Metadaten könnten in die __init__ der Dash-Apps verschoben werden, das spart beim Import.

# Initialize the Dash apps:
db1app = dashapp1_init(flask_app, metadata_dashapp1.get("route"))
db2app = dashapp2_init(flask_app, metadata_dashapp2.get("route"))
pksapp = init_dashboard(flask_app, metadata_pks.get("route"))

# For each Dash app, set the index_string to the content of the template file:
with flask_app.test_request_context("/?name=test"):
    pksapp.index_string = render_template(
        "dashapp.html", nav_entries=nav_entries, title="Polizeiliche Kriminalstatistik"
    )
with flask_app.test_request_context("/?name=test"):
    db1app.index_string = render_template(
        "dashapp.html", nav_entries=nav_entries, title="Dash App 1"
    )
with flask_app.test_request_context("/?name=test"):
    db2app.index_string = render_template(
        "dashapp.html", nav_entries=nav_entries, title="Dash App 2"
    )


# Define the index route:
@flask_app.route("/")
def index():

    posts = []
    posts.append(
        {
            "title": metadata_pks.get("title", "Default title"),
            "route": metadata_pks.get("route", "/default/"),
            "thumbnail_img": read_png_file(
                "dashapps/pks/" + metadata_pks.get("thumbnail", None)
            ),
            "synopsis": metadata_pks.get("synopsis", "Default synopsis"),
        }
    )
    posts.append(
        {
            "title": metadata_dashapp1.get("title", "Default title"),
            "route": metadata_dashapp1.get("route", "/default/"),
            "thumbnail_img": read_png_file(metadata_dashapp1.get("thumbnail", None)),
            "synopsis": metadata_dashapp1.get("synopsis", "Default synopsis"),
        }
    )
    posts.append(
        {
            "title": metadata_dashapp2.get("title", "Default title"),
            "route": metadata_dashapp2.get("route", "/default/"),
            "thumbnail_img": read_png_file(metadata_dashapp2.get("thumbnail", None)),
            "synopsis": metadata_dashapp2.get("synopsis", "Default synopsis"),
        }
    )

    # add a small rotation and side shift to each post:
    for i, post in enumerate(posts):
        post["rotation"] = (2 * (i % 2) - 1) * 3
        post["offset"] = [2, 5, 1, 4, 3][i % 5]

    return render_template(
        "index.html",
        intro="Lorem ipsum",
        nav_entries=nav_entries,
        posts=posts,
    )


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8080, debug=True)
