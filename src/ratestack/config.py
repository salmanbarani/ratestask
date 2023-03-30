import os


def get_postgres_uri():
    return "postgresql://postgres:ratestask@localhost:5432/postgres"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"
