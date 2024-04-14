from main.main import AppFactory
from config.settings import DevelopmentConfig

app = AppFactory().get_app(__name__)
app.run()
