from functools import wraps
from typing import Optional, Callable, Union
from flask import request, redirect, url_for, session

def login_required(view_func: Callable) -> Callable:
    """
    Decorator that checks if the user is logged in.

    Args:
        view_func (Callable): The view function to be decorated.

    Returns:
        Callable: The decorated view function.

    Usage:
        @login_required
        def my_view():
            # Code for the view function
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        """
        Inner function that checks if the user is logged in.

        Returns:
            The original view function if the user is logged in,
            otherwise redirects to the login page.
        """
        if 'email' not in session:
            # User is not logged in, redirect to login page with next_page parameter
            next_page = request.endpoint  # Get the view name of the current page
            return redirect(url_for('auth.login_api', next_page=next_page))
        return view_func(*args, **kwargs)
    return wrapper


def get_external_url(
    api_name: str, 
    args: Optional[dict[str, Union[str, bytes]]] = None
) -> str:
    """
    Generates an external URL for a given API endpoint.

    Args:
        api_name (str): The name of the API endpoint.
        args (Optional[dict[str, str]]): Optional dictionary containing arguments to be passed 
            as query parameters in the URL. Default is None.

    Returns:
        str: The generated external URL.

    Example:
        get_external_url('reset_password', {'token': 'abcd1234'})
        # Returns something like: 'https://example.com/reset_password?token=abcd1234'
    """
    if args and 'token' in args:
        return url_for(api_name, token=list(args.values())[0], _external=True)
    return url_for(api_name, _external=True)