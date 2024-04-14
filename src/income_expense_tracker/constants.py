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
    SALARY = "Salary"
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
    Electronics_SHOPPING = "Electronics Shopping" # We have same name in other categories. Hence using different naming convension.
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
    

class Personal(BaseEnum):
    SELF_CARE = "Self Care"
    GROOMING = "Grooming"
    HOBBIES = "Hobbies"
    VICES = "Vices"
    THERAPY = "Therapy"
    PERSONAL_OTHER = "Personal Other"
    
    
class Fitness(BaseEnum):
    GYM = "Gym"
    BADMINTON = "Badminton"
    FOOTBALL = "Football"
    CRICKET = "Cricket"
    CLASSES = "Classses"
    EQUIPMENT = "Equipment"
    NUTRITION = "Nutrition"
    FITNESS_OTHER = "Fitness Other"
    
    
class Services(BaseEnum):
    LAUNDRY = "Laundry"
    COURIER = "Courier"
    PLUMBER = "Plumber"
    MECHANIC = "Mechanic"
    PHOTOGRAPHER = "Phptographer"
    DRIVER = "Driver"
    VEHICAL_WASH = "Vehical Wash"
    ELECTRICIAN = "Electrician"
    PAINTING = "Painting"
    XEROX = "Xerox"
    LEGAL = "Legal"
    ADVISOR = "Advisor"
    REPAIR = "Repair"
    LOGISTICS = "Logistics"
    SERVICES_OTHER = "Services Other"
    
    
class Bill(BaseEnum):
    PHONE = "Phone"
    RENT = "Rent"
    WATER = "Water"
    ELECTRICITY = "Electricity"
    GAS = "Gas"
    INTERNET = "Internet"
    HOUSE_HELP = "House Help"
    EDUCATION_BILL = "Education Bill"
    DTH = "DTH"
    COOK = "Cook"
    MAINTENANCE = "Maintenance"
    BILL_OTHER = "Bill Other"
    
    
class Subscription(BaseEnum):
    NETFLIX = "Netflix"
    PRIME = "Prime"
    YOUTUBE = "Youtube"
    HOTSTAR = "Hotstar"
    SPOTIFY = "Spotify"
    GOOGLE = "Google"
    LERANING = "Learning"
    APPLE = "Apple"
    NEWS = "News"
    SUBSCRIPTION_OTHER = "Subscription Other"
    
    
class Emi(BaseEnum):
    ELECTRONICS_EMI = "Electronics EMI"
    HOUSE = "House"
    VEHICAL_EMI = "Vehical EMI"
    EDUCATION_EMI = "Education EMI"
    EMI_OTHER = "EMI Other"
    
    
class CreditBill(BaseEnum):
    CREDIT_CARD = "Credit Card"
    SIMPL = "Simpl"
    SLICE = "Slice"
    LAZYPAY = "Lazy Pay"
    AMAZOON_PAY = "Amazon Pay"
    CREDIT_BILL_OTHER = "Credit Bill Other"
    
    
class Investment(BaseEnum):
    MUTUAL_FUNDS = "Mutual Funds"
    STOCKS = "Stocks"
    PPF = "PPF"
    NPS = "NPS"
    FIXED_DEPOSIT = "Fixed Deposit"
    RECURRING_DEPOSIT = "Recurring Deposit"
    ASSETS = "Assets"
    CRYPTO = "Crypto"
    GOLD = "Gold"
    INVESTMENT_OTHER = "Investment Other"
    
    
class Support(BaseEnum):
    PARENTS = "Parents"
    SPOUCE = "Spouce"
    MOM = "Mom"
    DAD = "Dad"
    POCKET_MONEY = "Pocket Money"
    FRIEND = "Friend"
    SUPPORT_OTHER = "Support Other"
    
    
class Insurance(BaseEnum):
    HEALTH = "Health"
    VEHICAL_Insurance = "Vehical Insurace"
    LIFE = "Life"
    ELECTRONICS_INSURANCE = "Electronics Insurance"
    INSURANCE_OTHER = "Insurance Other"
    

class Tax(BaseEnum):
    INCOME_TAX = "Income Tax"
    INCOME_TAX_DEDUCTION_AT_SOURCE = "TDS"
    GST = "GST"
    PROPERTY_TAX = "Property Tax"
    
    
class TopUp(BaseEnum):
    UPI_LITE = "UTI Lite"
    PAYTIM = "Paytm"
    AMAZON = "Amazon"
    PHONEPAY = "Phone Pay"
    UTS = "UTS"
    OTHER_WALLETS = "Other"
    TOP_UP_OTHER = "Top Up Other"
    
    
class Misc(BaseEnum):
    TIP = "Tip"
    VERIFICATION = "Verification"
    FOREX = "Forex"
    MISC_OTHER = "Misc Other"
    DONATION = "Donation"