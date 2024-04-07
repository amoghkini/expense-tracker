import re
import unicodedata
from flask_sqlalchemy.model import camel_to_snake_case


class Utils:
    
    @staticmethod
    def slugify(string):
        string = re.sub(r'[^\w\s-]', '',
                        unicodedata.normalize('NFKD', string.strip()))
        return re.sub(r'[-\s]+', '-', string).lower()

    @staticmethod
    def title_case(string):
        return camel_to_snake_case(string).replace('_', ' ').title()
    
    @staticmethod
    def title_case_to_space_separated(string: str) -> str:
        return "".join([char if char.islower() else f" {char}" for char in string])[1:]

    @staticmethod
    def pluralize(name):
        if name.endswith('y'):
            # right replace 'y' with 'ies'
            return 'ies'.join(name.rsplit('y', 1))
        elif name.endswith('s'):
            return f'{name}es'
        return f'{name}s'
    
    @staticmethod
    def was_decorated_without_parenthesis(args):
        return args and callable(args[0])