from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash, _app_ctx_stack
from urlparse import urlparse, urlunparse

# DB config
DATABASE = "gifts.db"
DEBUG = True
SECRET_KEY = "insert key here"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('GIFTS_SETTINGS', silent=True)

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

def get_db():
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
	return top.sqlite_db

@app.teardown_appcontext
def close_db_connection(exception):
	top = _app_ctx_stack.top
	if hasattr(top, 'sqlite_db'):
		top.sqlite_db.close()

@app.route('/')
def show_homepage():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	db = get_db()
	cur = db.execute('select pw_hash, pw_salt, id from users where email=?', 
		[request.form['username']])

	r = cur.fetchall()

	if (len(r) < 1) or (request.form['password'] + r[0][1]) != r[0][0]:
		flash("Invalid username or password")
		return redirect(url_for('show_homepage'))
	else:
		session['logged_in'] = True
		session['user_id'] = r[0][2]
		return redirect(url_for('show_gifts'))

@app.route('/gifts')
def show_gifts():
	if not session['logged_in']:
		return redirect(url_for('login'))

	db = get_db()
	cur = db.execute('select id, name from users')
	users = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]

	for user in users:
		cur = db.execute('select id, title, url, price, desc from gifts where user_id=?', [user['id']])
		user['gifts'] = [dict(id=row[0], title=row[1], url=row[2], price=row[3], desc=row[4]) for row in cur.fetchall()]

	return render_template('gifts.html', users=users)

@app.route('/gifts/<giftid>')
def show_gift(giftid):
	if not session['logged_in']:
		return redirect(url_for('login'))

	db = get_db()
	cur = db.execute('select id, title, url, desc from gifts where id=?', [user['id']])
	gifts = [dict(id=row[0], title=row[1], url=row[2], desc=row[3]) for row in cur.fetchall()]

	if len(gifts) < 1:
		return redirect(url_for('show_gifts'))
	else:
		return render_template('gift_detail.html', gift=gifts[0])

@app.route('/gifts/new', methods=['GET', 'POST'])
def new_gift():
	if not session['logged_in']:
		return redirect(url_for('login'))

	if request.method == 'GET':
		return render_template('gift_new.html')
	else:
		title = request.form['title']
		url = request.form['url']
		price = request.form['price']
		desc = request.form['desc']

		if title == "" or url == "" or price == "":
			flash("Sorry, need a title, URL, and price")
			return render_template('gift_new.html')

		try:
			price = int(price)
		except ValueError:
			flash("Sorry, price must be a number")
			return render_template('gift_new.html')

		try:
			url = urlunparse(urlparse(url, 'http'))
		except Exception:
			flash("Sorry, invalid url")
			return render_template('gift_new.html')

		db = get_db()
		cur = db.execute('insert into gifts (user_id, title, url, price, desc) values (?, ?, ?, ?, ?)', 
			[session['user_id'], title, url, price, desc])
		db.commit()
		return redirect(url_for('show_gifts'))

if __name__ == '__main__':
	init_db()
	app.run()
