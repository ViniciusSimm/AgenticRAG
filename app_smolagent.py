import gradio as gr
from smolagents import CodeAgent, LiteLLMModel, GradioUI
from tools import CryptoCurrencyInfoTool, CurrencyExchangeRateTool, SeachStockSymbolTool, StockPriceTool, MarketStatusTool

# Using Local Model
model = LiteLLMModel(
    model_id="ollama_chat/qwen3:4b",
    api_base="http://127.0.0.1:11434",
    num_ctx=4096
)


# Define tools
crypto_currency_info = CryptoCurrencyInfoTool()
currency_exchange_rate = CurrencyExchangeRateTool()
seach_stock_symbol = SeachStockSymbolTool()
stock_price = StockPriceTool()
market_status = MarketStatusTool()

finance_agent = CodeAgent(
    tools=[crypto_currency_info,currency_exchange_rate, seach_stock_symbol, stock_price, market_status], 
    model=model,
    add_base_tools=True,
    planning_interval=3,
    additional_authorized_imports=["pandas", "numpy", "re"],
)

if __name__ == "__main__":
    GradioUI(finance_agent).launch()