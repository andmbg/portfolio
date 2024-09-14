import importlib
from flask import Flask, render_template, request, session, url_for, redirect, g
import markdown
import base64


LANGUAGE_NAMES = {"en": "English", "de": "Deutsch"}


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

    language_urls = {"en": f"/set_language/en", "de": f"/set_language/de"}

    app_dirs = [
        "bundestag",
        "pks",
        "wikimap",
        "elternsein",
    ]
    dash_apps = {"en": [], "de": []}


    for lang in ["en", "de"]:
        for app_dir in app_dirs:
            module = importlib.import_module(f"dashapps.{lang}.{app_dir}.{app_dir}")
            metadata = importlib.import_module(f"dashapps.{lang}.{app_dir}").metadata[lang]
            dash_app = module.init_dashboard(app, f'/{lang}/{app_dir}/')

            # modify apps to contain the dashapp template:
            with app.test_request_context("/?name=test"):
                dash_app.index_string = render_template(
                    "dashapp.html",
                    title=metadata.get("title", "default title"),
                    nav_entries=nav_entries,
                    language_names=LANGUAGE_NAMES,
                    current_language=lang,
                    language_urls=language_urls,
                )

            dash_apps[lang].append({"app": dash_app, "metadata": metadata})

    @app.route("/<lang>/<app_name>/")
    def render_dash_app(lang, app_name):
        if lang not in ["en", "de"] or app_name not in app_dirs:
            return redirect(url_for("index"))

        dash_app = next(
            (
                app
                for app in dash_apps[lang]
                if app["metadata"]["route"].endswith(f"/{app_name}/")
            ),
            None,
        )

        if dash_app:
            return dash_app["app"].index()
        else:
            return redirect(url_for("index"))

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
            language_names=LANGUAGE_NAMES,
            language_urls=language_urls,
        )

    @app.route("/contact")
    def contact():
        return render_template(
            f"contact_{g.language}.html",
            nav_entries=nav_entries,
            current_language=g.language,
            language_names=LANGUAGE_NAMES,
            language_urls=language_urls,
        )

    @app.route("/set_language/<lang>")
    def set_language(lang):
        session["language"] = lang
        referrer = request.referrer
        if referrer:
            for app_dir in app_dirs:
                if app_dir in referrer:
                    return redirect(
                        url_for("render_dash_app", lang=lang, app_name=app_dir)
                    )
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
