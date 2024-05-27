from userpreferences.models import Currencies
import json



with open('/Users/amanthakur/development/app/money_project/currencies.json', 'r') as file:
    data = json.load(file)
    print(data)