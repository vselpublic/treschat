from datetime import datetime
from . import db, login_manager
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from sqlalchemy.ext.declarative import declarative_base

#TODO: All this things to Model of MVC. In this script only dao.

def repr_all(**kwargs):
    representation=""
    for field, value in kwargs.items():
        representation += str(field) + " is " + str(value) + ", "
    return representation

chats_to_users_association_table=db.Table('chats_to_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chats.id')))

class User(UserMixin, db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(64), unique=True, index=True, nullable=False)
    username=db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash=db.Column(db.String(128), nullable=False)
    confirmed=db.Column(db.Boolean, default=False)
    name=db.Column(db.String(64))
    #token=db.Column(db.Text()) for future purpouse

    def __repr__(self):
        representation=repr_all(username=self.username, id=self.id)
        return representation
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash=generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_auth_token(self, expiration):
        s=Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    
class Chat(db.Model):
    __tablename__='chats'
    id=db.Column(db.Integer, primary_key=True)
    chatname=db.Column(db.String(256), index=True)
    chat_partisipants=db.relationship("User", secondary=chats_to_users_association_table,
                                        backref=db.backref("chats", lazy='dynamic'))


    def __repr__(self):
        return '<Chatname %r>' % self.chatname

class Message(db.Model):
    __tablename__='messages'
    id=db.Column(db.Integer, primary_key=True)
    userid=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chatid=db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    text=db.Column(db.String(999), index=True)
    timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r , Chat %r, Text %r>' % self.userid, self.chatid, self.text

#db.event.listen(Bookmark.text, 'set', Bookmark.on_changed_text)

class Anonymous(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False

login_manager.anonymous_user=Anonymous
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))