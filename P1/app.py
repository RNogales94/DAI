from flask import Flask, render_template
from flask import session, redirect, url_for, request

from db import find_restaurant

import shelve
import os
import json

app = Flask(__name__)

def add_history(url):
    if 'history' not in session:
        session['history'] = []

    session['history'].append(url)
    session.modified = True

@app.route("/",  methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        db = shelve.open("user.dat")
        if  user in db and db[user]['password'] == pwd:
            session['username'] = user
            session['password'] = pwd
            session['history'] = []
            session['loggedIn'] = True
            return redirect('/users/'+session['username'])
        else:
            return render_template('home.html', loggedIn=False, username=user)

    add_history('/')
    loggedIn = 'loggedIn' in session
    return render_template('home.html', loggedIn=loggedIn)

@app.route('/gatitos')
def gatitos():
    add_history('/gatitos')

    if 'loggedIn' in session:
        return render_template('gatitos.html', loggedIn=True, username=session['username'])
    else:
        return render_template('gatitos.html', loggedIn=False)

@app.route('/restaurants')
def restaurants():
    add_history('/restaurants')

    if 'loggedIn' in session:
        return render_template('restaurants.html', loggedIn=True, username=session['username'])
    else:
        return render_template('restaurants.html', loggedIn=False)


@app.route('/api/restaurant/<key>/<value>')
def query(key, value):
    result = find_restaurant(key, value)
    myjson = [{"name":row["name"], "street":row["address"]["street"] + " " + row["address"]["building"], "borough":row["borough"],  "cuisine":row["cuisine"]} for row in result]
    return json.dumps(myjson)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/users/<username>', methods = ['GET', 'POST'])
def profile(username):
    u = username
    h = session['history']
    if request.method == 'POST':
        db = shelve.open("user.dat", writeback=True)
        pwd = request.form['password']
        db[username]['password'] = pwd
        db.close()
        return render_template('profile.html', username=u, history=h, password=pwd)
    else:
        add_history('/users/'+username)
        db = shelve.open("user.dat")
        pwd = db[username]['password']
        db.close()

        return render_template('profile.html', username=u, history=h, password=pwd)

@app.route('/register',  methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        db = shelve.open("user.dat")
        db[user] = {'username':user, 'password':pwd}
        db.close()

        session['username'] = user
        session['password'] = pwd
        session['history'] = []
        return redirect('/users/'+session['username'])

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', debug=True)
