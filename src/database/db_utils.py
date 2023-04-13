import sqlalchemy
from sqlalchemy.orm import sessionmaker
from database.model import MarketData, Base

engine = sqlalchemy.create_engine('sqlite:///MarketData.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_data(symbol, current_time, interval=0):
    data = session.query(MarketData).filter(
        MarketData.close_time == current_time - interval, 
        MarketData.symbol == symbol
    ).all()[0]
    return data

def get_current_time():
    return session.query(sqlalchemy.func.max(MarketData.close_time)).scalar()
    
def add_to_db(data):
    session.add_all(data)
    session.commit()

def get_num_batches():
    return session.query(MarketData.close_time.distinct()).count()

def delete_old_data():
    oldest_time = session.query(MarketData.close_time.distinct()).order_by(MarketData.close_time).first()[0]
    session.query(MarketData).filter(MarketData.close_time == oldest_time).delete()
    session.commit()