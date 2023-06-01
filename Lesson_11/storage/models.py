from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    last_login = Column(DateTime, default=datetime.utcnow,
                        server_default=func.now())
    contacts_id = Column(Integer, ForeignKey("contacts.id"))
    contacts = relationship("Contacts", back_populates="users")

    def __init__(self, username):
        self.username = username


class History(Base):
    __tablename__ = 'user_history'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"), unique=True)
    login_time = Column(DateTime)
    ip_address = Column(String)

    def __init__(self, user_id, login_time, ip):
        self.user = user_id
        self.login_time = login_time
        self.ip_address = ip


class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    users = relationship("User", back_populates="contacts")



