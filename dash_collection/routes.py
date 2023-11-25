"""Routes for parent Flask app."""
from flask import current_app as app
from flask import render_template, request


@app.route("/")
def home():
    """Home page of Flask Application."""
    return render_template(
        "index.jinja2",
        title="List of routes",
        template="home-template",
        # description="More routes will appear here when extending the app.",
        # body="This is a homepage served with Flask.",
        base_url=request.base_url,
    )
