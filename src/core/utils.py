from typing import Optional
from flask import session


class Utils:
    
    @staticmethod
    def get_current_user_from_session() -> Optional[str]:
        if 'email' in session:
            return session['email']
        else:
             return None