import base64
import os
from flask import Flask, render_template


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

# Import and define apps from submodules here:
from dashapps.pks.pks import init_dashboard
from dashapps.pks import metadata as metadata_pks
from dashapps.dashapp1 import dashapp1_init, metadata_dashapp1
from dashapps.dashapp2 import dashapp2_init, metadata_dashapp2

apps = [
    {
        "app": init_dashboard(flask_app, metadata_pks.get("route", "default")),
        "metadata": metadata_pks,
    },
    {
        "app": dashapp1_init(flask_app, metadata_dashapp1.get("route", "default")),
        "metadata": metadata_dashapp1,
    },
    {
        "app": dashapp2_init(flask_app, metadata_dashapp2.get("route", "default")),
        "metadata": metadata_dashapp2,
    },
]

posts = []

for app_metadata in apps:

    app = app_metadata["app"]
    metadata = app_metadata["metadata"]

    # modify apps to contain the dashapp template:
    with flask_app.test_request_context("/?name=test"):
        app.index_string = render_template(
            "dashapp.html",
            nav_entries=nav_entries,
            title=metadata.get("title", "default title"),
        )

    # define thumbnail entries in posts list:
    posts.append(
        {
            "title": metadata.get("title", "Default title"),
            "route": metadata.get("route", "/default/"),
            "thumbnail_img": read_png_file(metadata.get("thumbnail", None)),
            "synopsis": metadata.get("synopsis", "Default synopsis"),
        }
    )


# Define the index and the post entries:
@flask_app.route("/")
def index():

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
