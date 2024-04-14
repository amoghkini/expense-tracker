import os
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
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///temp.db"
    