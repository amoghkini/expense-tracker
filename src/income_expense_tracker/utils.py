from income_expense_tracker.constants import (
    FoodAndDrinks, 
    Transport,
    Shopping,
    Groceries,
    Entertainment,
    Travel,
    Medical,
    Personal,
    Fitness,
    Services,
    Bill,
    Subscription,
    Emi,
    CreditBill,
    Investment,
    Support,
    Insurance,
    Tax,
    TopUp,
    Misc
)
from utils.utils import Utils as CommmonUtils

class Utils:
    
    @staticmethod
    def get_expense_categories() -> dict:
        categories_dict: dict = {}
        
        for enum_class in (FoodAndDrinks, Transport, Shopping, Groceries, Entertainment, Travel, Medical, Personal, Fitness, Services, Bill, Subscription, Emi, CreditBill, Investment, Support, Insurance, Tax, TopUp, Misc):
            optgroup = CommmonUtils.title_case_to_space_separated(enum_class.__name__)
            options = enum_class.allowed_values()
            categories_dict[optgroup] = options
        return categories_dict