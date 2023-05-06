import requests
import secret

class UrlShortener:
    def __init__(self, url):
        self.url = url
    
    
    def shorten(self):
        url_for_api = "https://url-shortener-service.p.rapidapi.com/shorten"

        payload = { "url": f"{self.url}" }
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": secret.api_key,
            "X-RapidAPI-Host": "url-shortener-service.p.rapidapi.com"
        }

        response = requests.post(url_for_api, data=payload, headers=headers)
        response = response.json()['result_url']
        return response


if __name__ == "__main__":
    user_input_url = input("Enter a URL to shorten: ")
    print(UrlShortener(user_input_url).shorten())