import inspect
from pydantic import TypeAdapter
from openai import OpenAI
import requests
import yfinance as yf
import json
import os
from dotenv import load_dotenv
from pprint import pprint 

load_dotenv()




def get_symbol(company: str):
    """
    Retrieve stock symbol for company.
    :param company: The name of the company for which to retrieve the stock symbol.
    :output: The stock symbol for the specified company.
    """
    pprint(f'get_symbol: {company}')
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {
        "q": company,
        "country": "United States",
    }
    user_agents = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    res = requests.get(url=url, params=params, headers=user_agents)
    data = res.json()
    return data["quotes"][0]["symbol"]

def get_stock_price(symbol: str):
    """
    Retrieve the most recent stock price data for a specified company.
    :param symbol: The stock symbol for which to retrieve the data.
    :output: A dictionary containing the most recent stock price data.
    """
    pprint(f'get_stock_price: {symbol}')
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d")
    latest = hist.iloc[-1]
    pprint(latest)
    return {
        "timestamp": str(latest.name),
        "open": latest["Open"],
        "close": latest["Close"],
        "high": latest["High"],
        "low": latest["Low"],
        "volume": latest["Volume"],
    }

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_symbol",
            "description": inspect.getdoc(get_symbol),
            "parameters": TypeAdapter(get_symbol).json_schema(),
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": inspect.getdoc(get_stock_price),
            "parameters": TypeAdapter(get_stock_price).json_schema(),
        },
    }
]

# print(get_symbol("Apple"))
# print(get_stock_price("AAPL"))

# pprint(tools)



client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)

def get_completion(messages):
    return client.chat.completions.create(
        model='meta-llama-3.1-8b-instruct',
        messages=messages,
        tools=tools,
        temperature=0,
    )

messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that can retrieve stock prices for a given company",
        },
    ]

while True:
    user_input = input("Enter your question: ")
    if user_input == "e" or user_input == "q":
        break

    messages.append({
            "role": "user",
            "content": user_input,
        })

    response = get_completion(messages)
    # pprint(response)

    FUNCTION_MAP = {
        "get_symbol": get_symbol,
        "get_stock_price": get_stock_price
    }

    first_choice = response.choices[0]
    finish_reason = first_choice.finish_reason
    while  finish_reason == 'tool_calls':
        tool_call = first_choice.message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        tool_function = FUNCTION_MAP[tool_name]
        tool_result = tool_function(**tool_args)
        messages.append(first_choice.message)
        messages.append({
            'role':'tool',
            'content':json.dumps(tool_result), 
            "tool_call_id": tool_call.id,
            "name": tool_name
        })

        response = get_completion(messages)
        first_choice = response.choices[0]
        finish_reason = first_choice.finish_reason

    bot_response = response.choices[0].message.content
    messages.append({'role':'assistant', 'content':bot_response})
    pprint(bot_response)

    # if tool_name == 'get_symbol':
    #     company = tool_args['company']
    #     symbol = get_symbol(company)
    #     messages.append({'role':'tool','content':symbol})
    # elif tool_name == 'get_stock_price':
    #     symbol = tool_args['symbol']
    #     stock_price = get_stock_price(symbol)
    #     messages.append({'role':'tool','content':stock_price})