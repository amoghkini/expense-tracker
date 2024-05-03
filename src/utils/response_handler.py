from typing import Any, Optional
class Response:
    
    def __init__(
        self,
        success: bool = True,
        data: Optional[Any] = None,    
        message: Optional[str] = None,
        errors: Optional[dict] = None,
        next_page: Optional[str]= None
    ) -> None:
        self.success = success
        self.data = data
        self.message = message
        self.errors = errors
        self.next_page = next_page
        
    def to_dict(self) -> dict:
        return self.__dict__