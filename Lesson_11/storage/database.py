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

    def get_user_by_login(self, login):
        user = self.session.query(User).filter_by(username=login).first()
        return user


if __name__ == '__main__':
    db = ServerStorage()
    db.log_in('user1')
    print(db.get_user_by_login('user1').id)
