from functools import wraps
from flask import request, redirect, url_for, session

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            # User is not logged in, redirect to login page with next_page parameter
            next_page = request.endpoint  # Get the view name of the current page
            return redirect(url_for('auth.login_api', next_page=next_page))
        return view_func(*args, **kwargs)
    return wrapper