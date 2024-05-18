from enum import StrEnum, auto


class BaseEnum(StrEnum):
    
    @classmethod
    def allowed_values(cls):
        return [member.value for member in cls]
    
class UserStatus(BaseEnum):
    CREATED = auto()
    ACTIVATED = auto()
    LOCKED = auto()
    DEACTIVATED = auto()
    DELETED = auto()
    TERMINATED = auto()
    

class RegularExpressions(BaseEnum):
    EMAIL_REGEX: str = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PASSWORD_REGEX: str = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
    
    
class IndianStatesAndUTs(BaseEnum):
    ANDHRA_PRADESH = "Andhra Pradesh"
    ARUNACHAL_PRADESH = "Arunachal Pradesh"
    ASSAM = "Assam"
    BIHAR = "Bihar"
    CHHATTISGARH = "Chhattisgarh"
    GOA = "Goa"
    GUJARAT = "Gujarat"
    HARYANA = "Haryana"
    HIMACHAL_PRADESH = "Himachal Pradesh"
    JAMMU_AND_KASHMIR = "Jammu and Kashmir"
    JHARKHAND = "Jharkhand"
    KARNATAKA = "Karnataka"
    KERALA = "Kerala"
    MADHYA_PRADESH = "Madhya Pradesh"
    MAHARASHTRA = "Maharashtra"
    MANIPUR = "Manipur"
    MEGHALAYA = "Meghalaya"
    MIZORAM = "Mizoram"
    NAGALAND = "Nagaland"
    ODISHA = "Odisha"
    PUNJAB = "Punjab"
    RAJASTHAN = "Rajasthan"
    SIKKIM = "Sikkim"
    TAMIL_NADU = "Tamil Nadu"
    TRIPURA = "Tripura"
    UTTARAKHAND = "Uttarakhand"
    UTTAR_PRADESH = "Uttar Pradesh"
    WEST_BENGAL = "West Bengal"
    ANDAMAN_AND_NICOBAR_ISLANDS = "Andaman and Nicobar Islands"
    CHANDIGARH = "Chandigarh"
    DADRA_AND_NAGAR_HAVELI = "Dadra and Nagar Haveli"
    DAMAN_AND_DIU = "Daman and Diu"
    DELHI = "Delhi"
    LAKSHADWEEP = "Lakshadweep"
    PUDUCHERRY = "Pondicherry"