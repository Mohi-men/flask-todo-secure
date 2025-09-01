import os
from dotenv import load_dotenv
from app import create_app

# load all environment variables from .env before app is created
load_dotenv()

app = create_app(os.environ.get("APP_CONFIG", "config.DevConfig"))

if __name__ == "__main__":
    app.run()