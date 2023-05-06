import datetime as dt
import requests
import pandas as pd


class Currency:
    '''This class is used to get the data from the API'''

    def __init__(self, date_from=None, date_to=None):
        '''This function is used to initialize the class'''
        self.date_from = date_from or dt.date.today()
        self.date_to = date_to or dt.date.today()
        self.data = []
        self.total_pages = None
        self.total_records = None

    def _get_page(self, page_num):
        '''This method returns the data for a single page'''
        response = requests.get(
            f"https://www.nrb.org.np/api/forex/v1/rates/?page={page_num}&from={self.date_from}&to={self.date_to}&per_page=100",
            timeout=60)
        response.raise_for_status()
        data = response.json()
        self.total_pages = data['pagination']['pages']
        self.total_records = data['pagination']['total']
        return data['data']['payload']

    def _parse_data(self, payload):
        '''This method parses the payload and returns a list of dictionaries'''
        data = []
        for item in payload:
            date = dt.datetime.strptime(item['date'], '%Y-%m-%d').date()
            for rate in item['rates']:
                data.append({
                    'date': date,
                    'currency_code': rate['currency']['iso3'],
                    'currency_name': rate['currency']['name'],
                    'buy': rate['buy'],
                    'sell': rate['sell']
                })
        return data

    def get_data(self):
        '''This method returns the data from the API'''
        
        self._get_page(1)

        for i in range(1, self.total_pages + 1):
            payload = self._get_page(i)
            data = self._parse_data(payload)
            self.data.extend(data)
        
        df = pd.DataFrame(self.data)
        
        return df.to_markdown()


if __name__ == "__main__":
    Curr = Currency(date_from='2023-05-01', date_to='2023-05-04').get_data()
    print(Curr)

