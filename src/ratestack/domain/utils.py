import re
from datetime import datetime
from decimal import Decimal


class TypeChecker:
    @staticmethod
    def is_slug_valid(slug_param):
        pattern = r"^[a-z0-9]+(?:_[a-z0-9]+)*$"
        return bool(re.match(pattern, slug_param))

    @staticmethod
    def is_code_valid(code, char_legnth=5):
        return len(str(code)) <= char_legnth

    @staticmethod
    def is_price_valid(price):
        return isinstance(price, Decimal) and price >= Decimal("0.0")

    @staticmethod
    def is_date_valid(date):
        try:
            datetime.strptime(str(date), "%Y-%m-%d")
            return True
        except ValueError:
            return False
