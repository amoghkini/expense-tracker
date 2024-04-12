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
    TRANSFER = auto()
    
    
class ReasonOfExpense(BaseEnum):
    INVESTMENT = auto()
    NEED = auto()
    WANT = auto()
    OTHER = auto()
    

# Income categories enum values
class IncomeCategories(BaseEnum):
    SALARY = 'Salary'
    MARKET = "Market"
    MUTUAL_FUNDS = "Mutual Funds"
    INTEREST = "Interest"
    

# Expense categoris enum values 
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
    FOOD_AND_DRINKS_OTHER = "Food & Drinks Other"
    

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
    
    
class Shopping(BaseEnum):
    CLOTHS = "Cloths"
    SHOES = "Shoes"
    Electronics = "Electronics"
    VIDEO_GAMES = "Video Games"
    BOOKS = "Books"
    PLANTS = "Plants"
    JEWELLERY = "Jewellery"
    FURNITURE = "Furniture"
    VEHICLE = "Vehicle"
    COSMETICS = "Cosmetics"
    Toys = "Toys"
    STATIONARY = "Stationary"
    GLASSES = "Glasses"
    SHOPPING_OTHER = "Shopping Other"
    

class Groceries(BaseEnum):
    VEGETABLES = "Vegetables"
    FRUITS = "Fruits"
    MEAT = "Meat"
    BAKERY = "Bakery"
    DAIRY = "Dairy"
    GROCERIES_OTHER = "Groceries Other"
    
class Entertainment(BaseEnum):
    MOVIES = "Movies"
    SHOWS = "Shows"
    BOWLING = "Bowling"
    ENTERTAINMENT_OTHER = "Entertainment Other"
    
    
class Travel(BaseEnum):
    ACTIVITIES = "Activities"
    CAMPING = "Camping"
    HOTEL = "Hotel"
    HOSTEL = "Hostel"
    AIRBNB = "Airbnb"
    
    
class Medical(BaseEnum):
    MEDICINES = "Medicines"
    HOSPITAL = "Hospital"
    CLINIC = "Clinic"
    DENTIST = "Dentist"
    LAB_TEST = "Lab Test"
    HYGINE = "Hygine"
    MEDICAL_OTHER = "Medical Other"