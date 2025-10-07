"""Entry point for running the Flask development server."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="20.48.204.0", port=5000, debug=False)
