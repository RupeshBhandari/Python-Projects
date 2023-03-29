import requests 
from datetime import date

class Currency():
    def __init__(self, date=date.today(), currency='USD'):
        self.date = date
        self.currency = currency
        
        self.data = requests.get('https://www.nrb.org.np/api/forex/v1/rate/?from=2021-03-29&to=2021-03-29')
        self.data = self.data.json()

    def get_data(self):
        for i in self.data['data']:

            for j in self.data['data'][i]['rates']:
                
                if j['currency']['iso3'] == self.currency:
                    print(f"Currency Code: {j['currency']['iso3']}")
                    print(f"Currency Name: {j['currency']['name']}")
                    print(f"Currency Unit: {j['currency']['unit']}")
                    print(f"Currency Buy : {j['buy']}")
                    print(f"Currency Sell: {j['sell']}")
        return self.data
    
    def convert_to_npr(self, amount):
        self.amount = amount
        for i in self.data['data']:
            
            for j in self.data['data'][i]['rates']:
                
                if j['currency']['iso3'] == self.currency:
                    
                    print(f"'Currency Name:' {j['currency']['name']}")
                    print(f"'Currency Buy:' {float(j['buy']) * amount/float(j['currency']['unit'])}")
                    print(f"'Currency Sell:' {float(j['sell']) * amount/float(j['currency']['unit'])}")

Currency('2023-03-29', 'INR').get_data()

Currency('2023-03-28','INR').convert_to_npr(1000)

