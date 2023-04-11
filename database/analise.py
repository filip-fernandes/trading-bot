import pandas as pd
import sqlalchemy
from model import MarketData
from sqlalchemy.orm import sessionmaker


engine = sqlalchemy.create_engine('sqlite:///MarketData.db')
Session = sessionmaker(bind=engine)
session = Session()

def get_current_time():
   return session.query(MarketData).all()[-1].close_time

def get_data(interval):
   # get data at time t and data at time t-interval
   t = get_current_time()
   batch_present = session.query(MarketData).filter(MarketData.close_time == t).all()
   batch_past = session.query(MarketData).filter(MarketData.close_time == t - interval).all()
   current_data = [{"symbol": item.symbol,
                    "price": item.last_price} for item in batch_present]
   past_data =  [{"symbol": item.symbol,
                  "price": item.last_price} for item in batch_past]
   return current_data, past_data

def hot_tokens(interval, threshold):
   assert interval < get_current_time()
   current_data, past_data = get_data(interval)
   percentages = dict()
   for present, past in zip(current_data, past_data):
      try:
         percentages[present["symbol"]] = round(((present["price"] - past["price"])/present["price"]) * 100, 2)
      except ZeroDivisionError:
         percentages[present["symbol"]] = 0.0
   
   tokens = []
   for item in percentages:
      if percentages[item] >= threshold:
         tokens.append(item)

   return tokens

while True:
   print(hot_tokens(10, 1.0), get_current_time())
