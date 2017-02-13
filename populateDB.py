from model import *


engine = create_engine('sqlite:///GetBooks.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

books = [
 {'name':'Divergent', 'author':'Vironica Roth', 'photo':'something', 'price':'0', 'description':'somethimg something'}]

#user = session.query(User).first()
#this_id= user.id
#for book in books:
 	#newBook = Book(name=book['name'], author=book['author'], photo=book['photo'], price=book['price'], description=book['description'])
newBook1 = Book(name = "Harry Potter and the Cursed", author = 'J.K. Rolling', photo = '/Desktop/download.jpg', price = '5', description = 'The 8th book of the Harry Potter series')
newBook = Book(name = "The Secret Daughter", author = 'Shilpi Somaya Gowda', photo = 'https://images-na.ssl-images-amazon.com/images/I/41UZRDWMl2L._SX329_BO1,204,203,200_.jpg', price = '0', description = 'blablabla- a good book')
session.add(newBook)
session.add(newBook1)
session.commit()
# newUser= User(name='smsmmslam', address="Nazereth something", email="smsmmslam@gmail.com", password_hash='6786')
# session.add(newUser)