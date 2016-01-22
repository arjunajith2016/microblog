# all the imports
import os
import sqlite3
import datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, send_from_directory, jsonify
from contextlib import closing
from werkzeug import secure_filename


# configuration
DATABASE = './flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# functions
def debugdb():
    cur = g.db.execute('select * from users')
    print cur.fetchall()
    cur = g.db.execute('select * from entries')
    print cur.fetchall()

# database connection
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# setting up views

#@app.route('/user/like/<id>', methods=['PUT'])
@app.route('/like/<id>', methods=['PUT'])
def addlike(id):
    post = int(id)
    likelist=[]
    flag3='n'

    f = open('./likes/'+id, 'a')
    f.close()

    with open('./likes/'+id) as f:
        likelist = f.read().splitlines()
    if session['user'] in likelist:
        likelist.remove(session['user'])
        g.db.execute('update entries set likes = likes - 1 WHERE id=(?)', [post])
        g.db.commit()
    else:
        likelist.append(session['user'])
        g.db.execute('update entries set likes = likes + 1 WHERE id=(?)', [post])
        g.db.commit()
        flag3='y'
    f.close()
    f = open('./likes/'+id, 'w')
    for item in likelist:
        f.write("%s\n" % item)
    f.close()
    cur = g.db.execute('select likes from entries where id=(?)', [post])
    g.db.commit()
    #debugdb()
    entries = [dict(likes=row[0]) for row in cur.fetchall()]
    if entries[0]['likes']==None:
        return '0'
    return flag3+str(entries[0]['likes'])
    #return 'Success'

@app.route('/')
def home():
    cur = g.db.execute('select title, text, date, time, id, user, likes from entries order by id desc')
    entries = [dict(title=row[0], text=row[1], date=row[2], time=row[3], id=row[4], user=row[5], likes=row[6]) for row in cur.fetchall()]
    return render_template('home.html', entries=entries)

@app.route('/<username>')
def user(username):
    cur = g.db.execute('select title, text, date, time, id, user, likes from entries where user = (?) order by id desc', [username])
    entries = [dict(title=row[0], text=row[1], date=row[2], time=row[3], id=row[4], user=row[5], likes=row[6]) for row in cur.fetchall()]
    return render_template('user.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    t=datetime.datetime.now()
    current_date=str(getattr(t,'day'))+'-'+str(getattr(t,'month'))+'-'+str(getattr(t,'year'))
    if getattr(t,'hour') < 12:
        current_time=str(getattr(t,'hour'))+':'+str(getattr(t,'minute'))+' AM'
    elif getattr(t,'hour') == 12:
        current_time=str(getattr(t,'hour'))+':'+str(getattr(t,'minute'))+' PM'
    elif getattr(t,'hour') > 12:
        current_time=str(getattr(t,'hour')-12)+':'+str(getattr(t,'minute'))+' PM'

    if not session.get('logged_in'):
        abort(401)
    if request.form['title'] =='':
        flash('Title cannot be empty')
    elif request.form['text']=='':
        flash('Body cannot be empty')
    else:
        g.db.execute('insert into entries (title, text, date, time, user, likes) values (?, ?, ?, ?, ?, ?)', [request.form['title'], request.form['text'], current_date, current_time, session['user'], 0])
        g.db.commit()
        flash('New entry was successfully posted')
    return redirect(url_for('home'))

@app.route('/del', methods=['POST'])
def del_entry():
    g.db.execute('delete from entries where id=(?)', [request.form['del']])
    g.db.commit()
    flash('Post deleted')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password from users where username=(?)', [request.form['username']])
        users = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]

        flag2=0
        for item in users:
            if request.form['username'] == item['username']:
                flag2=1
        
        if request.form['name']=='':
            flash('Name cannot be empty')
        elif request.form['username']=='':
            flash('Username cannot be empty')
        elif request.form['password']=='':
            flash('password cannot be empty')
        elif request.form['name']=='login':
            flash('You cannot have your name as login')
        elif request.form['name']=='logout':
            flash('You cannot have your name as logout')
        elif request.form['name']=='register':
            flash('You cannot have your name as register')
        elif flag2 == 0:
            g.db.execute('insert into users (name, username, password) values (?, ?, ?)', [request.form['name'], request.form['username'], request.form['password']])
            g.db.commit()
            flash('You have been registered')
            return redirect(url_for('home'))
        else:
            flash('Username already exists')
    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password, name from users where username=(?)', [request.form['username']])
        users = [dict(username=row[0], password=row[1], name=row[2]) for row in cur.fetchall()]

        flag2=0
        for item in users:
            if request.form['username'] == item['username']:
                flag2=1
                if request.form['password'] == item['password']:
                    session['logged_in'] = True
                    session['user'] = item['name']
                    flash(str('Welcome back, %s' %item['name']))
                    return redirect(url_for('home'))

        if flag2==0:
            error = 'Invalid username'
        elif flag2==1:
            error = 'Invalid password'
    return render_template('login.html', flag=True, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# to start the server
if __name__ == '__main__':
    #init_db()
    app.run(host='0.0.0.0')

