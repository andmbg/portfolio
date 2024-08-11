import importlib
from flask import Flask, render_template, request, session, url_for, redirect, g
import markdown
import base64


def read_png_file(file_path):
    if file_path is None:
        return None
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key_here"

    nav_entries = {
        "Start": "/",
        "Kontakt": "/contact",
    }

    app_dirs = [
        # "pks",
        # "bundestag",
        "wikimap",
        "elternsein",
    ]
    dash_apps = {"en": [], "de": []}

    for lang in ["en", "de"]:
        for app_dir in app_dirs:
            module = importlib.import_module(f"dashapps.{lang}.{app_dir}.{app_dir}")
            metadata = importlib.import_module(f"dashapps.{lang}.{app_dir}").metadata
            dash_app = module.init_dashboard(app, metadata.get("route", f"/{app_dir}/"))
            dash_apps[lang].append({"app": dash_app, "metadata": metadata})

    @app.before_request
    def before_request():
        if "language" not in session:
            session["language"] = request.accept_languages.best_match(
                ["en", "de"], default="en"
            )
        g.language = session["language"]

    @app.route("/")
    def index():
        with open(f"static/prose/{g.language}/intro.md", "r") as file:
            intro = markdown.markdown(file.read())

        posts = []
        for i, app_md in enumerate(dash_apps[g.language]):

            metadata = app_md["metadata"]

            post = {
                "title": metadata.get(f"title", "Default title"),
                "route": metadata.get("route", "/default/"),
                "thumbnail_img": read_png_file(metadata.get("thumbnail", None)),
                "synopsis": metadata.get(f"synopsis", "Default synopsis"),
                "rotation": (2 * (i % 2) - 1) * 3,
                "offset": [2, 5, 1, 4, 3][i % 5],
            }
            posts.append(post)

        return render_template(
            "index.html",
            intro=intro,
            posts=posts,
            nav_entries=nav_entries,
            current_language=g.language,
            language_names={"en": "English", "de": "Deutsch"},
        )

    @app.route("/contact")
    def contact():
        return render_template(
            f"contact_{g.language}.html",
            nav_entries=nav_entries,
            current_language=g.language,
            language_names={"en": "English", "de": "Deutsch"},
        )

    @app.route("/set_language/<lang>")
    def set_language(lang):
        session["language"] = lang
        return redirect(request.referrer or url_for("index"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
