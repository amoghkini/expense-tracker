from enum import StrEnum, auto


class UserStatus(StrEnum):
    CREATED = auto()
    ACTIVATED = auto()
    DEACTIVATED = auto()
    DELETED = auto()
    TERMINATED = auto()
    

class RegularExpressions(StrEnum):
    EMAIL_REGEX: str = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PASSWORD_REGEX: str = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"