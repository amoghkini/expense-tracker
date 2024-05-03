from typing import Any, Optional
class Response:
    
    def __init__(
        self,
        success: bool = True,
        data: Any = None,    
        message: str = '',
        errors: dict = {},
        next_page: str = ''
    ) -> None:
        self.success = success
        self.data = data
        self.message = message
        self.errors = errors
        self.next_page = next_page
        
    def to_dict(self) -> dict:
        return self.__dict__