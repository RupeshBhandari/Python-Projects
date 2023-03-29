import requests 
import pandas as pd
from datetime import date


class Currency():
    def __init__(self, date=date.today(), currency=''):
        self.date = date
        self.currency = currency
        
        # requests from API
        self.data = requests.get(f'https://www.nrb.org.np/api/forex/v1/rate/?from={self.date}&to={self.date}')
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
                else:
                    for a in self.data['data'][i]['rates']:
                        print(f"Currency Code: {a['currency']['iso3']}")
                        print(f"Currency Name: {a['currency']['name']}")
                        print(f"Currency Unit: {a['currency']['unit']}")
                        print(f"Currency Buy : {a['buy']}")
                        print(f"Currency Sell: {a['sell']}")
                    
        return self.data
    
    def convert_to_npr(self, amount):
        self.amount = amount
        for i in self.data['data']:
            
            for j in self.data['data'][i]['rates']:
                
                # Filter the currency from argument and convert it to NPR
                if j['currency']['iso3'] == self.currency:
                    print(f"'Currency Name:' {j['currency']['name']}")
                    print(f"'Currency Buy:' {float(j['buy']) * amount/float(j['currency']['unit'])}")
                    print(f"'Currency Sell:' {float(j['sell']) * amount/float(j['currency']['unit'])}")

    
    def table(self):
        currency_code = list()
        currency_name = list()
        currency_buy = list()
        currency_sell = list()
        
        if self.currency != '':
            for i in self.data['data']['payload']['rates']:
                if i['currency']['iso3'] == self.currency:
                    currency_code.append(i['currency']['iso3'])
                    currency_name.append(i['currency']['name'])
                    currency_buy.append(i['buy'])
                    currency_sell.append(i['sell'])
                    dic_for_table = zip(currency_code, currency_name, currency_buy, currency_sell)
                else:
                    continue
        else:
            for i in self.data['data']['payload']['rates']:
                currency_code.append(i['currency']['iso3'])
                currency_name.append(i['currency']['name'])
                currency_buy.append(i['buy'])
                currency_sell.append(i['sell'])
                dic_for_table = zip(currency_code, currency_name, currency_buy, currency_sell)
            
    
                # continue
                
            
            # dic_for_table = zip(currency_code, currency_name, currency_buy, currency_sell)
        
        data_frame = pd.DataFrame(dic_for_table, columns=['Currency Code','Currency Name', 'Currency Buy', 'Currency Sell'])
        data_frame.set_index('Currency Code', inplace=True)
        return data_frame.to_markdown()


# start_date = input('Enter Start Date: ')
# last_date = input('Enter Last Date: ')
# currency = input('Enter Currency Code: ')

# print(Currency(date=date, currency=currency).table())

print(Currency(date='2023-03-29', currency='').table())

# Currency().convert_to_npr(1000)

