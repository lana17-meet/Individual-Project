from flask import Flask, url_for, flash, render_template, redirect, request, g, send_from_directory
from flask import session as login_session
from model import *
from werkzeug.utils import secure_filename
import locale, os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


engine = create_engine('sqlite:///GetBooks.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

@app.route('/')
def HomePage():
	books = session.query(Book).all()
	ordered = session.query(Order).all()
	final = []
	canAdd = True
	for book in books:
		d= book.id
		for order in ordered:
			o = order.book_id
			if d==o:
				canAdd= False

		if(canAdd):
			final.append(book)
		canAdd = True

	return render_template('HomePage.html', books=final)

@app.route('/myBooks')
def myBooks():
	if 'id' not in login_session:
		flash("You need to be logged in")
		return redirect(url_for('logIn'))
	else:
		books = session.query(Book).all()
		ordered = session.query(Order).all()
		orderedBooks = []
		addedBooks = []
		for book in books:
			if book.user_id == login_session['id']:
				addedBooks.append(book)
		for order in ordered:
			if order.user_id == login_session['id']:
				b = session.query(Book).filter_by(book_id=order.book_id).one()
				orderedBooks.append(b)
		return render_template('myBooks.html', oBooks=orderedBooks, aBooks=addedBooks)

@app.route('/logIn', methods = ['GET','POST'])
def logIn():
	if request.method == 'GET':
		if 'id' in login_session:
			flash("You're already logged in")
		 	return redirect(url_for('HomePage'))
		return render_template('logIn.html')
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email is None or password is None:
			flash('Missing Arguments')
			return redirect(url_for('logIn'))
		user = session.query(User).filter_by(email=email).first()		
		if not user or not user.verify_password(password):
		 	flash('Incorrect username/password combination')
		 	return redirect(url_for('logIn'))
		else:
		 	flash('Login Successful, welcome, %s' % user.name)
		 	login_session['name'] = user.name
		 	login_session['email'] = user.email
		 	login_session['id'] = user.id
		 	return redirect(url_for('HomePage'))

@app.route('/addBook', methods = ['GET','POST'])
def addBook():
	if 'id' not in login_session:
		flash("You need to be logged in")
		return redirect(url_for('logIn'))
	else:
		if request.method == 'GET':
			return render_template('addBook.html')
		else:
			name = request.form["name"]
			author = request.form["author"]
			price = request.form["price"]
			description= request.form["description"]
			if name is None or author is None or price is None or 'file' not in request.files:
				flash('There are missing arguments')
				return redirect(url_for('addBook'))
			file = request.files['file']
			# if file.filename=='':
			# 	flash('No file selected')
		    #	return redirect(url_for('addBook'))
			flash(file.filename)
			if file and allowed_file(file.filename):

				book = Book(name = name, author = author, price = price, description = description, user_id = login_session['id'])
				session.add(book)
				session.commit()
				filename = str(book.id) + "_" + secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				book.set_photo(filename)
				session.add(book)
				session.commit()
				flash("Book Added Successfuly!")
				return redirect(url_for('HomePage'))
			else:
				flash("Please upload either a .jpg, .jpeg, .png, or .gif file.")
				return redirect(url_for('addBook'))


@app.route('/logout')
def logout():
	if 'id' in login_session:
		del login_session['name']
		del login_session['email']
		del login_session['id']
		flash("Logged Out Successfully")
	return redirect(url_for('HomePage'))


# @app.route('/showBook/<int:book_id>', methods = ['GET','POST'])
# def showBook(book_id):
# 	if request.method == "GET":
# 		book = session.query(Book).filter_by(id=book_id).one()
# 		return render_template('showBook.html', book=book)
# 	else:
# 		if 'id' not in login_session:
# 			flash("You need to be logged in")
# 			return redirect(url_for('logIn'))
# 		order = Order(user_id=login_session['id'], book_id=book_id, total_price=book.id)
# 		session.add(order)
# 		session.commit()
# 		flash('This book was ordered successfuly')
# 		return redirect(url_for("HomePage"))


@app.route("/showBook/<int:book_id>")
def showBook(book_id):
		book = session.query(Book).filter_by(id=book_id).one()
		return render_template('showBook.html', book=book)

@app.route("/showBook/<int:book_id>/order", methods = ['POST'])
def order(book_id):
	if 'id' not in login_session:
		flash("You need to be logged in")
		return redirect(url_for('logIn'))
	b = session.query(Book).filter_by(id=book_id).one()
	order = Order(user_id=login_session['id'], book_id=book_id, total_price=b.price)
	session.add(order)
	session.commit()
	flash('This book was ordered successfuly')
	return redirect(url_for('HomePage'))


@app.route('/signUp', methods = ['GET','POST'])
def signUp():

	if request.method == "GET":
		return render_template('signUp.html')
	else:
		name = request.form['name']
		email = request.form['email']
		address = request.form['address']
		password = request.form['password']
		if name is None or email is None or address is None or password is None:
			flash("Your form is missing arguments")
		 	return redirect(url_for('signUp'))
		if session.query(User).filter_by(email=email).first() is not None:
			flash("A user with this email address already exists")
			return redirect(url_for('signUp'))
		user = User(name = name, email=email, address = address)
        user.hash_password(password)
        session.add(user)
        session.commit()
        flash("User Created Successfully!")
        return redirect(url_for('logIn'))

if __name__=='__main__':
	app.run()


