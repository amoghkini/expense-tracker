from enum import StrEnum, auto


class BaseEnum(StrEnum):
    
    @classmethod
    def allowed_values(cls):
        return [member.value for member in cls]
    
    
class TransactionType(BaseEnum):
    CREDIT = auto()
    DEBIT = auto()
    
    
class ModeOfPayment(BaseEnum):
    CASH = auto()
    UPI = auto()
    
    
class ReasonOfExpense(BaseEnum):
    INVESTMENT = auto()
    NEED = auto()
    WANT = auto()
    OTHER = auto()
    

# Categoris enum values 
class FoodAndDrinks(BaseEnum):
    EATING_OUT = "Eating Out"
    TAKE_AWAY = "Take Away"
    TEA_AND_COFFEE = "Tea & Coffee"
    FAST_FOOD = "Fast Food"
    SNACKS = "Snacks"
    SWIGGY = "Swiggy"
    ZOMATO = "Zomato"
    DOMINOES = "Dominoes"
    DESSERT = "Dessert"
    LIQUOR = "Liquor"
    BEVERAGES = "Beverages"
    DATE = "Date"
    PIZZA = "Pizza"
    BURGER = "Burger"
    TIFFIN = "Tiffin"
    FOOD_AND_DRINKS_OTHER = 'Food & Drinks Other'
    

class Transport(BaseEnum):
    UBER = "Uber"
    OLD = "Ola"
    RAPIDO = "Rapido"
    AUTO = "Auto"
    CAB = "Cab"
    TRAIN_PASS = "Train Pass"
    TRAIN_TICKET = "Train Ticket"
    METRO = "Metro"
    BUS = "Bus"
    Bike = "Bike"
    PETROL = "Petrol"
    DISEAL = "Diseal"
    FLIGHTs = "Flights"
    PARKING = "Parking"
    FASTAG = "FASTag"
    TOLLS = "Tolls"
    LOUNGE = "Lounge"
    FINE = "Fine"
    TRANSPORT_OTHER = "Transport Other"
    
    
    