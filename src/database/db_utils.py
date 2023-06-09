import sqlalchemy
from sqlalchemy.orm import sessionmaker
from database.model import MarketData, Base


engine = sqlalchemy.create_engine('sqlite:///MarketData.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_data(symbol: str, interval: int = 0) -> MarketData:
    current_time = get_current_time()
    assert interval <= current_time, "Interval is too large"
    data = session.query(MarketData).filter(
        MarketData.close_time == current_time - interval, 
        MarketData.symbol == symbol
    ).all()[0]
    return data

def get_current_time() -> int:
    return session.query(sqlalchemy.func.max(MarketData.close_time)).scalar()
    
def add_to_db(data: list[MarketData]) -> None:
    session.add_all(data)
    session.commit()

def get_num_batches() -> int:
    return session.query(MarketData.close_time.distinct()).count()

def delete_old_data() -> None:
    oldest_time = session.query(MarketData.close_time.distinct()).order_by(MarketData.close_time).first()[0]
    session.query(MarketData).filter(MarketData.close_time == oldest_time).delete()
    session.commit()

