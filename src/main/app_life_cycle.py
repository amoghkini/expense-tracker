from flask import Flask
from main.extensions import db

class AppLifeCycle:
    
    def __init__(
        self,
        app: Flask
    ) -> None:
        self.app = app
        
    def register_before_first_request(self):
        @self.app.before_first_request
        def before_first_request():
            # create database
            db.create_all()   
        
    def register_before_request(self):
        @self.app.before_request
        def before_request():
            # Your before_request logic goes here
            pass
        
    def register_after_request(self):
        @self.app.after_request
        def after_request(response):
            # Your after_request logic goes here
            return response
        
    def register_teardown_appcontext(self):
        @self.app.teardown_appcontext
        def teardown_appcontext(exception):
            # Your before_first_request logic goes here
            pass
        