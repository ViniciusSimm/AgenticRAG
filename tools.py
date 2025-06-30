from smolagents import Tool
import requests
import os

class CryptoCurrencyInfoTool(Tool):
    name = "crypto_currency_info"
    description = "Fetches real-time cryptocurrency information."
    inputs = {
        "id": {
            "type": "string",
            "description": "The ID of the cryptocurrency to fetch information for. Ex '90' for Bitcoin, '80' for Ethereum, etc."
        }
    }
    output_type = "string"

    def forward(self, id: str):
        url = "https://api.coinlore.net/api/ticker/?id={}".format(id)
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return f"{data[0]['name']} ({data[0]['symbol']}): ${data[0]['price_usd']}, Change in 24h: ${data[0]['percent_change_24h']}, Volume: ${data[0]['volume24']}"
        except requests.RequestException as e:
            return f"Error fetching cryptocurrency data: {str(e)}"


class CurrencyExchangeRateTool(Tool):
    name = "currency_exchange_rate"
    description = "Fetches the exchange rate between two currencies at the current time."
    inputs = {
        "from_currency": {
            "type": "string",
            "description": "The currency to convert from, e.g., 'USD'."
        },
        "to_currency": {
            "type": "string",
            "description": "The currency to convert to, e.g., 'EUR'."
        }
    }
    output_type = "string"

    def forward(self, from_currency: str, to_currency: str):
        url = f"https://economia.awesomeapi.com.br/last/{from_currency}-{to_currency}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            file = data[f"{from_currency}{to_currency}"]
            return f"Exchange rate {file['name']}, High: {file['high']}, Low: {file['low']}, Bid: {file['bid']}, Ask: {file['ask']}"
        except requests.RequestException as e:
            return f"Error fetching exchange rate data: {str(e)}"
    
class SeachStockSymbolTool(Tool):
    name = "search_stock_symbol"
    description = "Searches for a stock symbol based on a company name."
    inputs = {
        "company_name": {
            "type": "string",
            "description": "The name of the company to search for its stock symbol."
        }
    }
    output_type = "string"

    def forward(self, company_name: str):
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={os.getenv('ALPHAVANTEGE_API_KEY')}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'bestMatches' in data and len(data['bestMatches']) > 0:
                match = data['bestMatches']
                result = '; '.join([f"Company: {i['2. name']} symbol: {i['1. symbol']} type: {i['3. type']} region: {i['4. region']}" for i in match[0:3]])
                return result
            else:
                return "No stock symbol found for the given company name."
        except requests.RequestException as e:
            return f"Error fetching stock symbol data: {str(e)}"

class StockPriceTool(Tool):
    name = "stock_price"
    description = "Fetches the current stock price for a given stock symbol."
    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the price for, e.g., 'AAPL' for Apple Inc."
        }
    }
    output_type = "string"

    def forward(self, symbol: str):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={os.getenv('ALPHAVANTEGE_API_KEY')}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'Global Quote' in data and '05. price' in data['Global Quote']:
                return f"The current price of {symbol} is ${data['Global Quote']['05. price']}."
            else:
                return f"No data found for the stock symbol {symbol}."
        except requests.RequestException as e:
            return f"Error fetching stock price data: {str(e)}"

class MarketStatusTool(Tool):
    name = "market_status"
    description = "Provides the current status of the stock market (open or closed)."
    inputs = {
        "country": {
            "type": "string",
            "description": "The country for which to check the market status, e.g., 'United States' or 'Brazil'.",
        }
    }
    output_type = "string"

    def forward(self, country: str):
        url = f"https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={os.getenv('ALPHAVANTEGE_API_KEY')}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'markets' in data:
                market = next((m for m in data['markets'] if m['region'].lower() == country.lower()), None)
                if market:
                    data['status'] = market['current_status']
                else:
                    data['status'] = "unknown"
                return f"The stock market in {country} is currently {data['status']}."
            else:
                return "Market status information is not available."
        except requests.RequestException as e:
            return f"Error fetching market status data: {str(e)}"

    