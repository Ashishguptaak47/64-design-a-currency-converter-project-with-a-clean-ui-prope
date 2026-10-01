import sys
import requests

class CurrencyConverter:
    API_URL = "https://api.exchangerate-api.com/v4/latest/"

    def __init__(self):
        pass

    def fetch_rates(self, base_currency: str) -> dict:
        try:
            response = requests.get(f"{self.API_URL}{base_currency.upper()}", timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("rates", {})
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch exchange rates: {e}")

    def convert(self, amount: float, from_curr: str, to_curr: str) -> float:
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        
        rates = self.fetch_rates(from_curr)
        to_curr = to_curr.upper()
        
        if to_curr not in rates:
            raise ValueError(f"Target currency '{to_curr}' is not supported.")
        
        return amount * rates[to_curr]

def main():
    print("================================")
    print("   WELCOME TO CURRENCY CONVERTER ")
    print("================================")
    
    converter = CurrencyConverter()
    
    while True:
        try:
            from_curr = input("\nEnter source currency (e.g., USD, EUR) or 'q' to quit: ").strip()
            if from_curr.lower() == 'q':
                print("Goodbye!")
                break
                
            to_curr = input("Enter target currency (e.g., GBP, JPY): ").strip()
            
            amount_input = input("Enter amount to convert: ").strip()
            amount = float(amount_input)
            
            print("Fetching latest rates...")
            result = converter.convert(amount, from_curr, to_curr)
            
            print(f"\n{amount:,.2f} {from_curr.upper()} = {result:,.2f} {to_curr.upper()}\n")
            
        except ValueError as ve:
            print(f"[Error] {ve}")
        except ConnectionError as ce:
            print(f"[Network Error] {ce}")
        except Exception as e:
            print(f"[Unexpected Error] {e}")

if __name__ == "__main":
    main()
