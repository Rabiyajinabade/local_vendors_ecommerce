import requests

def get_conversion_rate(to_currency='USD', base='INR'):
    url = f"https://api.exchangerate.host/latest?base={base}&symbols={to_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        return data['rates'][to_currency]
    except Exception as e:
        print("Error fetching currency rate:", e)
        return None
