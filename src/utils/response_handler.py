class Response:
    
    def __init__(
        self,
        success: bool = True,
        message: str = '',
        errors: dict = {}
    ) -> None:
        self.success = success
        self.message = message
        self.errors = errors
        
    def to_dict(self) -> dict:
        return self.__dict__