import base64
import markdown

from flask import Flask, g, session, render_template, request, redirect, url_for

from dashapps.apps_metadata import APPS_METADATA
from config import LANGUAGES


def read_png_file(file_path):
    if file_path is None:
        return None
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    @app.before_request
    def before_request():
        if "language" not in session:
            session["language"] = request.accept_languages.best_match(
                ["en", "de"], default="en"
            )
        g.language = session["language"]

    nav_entries = {
        "Start": "/",
        "Kontakt": "/contact",
    }

    language_urls={"de": "/set_language/de", "en": "/set_language/en"}

    #
    # Index:
    # List of dash apps and an intro text.
    #
    @app.route("/")
    def index():

        with open(f"static/prose/{g.language}/intro.md", "r") as file:
            intro = markdown.markdown(file.read())

        posts = []
        for i, app_name in enumerate(APPS_METADATA):
            metadata = APPS_METADATA[app_name]
            posts.append({
                "title": metadata["title"][g.language],
                "route": app_name,
                "thumbnail_img": read_png_file(metadata["thumbnail"]),
                "synopsis": metadata["synopsis"][g.language],
                "rotation": (2 * (i % 2) - 1) * 3,
                "offset": [2, 5, 1, 4, 3][i % 5],
            })
        
        return render_template(
            "index.html",
            intro=intro,
            posts=posts,
            nav_entries=nav_entries,
            language_names=LANGUAGES,
            current_language=g.language,
            language_urls=language_urls,
        )

    #
    # Contact
    #
    @app.route("/contact")
    def contact():
        return render_template(
            f"contact_{g.language}.html",
            nav_entries=nav_entries,
            language_names=LANGUAGES,
            current_language=g.language,
            language_urls=language_urls,
        )

    #
    # Set Language
    #
    @app.route("/set_language/<lang>")
    def set_language(lang):
        session["language"] = lang
        referrer = request.referrer
        if referrer:
            return redirect(referrer)


    return app

flask_app = create_app()

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000, debug=False)
