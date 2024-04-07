import yfinance as yf
from datetime import datetime
from .models import Stock, Order
import pandas as pd
import time
import pytz




def fetch_stock_data(order_id):
    order = Order.objects.get(pk=order_id)
    stock_name = order.name + ".SA"
    stock = yf.Ticker(stock_name)
    data = stock.history(period='90m',interval='1m')  # Fetch data for the specified period
    df = pd.DataFrame(data)
    ultima_info = df.iloc[-1,:]
    date = df.index[-1]
    open_price = ultima_info['Open']
    close_price = ultima_info['Close']
    high_price = ultima_info['High']
    low_price = ultima_info['Low']
    stock_obj = Stock.objects.create(order=order,name=order.name,date=date,open_price=open_price,close_price=close_price,high_price=high_price,low_price=low_price)
    if stock_obj:
        return stock_obj  
    else:
        return False
        


def convert_minutes_to_seconds(time_string):
    try:
        num = int(time_string[:-1])
        unit = time_string[-1]
        if unit == 'm':
            return num * 60  
        else:
            raise ValueError("Intervalo Invalido")
    except ValueError as e:
        print("Error:", e)
        return None


def send_alert(order,stock):
    if stock.close_price > order.upper_limit:
        print(f'{stock.name} passou do limite superior, ativo pronto para venda')
        return 'Sell'
    elif stock.close < stock.lower_limit:
        print(f'{stock.name} passou do limite inferior, ativo pronto para compra')
        return 'Buy'
    else:
        print('Nenhuma ação recomendada')