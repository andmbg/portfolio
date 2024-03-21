from flask import Flask, render_template
import dashapps.interface_dashapp1
import dashapps.interface_dashapp2
import dashapps.interface_pks

flask_app = Flask(__name__)


@flask_app.route("/")
def index():
    return render_template(
        "index.html",
        content="Hello World",
    )  # This is your main page with header and footer

dashapps.interface_dashapp1.init(flask_app)
dashapps.interface_dashapp2.init(flask_app)
dashapps.interface_pks.init(flask_app)


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8080, debug=False)
