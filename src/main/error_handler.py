from flask import Flask, render_template
from http import HTTPStatus

class ErrorHandler():
    
    def __init__(
        self,
        app: Flask
    ) -> None:
        self.app = app
        
    def register_400_error(self):
        # 400 - Bad request
        _template = '400.html'
        @self.app.errorhandler(HTTPStatus.BAD_REQUEST)
        def bad_request(e):
            return render_template(_template), HTTPStatus.BAD_REQUEST
        
    def register_403_error(self):
        _template = '403.html'
        @self.app.errorhandler(HTTPStatus.FORBIDDEN)
        def forbidden(e):
            return render_template(_template), HTTPStatus.FORBIDDEN
        
    def register_404_error(self):
        _template = '404.html'
        @self.app.errorhandler(HTTPStatus.NOT_FOUND)
        def page_not_found(e):
            return render_template(_template), HTTPStatus.NOT_FOUND
        
    def register_405_error(self):
        _template = '405.html'
        @self.app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
        def method_not_allowed(e):
            return render_template(_template), HTTPStatus.METHOD_NOT_ALLOWED
        
    def register_500_error(self):
        _template = '500.html'
        @self.app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
        def internal_server_error(e):
            return render_template(_template), HTTPStatus.INTERNAL_SERVER_ERROR