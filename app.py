import os
from flask import Flask, render_template
import dashapps.interface_dashapp1
import dashapps.interface_dashapp2
import dashapps.interface_pks
# from dashapps.dashapp1 import dashapp1_init

flask_app = Flask(__name__)

dashapps.interface_pks.init(flask_app)
dashapps.interface_dashapp1.init(flask_app)
dashapps.interface_dashapp2.init(flask_app)

@flask_app.route("/")
def index():

    nav_entries = {
        "Home": "/",
        "Contact": "/contact",
    }

    posts = []

    # Iterate through interface files
    for module_name in dir(dashapps):
        if module_name.startswith("interface_"):
            module = getattr(dashapps, module_name)
            if hasattr(module, "metadata"):
                metadata = module.metadata
                route = metadata.get("route")
                if route:
                    posts += [metadata]

    for post in posts:
        print(post.get("route", "(route)") + post.get("thumbnail", "(thumb)"))

    return render_template(
        "index.html",
        intro="Lorem ipsum",
        nav_entries=nav_entries,
        posts=posts,
    )


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8080, debug=True)
