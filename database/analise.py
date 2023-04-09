import pandas as pd
import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:///MarketData.db')
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_sql(session, engine)
print(df)
while True:
   if session.new or session.dirty:
      print('yop')
   print('nah')