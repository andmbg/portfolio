from flask import Flask
from . import dashapp2_init


app = Flask(__name__, instance_relative_config=False)
app = dashapp2_init(app, route="/")
app.run(host="0.0.0.0", port=8080, debug=True, load_dotenv=False)
