import dotenv
import os

def load_settings_from_env(root_path):
    dotenv.load_dotenv(os.path.join(root_path, '.env'))
