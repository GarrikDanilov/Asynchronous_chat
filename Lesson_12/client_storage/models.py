from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    contact = Column(String)

    def __init__(self, contact):
        self.contact = contact


class MessageHistory(Base):
    __tablename__ = 'message_history'
    id = Column(Integer, primary_key=True)
    from_user = Column(String)
    to_user = Column(String)
    message = Column(String)
    date = Column(DateTime, default=datetime.utcnow,
                        server_default=func.now())
    
    def __init__(self, from_user, to_user, message):
        self.from_user = from_user
        self.to_user = to_user
        self.message = message
