'''import modules'''
import datetime as dt
import requests
import pandas as pd

class Currency():
    '''This class is used to get the data from the API'''

    def __init__(self, dates=dt.date.today(), date_from='', date_to='', currency='') -> None:
        '''This function is used to initialize the class'''
        self.date = dates
        self.date_from = date_from
        self.date_to = date_to
        self.currency = currency
        self.data = None
        self.total_pages = None
        self.total_records = None

    def get_data(self) -> pd.DataFrame:
        '''This function returns the data from the API'''
        print('HELLLO')

        self.data = requests.get(
            f"https://www.nrb.org.np/api/forex/v1/rates/?page=1&from={self.date_from}&to={self.date_to}&per_page=100", timeout=60)
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
            self.data = requests.get(
                f"https://www.nrb.org.np/api/forex/v1/rates/?page={i}&from={self.date_from}&to={self.date_to}&per_page=100", timeout=60)
            self.data = self.data.json()

            for j in range(0, len(self.data['data']['payload'])):
                for k in self.data['data']['payload'][j]['rates']:
                    dates['Dates'].append(
                        self.data['data']['payload'][j]['date'])
                    # dates.append(self.data['data']['payload'][j]['date'])
                    currency_code['Currency Code'].append(
                        k['currency']['iso3'])
                    currency_name['Currency Name'].append(
                        k['currency']['name'])
                    currency_buy['Currency Buy'].append(k['buy'])
                    currency_sell['Currency Sell'].append(k['sell'])

        data_frame = pd.DataFrame(
            {**dates, **currency_code, **currency_name, **currency_buy, **currency_sell})
        return data_frame.to_markdown()


if __name__ == "__main__":
    Curr = Currency(date_from='2023-05-03', date_to='2023-05-04').get_data()
    print(Curr)
