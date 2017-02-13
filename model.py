from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    order = relationship("Order", back_populates="user")
    book = relationship("Book", uselist=False, back_populates="user")

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
 

class Book(Base):
	__tablename__ = 'book'
	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	author = Column(String(255))
	photo = Column(String)
	price = Column(Float(255))
	description = Column(String(500))
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship('User', back_populates="book")
	order = relationship("Order", back_populates="book")

	def set_photo(self, photo):
		self.photo = photo


class Order(Base):
	__tablename__ = 'order'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	book_id = Column(Integer, ForeignKey('book.id'))
	total_price = Column(Float(255))
	user = relationship("User", back_populates="order")
	book = relationship("Book", back_populates="order")


engine = create_engine('sqlite:///GetBooks.db')


Base.metadata.create_all(engine)