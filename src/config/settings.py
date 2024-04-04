import os


class BaseConfig(object):
    SYSTEM_MESSAGE_CATEGORIES = [
            'success'           # 0 - GREEN
            'info',             # 1 - BLUE
            'warning',          # 2 - YELLOW
            'danger',           # 3 - RED
    ]
    
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    CSRF_ENABLED = True
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "SomeRandomSecretKeyHere"
    VERBOSE = True
    
    URL_MODULES = [
        'core.urls.routes',
        'auth.urls.routes',
        'dashboard.urls.routes',
    ]
    
    BLUEPRINTS = [
        'core.core_blueprint',
        'auth.auth',
        'dashboard.dashboard'
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
    