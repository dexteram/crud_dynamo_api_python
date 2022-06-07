import json
from decimal import Decimal
from unicodedata import decimal

# class for the custom encoder
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):    
            return float(obj)
        return json.JSONEncoder.default(self, obj)