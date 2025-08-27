import os
from dotenv import load_dotenv


def load_env_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    possible_paths = [
        os.path.join(current_dir, "..", ".env"),
        os.path.join(current_dir, "..", ".env.template"),
    ]

    found = False
    for path in possible_paths:
        if os.path.exists(path):
            load_dotenv(path, override=False)
            found = True

    if not found:
        print("⚠️ .env file not found in expected locations")
