import base64
import os
from flask import Flask, render_template

import dashapps.interface_dashapp1
import dashapps.interface_dashapp2
import dashapps.interface_pks
from dashapps.pks.pks import init_dashboard
from dashapps.pks.metadata import metadata as metadata_pks


flask_app = Flask(__name__)

dashapps.interface_dashapp1.init(flask_app)
dashapps.interface_dashapp2.init(flask_app)
pksapp = init_dashboard(flask_app, "/pks/")

nav_entries = {
    "Home": "/",
    "Contact": "/contact",
}

with flask_app.test_request_context("/?name=test"):
    pksapp.index_string = render_template(
        "dashapp.html",
        nav_entries=nav_entries,
        title="Polizeiliche Kriminalstatistik"
    )

@flask_app.route("/")
def index():

    posts = []

    def read_png_file(file_path):
        if file_path is None:
            return None

        with open(file_path, "rb") as file:
            png_content = base64.b64encode(file.read()).decode("utf-8")
        return png_content

    # Iterate through interface files
    for module_name in dir(dashapps):
        if module_name.startswith("interface_"):
            module = getattr(dashapps, module_name)
            if hasattr(module, "metadata"):
                metadata = module.metadata
                route = metadata.get("route")
                thumbnailpath = metadata.get("thumbnail")

                if thumbnailpath:
                    metadata["thumbnail"] = read_png_file(
                        "dashapps"
                        + metadata.get("route", "")
                        + metadata.get("thumbnail", "")
                    )
                else:
                    metadata["thumbnail"] = read_png_file("static/none.png")

                if route:
                    posts += [metadata]

    # add a small rotation and side shift to each post:
    for i, post in enumerate(posts):
        post["rotation"] = (2*(i % 2) - 1) * 3
        post["offset"] = [2, 5, 1, 4, 3][i % 5]

    return render_template(
        "index.html",
        intro="Lorem ipsum",
        nav_entries=nav_entries,
        posts=posts,
    )


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8080, debug=True)
