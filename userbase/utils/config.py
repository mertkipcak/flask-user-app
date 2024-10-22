import json
import os

CONFIG_PATH = os.getenv('CONFIG_PATH', './config/app_config.json')

class Config:
    _instance = None

    def __new__(cls, config_file_path=CONFIG_PATH):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config(config_file_path)
        return cls._instance

    def _load_config(self, config_file_path):
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Config file not found: {config_file_path}")
        with open(config_file_path) as config_file:
            self.config = json.load(config_file)

    def get(self, key, default=None):
        return self.config.get(key, default)

# Create a singleton instance of Config
CONFIG = Config()
