import os
import yaml
from typing import Any
from dotenv import load_dotenv


dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class BaseConfig(object):
    
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    CSRF_ENABLED = True
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "SomeRandomSecretKeyHere"
    VERBOSE = True
    
    URL_MODULES = [
        'auth.urls.routes',
        'core.urls.routes',
        'dashboard.urls.routes',
        'income_expense_tracker.urls.routes'
    ]
    
    BLUEPRINTS = [
        'auth.auth',
        'core.core_blueprint',
        'dashboard.dashboard',
        'income_expense_tracker.income_expense_tracker',
    ]
    
    EXTENSIONS = [
        'main.extensions.db',
    ]
    
    CONTEXT_PROCESSORS = [
        'core.context_processors.inject_layout_type',
    ]
    

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///temp.db"
    

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///temp.db"
    

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///temp.db"

# Dictionary to map environment names to configuration classes
config_mapping = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}


# Function to get the configuration class based on the environment
def get_config():
    flask_env = os.getenv('FLASK_ENV', 'development')  # Default to development if FLASK_ENV is not set
    print(flask_env)
    return config_mapping.get(flask_env.lower(), DevelopmentConfig)()


def get_server_helper_config_from_yaml() -> dict[str, Any]:
    config_file_path: str  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config','config.yaml'))
    with open(config_file_path, 'r') as stream:
        try:
            config_data: dict[str, Any] = yaml.safe_load(stream)
            return config_data
        except yaml.YAMLError as e:
            print(e)
            