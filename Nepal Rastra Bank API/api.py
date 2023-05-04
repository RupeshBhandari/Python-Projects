import requests 
import pandas as pd
from datetime import date


class Currency():
    def __init__(self, date=date.today(), currency=''):
        self.date = date
        self.currency = currency
        
        # requests from API
        self.data = requests.get(f'https://www.nrb.org.np/api/forex/v1/rates/?from={self.date}&to={self.date}')
        
#         rate is for today rate and rates for mutiple date!!!!!

#         https://www.nrb.org.np/api/forex/v1/rates/?page=6&from=2021-03-27&to=2023-05-04&per_page=100

        self.data = self.data.json()

    def get_data(self):
        currency_code = list()
        currency_name = list()
        currency_buy = list()
        currency_sell = list()
        
        if self.currency != '' and self.currency != 'ALL':
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
        
        data_frame = pd.DataFrame(dic_for_table, columns=['Currency Code','Currency Name', 'Currency Buy', 'Currency Sell'])
        data_frame.set_index('Currency Code', inplace=True)
        return data_frame.to_markdown()


    def convert_to_npr(self, amount):
        self.amount = amount
        for i in self.data['data']:
            
            for j in self.data['data'][i]['rates']:
                
                # Filter the currency from argument and convert it to NPR
                if j['currency']['iso3'] == self.currency:
                    print(f"'Currency Name:' {j['currency']['name']}")
                    print(f"'Currency Buy:' {float(j['buy']) * amount/float(j['currency']['unit'])}")
                    print(f"'Currency Sell:' {float(j['sell']) * amount/float(j['currency']['unit'])}")



req = requests.get(f'https://www.nrb.org.np/api/forex/v1/rate/')
req = req.json()
count = 1
curr_dict = {0: 'ALL'}

for i in req['data']['payload']['rates']:
    curr_dict[count] = i['currency']['iso3']
    count = count + 1

#====================================================================================================
                        ######         User Input         ######
#====================================================================================================

start_date = input('Enter Start Date (Eg: 2023-01-01): ')

print(f"Choose the Currency Code:")

for g in range(len(curr_dict)):
    print(f"{g} - {curr_dict[g]}")

currency_code_input = int(input(f'Choose the Currency Code:'))

#====================================================================================================
######      End of User Input         ########
#====================================================================================================

print(Currency(date='2021-03-28', currency=curr_dict[currency_code_input]).get_data())
