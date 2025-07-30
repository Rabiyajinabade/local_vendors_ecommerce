import requests

def get_conversion_rate(from_currency, to_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        print("API response:", data)  # 👈 Add this line for debugging

        # Check if 'rates' is in response
        if 'rates' not in data:
            print("Key 'rates' not in response")
            return None
        
        rate = data['rates'].get(to_currency)
        return rate
    except Exception as e:
        print("Error fetching currency rate:", e)
        return None
