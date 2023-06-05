from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, History, Contacts


DB_URL = 'sqlite:///server_db.sqlite3'


class ServerStorage:
    def __init__(self, db_url=DB_URL):
        self.engine = create_engine(db_url, echo=False, pool_recycle=7200)
        self.metadata = Base.metadata
        self.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def log_in(self, login):
        user = self.session.query(User).filter_by(username=login).first()

        if user:
            user.last_login = datetime.utcnow()
        else:
            new_user = User(login)
            self.session.add(new_user)
        
        self.session.commit()
    
    def add_history(self, username, ip_address):
        user = self.session.query(User).filter_by(username=username).first()
        record = History(user.id, user.last_login, ip_address)
        self.session.add(record)
        self.session.commit()

    def get_history(self, username=None):
        query = self.session.query(User.username, History.login_time, 
                                   History.ip_address).join(User)
        
        if username:
            user_history = [record for record in query.all() if record[0] == username]
            return user_history

        return query.all()
    
    def get_contacts(self, username):
        user = self.session.query(User).filter_by(username=username).one()

        query = self.session.query(Contacts, User.username).filter_by(user_id=user.id). \
            join(User, Contacts.contact_id == User.id)
        
        return [contact[1] for contact in query.all()]
    
    def add_contact(self, username, contact_name):
        user = self.session.query(User).filter_by(username=username).first()
        contact = self.session.query(User).filter_by(username=contact_name).first()

        if not contact or self.session.query(Contacts).filter_by(user_id=user.id, contact_id=contact.id).count():
            return
        
        record = Contacts(user.id, contact.id)
        self.session.add(record)
        self.session.commit()

    def del_contact(self, username, contact_name):
        user = self.session.query(User).filter_by(username=username).first()
        contact = self.session.query(User).filter_by(username=contact_name).first()

        if not contact:
            return
        
        self.session.query(Contacts).filter_by(user_id=user.id, contact_id=contact.id).delete()
        self.session.commit()


if __name__ == '__main__':
    db = ServerStorage()
    for i in range(1, 7):
        db.log_in(f'user{i}')
        db.add_history(f'user{i}', f'127.0.0.{i}')

    db.add_contact('user1', 'user3')
    db.add_contact('user1', 'user4')
    db.add_contact('user5', 'user6')
    db.add_contact('user5', 'user3')
    db.add_contact('user5', 'user1')

    print(db.get_contacts('user5'))
    print(db.get_history('user1'))
    print(db.get_history())
