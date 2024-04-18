from datetime import timedelta
from flask import Flask, session, g


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
            db.create_all()   # To create database
        
    def register_before_request(self):
        @self.app.before_request
        def before_request():
            session.permanent = True  # set session to use PERMANENT_SESSION_LIFETIME
            session.modified = True   # reset the session timer on every request
            self.app.permanent_session_lifetime = timedelta(minutes=5)
            
            g.user = None
            if 'user' in session:
                g.user = session['user']
            
    def register_after_request(self):
        @self.app.after_request
        def after_request(response):
            # Your after_request logic goes here
            return response
        
    def register_teardown_appcontext(self):
        @self.app.teardown_appcontext
        def teardown_appcontext(exception):
            pass
        