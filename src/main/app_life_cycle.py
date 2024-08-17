from datetime import timedelta
from flask import Flask, session, g


from main.extensions import db

class AppLifeCycle:
    
    def __init__(
        self,
        app: Flask
    ) -> None:
        self.app = app
                
    def register_before_request(self):
        @self.app.before_request
        def before_request():
            session.permanent = True  # set session to use PERMANENT_SESSION_LIFETIME
            session.modified = True   # reset the session timer on every request
            self.app.permanent_session_lifetime = timedelta(minutes=60)
            
            g.user = None
            if 'email' in session:
                g.email =  session.get('email')
            
    def register_after_request(self):
        @self.app.after_request
        def after_request(response):
            # Your after_request logic goes here
            return response
        
    def register_teardown_appcontext(self):
        @self.app.teardown_appcontext
        def teardown_appcontext(exception):
            pass
        