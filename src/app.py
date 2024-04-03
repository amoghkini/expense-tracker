from main.main import AppFactory
from config.settings import DevelopmentConfig

app = AppFactory(DevelopmentConfig).get_app(__name__)
app.run()
