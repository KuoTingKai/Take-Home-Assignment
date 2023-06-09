from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy import inspect
from financial_data import get_raw_data


engine = create_engine('mysql+pymysql://root:cov45154551@localhost:3306/homework')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class FinancialData(Base):
    __tablename__ = 'financial_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(255))
    date = Column(String(255))
    open_price = Column(String(255))
    close_price = Column(String(255))
    volume = Column(String(255))


inspector = inspect(engine)
table_names = inspector.get_table_names()
# 判断目标表格是否存在
if 'financial_data' not in table_names:
    # 表格不存在，创建表格
    Base.metadata.create_all(engine)
    print("表格已创建")




rawdata = get_raw_data()
existing_record = session.query(FinancialData.date).all()
existing_record = set([item[0] for item in existing_record])
financial_list = []

for data in rawdata:
    date = data['date']
    if date not in existing_record:
        financial_list.append(FinancialData(**data))
        # financial_list = [FinancialData(**data) for data in rawdata]
session.add_all(financial_list)
    


# 提交会话（事务）
session.commit()

# 关闭会话
session.close()

# print(financial_list)

# for i in rawdata:
#     print(**i)
# session.add_all(rawdata)
# rows = session.query('financial_data').filter_by(comsumed_name=date).first()