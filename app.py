from pathlib import Path
import sys
import base64

from flask import Flask, render_template
import markdown


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
    "Start": "/",
    "Kontakt": "/contact",
}

# Add base directory of pks
pks_base_dir = Path(__file__).resolve().parent / 'dashapps' / 'pks'
if pks_base_dir.exists() and str(pks_base_dir) not in sys.path:
    sys.path.insert(0, str(pks_base_dir))

# Add base directory of elternsein
elternsein_base_dir = Path(__file__).resolve().parent / 'dashapps' / 'elternsein'
if elternsein_base_dir.exists() and str(elternsein_base_dir) not in sys.path:
    sys.path.insert(0, str(elternsein_base_dir))


# Import and define apps from submodules here:
from dashapps.pks.pks import init_dashboard as init_pks
from dashapps.pks import metadata as metadata_pks

from dashapps.elternsein.elternsein import init_dashboard as init_elternsein
from dashapps.elternsein import metadata as metadata_elternsein

from dashapps.bundestag.bundestag import init_dashboard as init_bundestag
from dashapps.bundestag import metadata as metadata_bundestag

apps = [
    {
        "app": init_pks(flask_app, metadata_pks.get("route", "default")),
        "metadata": metadata_pks,
    },
    {
        "app": init_elternsein(flask_app, metadata_elternsein.get("route", "default")),
        "metadata": metadata_elternsein,
    },
    {
        "app": init_bundestag(flask_app, metadata_bundestag.get("route", "default")),
        "metadata": metadata_bundestag,
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
    
    with open("static/prose/intro.md", "r") as file:
        intro = markdown.markdown(file.read())

    # add a small rotation and side shift to each post:
    for i, post in enumerate(posts):
        post["rotation"] = (2 * (i % 2) - 1) * 3
        post["offset"] = [2, 5, 1, 4, 3][i % 5]

    return render_template(
        "index.html",
        intro=intro,
        nav_entries=nav_entries,
        posts=posts,
    )

@flask_app.route("/contact")
def contact():

    return render_template(
        "contact.html",
        nav_entries=nav_entries,
    )


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
