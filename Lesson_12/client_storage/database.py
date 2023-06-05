from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Contacts, MessageHistory


DB_URL = 'sqlite:///client_db.sqlite3'


class ClientStorage:
    def __init__(self, db_url=DB_URL):
        self.engine = create_engine(db_url, echo=False, pool_recycle=7200)
        self.metadata = Base.metadata
        self.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_contact(self, contact):
        if not self.session.query(Contacts).filter_by(contact=contact).count():
            record = Contacts(contact)
            self.session.add(record)
            self.session.commit()

    def save_message(self, from_user, to_user, message):
        record = MessageHistory(from_user, to_user, message)
        self.session.add(record)
        self.session.commit()


if __name__ == '__main__':
    db = ClientStorage()
    db.add_contact('user1')
    db.add_contact('user2')
    db.save_message('user1', 'user2', 'test message')
