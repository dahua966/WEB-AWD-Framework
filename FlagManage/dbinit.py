import os,time
from datetime import date
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import FLOAT, VARCHAR, INTEGER
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ROUND_TIME = 5*60  #huasir

connect_str = 'sqlite:///%s' % os.path.join(os.getcwd(), 'flag.db3')

BaseModel = declarative_base()
engine = create_engine(connect_str, echo=False, pool_recycle=3600)
db = scoped_session(sessionmaker(bind=engine))

class Flag(BaseModel):
    __tablename__ = 'flag'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    flag = Column(VARCHAR(200), unique=True,nullable=True)
    stime = Column(INTEGER,default=int(time.time()))

    def __repr__(self):
        return '%s' % self.flag

    @staticmethod
    def clear():
        result = db.query(Flag).filter(Flag.stime < str(int(time.time())-ROUND_TIME)).delete()
        db.commit()
        print "[*]delete %d overdue flag" % result
            
    @staticmethod
    def getflag():
        result = db.query(Flag).filter(Flag.stime > str(int(time.time())-ROUND_TIME)).all()
        return result

    @staticmethod
    def ifexist(text):
        result = db.query(Flag).filter(Flag.flag==text).count()
        return result

class Success(BaseModel):
    __tablename__ = 'success'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    flag = Column(VARCHAR(200), unique=True,nullable=True)
    stime = Column(INTEGER,default=int(time.time()))

    def __repr__(self):
        return '%s' % self.flag

    @staticmethod
    def ifexist(text):
        result = db.query(Success).filter(Success.flag==text).count()
        return result

    @staticmethod
    def clear():
        result = db.query(Success).filter(Success.stime < str(int(time.time())-ROUND_TIME)).delete()
        db.commit()
        print "[*]delete %d success flag" % result

def main():
    BaseModel.metadata.create_all(engine)

if __name__ == '__main__':
    main()
    # print connect_str
