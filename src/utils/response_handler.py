from typing import Any
class Response:
    
    def __init__(
        self,
        success: bool = True,
        data: Any = None,    
        message: str = '',
        errors: dict = {}
    ) -> None:
        self.success = success
        self.data = data
        self.message = message
        self.errors = errors
        
    def to_dict(self) -> dict:
        return self.__dict__