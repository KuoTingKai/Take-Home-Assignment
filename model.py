from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from financial_data import FinancialData
import math

class parameters_get(FinancialData):
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:cov45154551@localhost:3306/homework')
        self.table = FinancialData.__table__

    
    def get(self, start=None, end=None, symbol='IBM', limit=5, page=1):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        if start is None:
            existing_record = session.query(self.table.c.date).all()
        elif end is None:
            existing_record = session.query(self.table).filter(self.table.c.date >= start).all()
        else:
            existing_record = session.query(self.table).filter(self.table.between(start, end)).all()
        print(existing_record)
        record_count = len(existing_record)
        pages = math.ceil(record_count / limit)
        offset = (pages - 1) * limit
        # existing_records = existing_records[offset:offset + limit]

        # pagination = {
        #     "count": record_count,s
        #     "page": page,
        #     "limit": limit,
        #     "pages": pages
        # },
        return existing_record