from datetime import date
import requests
import pandas as pd

class Currency():
    def __init__(self, dates =date.today(), date_from = '', date_to = '', currency=''):
        
        self.date = dates
        self.date_from = date_from
        self.date_to = date_to
        self.currency = currency


    def get_data(self):
        print('HELLLO')
        self.data = requests.get(f"https://www.nrb.org.np/api/forex/v1/rates/?page=1&from={self.date_from}&to={self.date_to}&per_page=100")
        self.data = self.data.json()
        self.total_pages = self.data['pagination']['pages']
        self.total_records = self.data['pagination']['total']
        print(self.total_pages)
        
        # Data storage
        dates = {'Dates': []}
        currency_code = {'Currency Code': []}
        currency_name = {'Currency Name': []}
        currency_buy = {'Currency Buy': []}
        currency_sell = {'Currency Sell': []}
        
        for i in range(1, self.total_pages+1):
            self.data = requests.get(f"https://www.nrb.org.np/api/forex/v1/rates/?page={i}&from={self.date_from}&to={self.date_to}&per_page=100")
            self.data = self.data.json()
            
            for j in range(0, len(self.data['data']['payload'])):
                for k in self.data['data']['payload'][j]['rates']:
                    dates['Dates'].append(self.data['data']['payload'][j]['date'])
                    # dates.append(self.data['data']['payload'][j]['date'])
                    currency_code['Currency Code'].append(k['currency']['iso3'])
                    currency_name['Currency Name'].append(k['currency']['name'])
                    currency_buy['Currency Buy'].append(k['buy'])
                    currency_sell['Currency Sell'].append(k['sell'])
                    
                    
                    # dates.append(self.data['data']['payload'][j]['date'])
                    # currency_code.append(k['currency']['iso3'])
                    # currency_name.append(k['currency']['name'])
                    # currency_buy.append(k['buy'])
                    # currency_sell.append(k['sell'])

        # dic_for_table = zip(dates, currency_code, currency_name, currency_buy, currency_sell)
        
        # print(dates)
        # all_data = []
        data_frame = pd.DataFrame({**dates, **currency_code, **currency_name, **currency_buy, **currency_sell})
        
        # for a in dic_for_table:
        #     all_data.append(a)
        
        # data_frame = pd.DataFrame(all_data, columns=['Dates','Currency Code','Currency Name', 'Currency Buy', 'Currency Sell'])
        return data_frame.to_markdown()
        
        # # for i in self.data['data']['payload']:
        # #     print(i)
        
        # if self.currency != '' and self.currency != 'ALL':
        #     for i in self.data['data']['payload']['rates']:
                
        #         if i['currency']['iso3'] == self.currency:
        #             currency_code.append(i['currency']['iso3'])
        #             currency_name.append(i['currency']['name'])
        #             currency_buy.append(i['buy'])
        #             currency_sell.append(i['sell'])
        #             dic_for_table = zip(currency_code, currency_name, currency_buy, currency_sell)
        #         else:
        #             continue
        # else:
        #     for i in self.data['data']['payload']['rates']:
        #         currency_code.append(i['currency']['iso3'])
        #         currency_name.append(i['currency']['name'])
        #         currency_buy.append(i['buy'])
        #         currency_sell.append(i['sell'])
        #         dic_for_table = zip(currency_code, currency_name, currency_buy, currency_sell)
        



    # def convert_to_npr(self, amount):
    #     self.amount = amount
    #     for i in self.data['data']:
            
    #         for j in self.data['data'][i]['rates']:
                
    #             # Filter the currency from argument and convert it to NPR
    #             if j['currency']['iso3'] == self.currency:
    #                 print(f"'Currency Name:' {j['currency']['name']}")
    #                 print(f"'Currency Buy:' {float(j['buy']) * amount/float(j['currency']['unit'])}")
    #                 print(f"'Currency Sell:' {float(j['sell']) * amount/float(j['currency']['unit'])}")






if __name__ == "__main__":
    Curr = Currency(date_from = '2023-05-03', date_to = '2023-05-04').get_data()
    print(Curr)
