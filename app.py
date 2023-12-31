"""Application entry point."""
from dash_collection import init_app

app = init_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False, load_dotenv=False)
