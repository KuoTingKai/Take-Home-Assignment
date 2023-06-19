import requests
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import inspect
import datetime


engine = create_engine('mysql+pymysql://root:cov45154551@localhost:3306/homework')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

def get_raw_data():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=60min&outputsize=full&apikey=VYT3ACM4W08OVVTR'
    r = requests.get(url)
    data = r.json()
    output = []
    symbol = 'IBM'
    Date = ''
    volume = 0
    close_price = None

    for date, values in data['Time Series (60min)'].items():
        if Date == '':
            Date = date.split()[0]
            open_price = values['1. open']
            volume = 0

        if Date != date.split()[0]:
            entry = {
                "symbol": symbol,
                "date": Date,
                "open_price": open_price,
                "close_price": close_price,
                "volume": volume
            }
            output.append(entry)
            Date = date.split()[0]
            open_price = values['1. open']
            volume = 0

        close_price = values['4. close']
        volume += int(values['5. volume'])

    return output


class FinancialData(Base):
    __tablename__ = 'financial_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(255))
    date = Column(String(255))
    open_price = Column(String(255))
    close_price = Column(String(255))
    volume = Column(Integer)


if __name__ == "__main__":
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    # 判断目标表格是否存在
    if 'financial_data' not in table_names:
        # 表格不存在，创建表格
        Base.metadata.create_all(engine)

    rawdata = get_raw_data()
    existing_records = session.query(FinancialData.date).all()
    existing_dates = set([item[0] for item in existing_records])
    # existing_dates = set(record[0].strftime("%Y-%m-%d") for record in existing_records)
    financial_list = []

    for data in rawdata:
        date = data['date']
        if date not in existing_dates:
            financial_list.append(FinancialData(**data))

    session.add_all(financial_list)
    # 提交会话（事务）
    session.commit()
    # 关闭会话
    session.close()




