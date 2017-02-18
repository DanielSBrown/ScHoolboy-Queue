#!/usr/bin/python
from flask import Flask, redirect, url_for, request, render_template, make_response
import sqlite3 as sql
import database

app = Flask(__name__)

#home page
#group code inputted here
@app.route('/')
def landing():
    return render_template('landing.html')

#login page
#needs to verify user and password validity
@app.route('/login/', methods= ['GET', 'POST'])
def login():
    return render_template('login.html')

#page when group code entered
#needs to verify groupcode
#should display group name, queue, group members
@app.route('/group/', methods= ['GET', 'POST'])
def group():
    if request.method=='POST':
        groupcode = request.form['groupcode']
        return render_template('group.html')

#page for user profile
#should display user's groups
@app.route('/profile/', methods= ['GET', 'POST'])
def user_profile():
    name = request.cookies.get('name')
    pw = request.cookies.get('pw')
    return render_template('profile.html', name = name)

#cookie is set after sign up or log in
@app.route('/setcookie/', methods=['POST', 'GET'])
def setcookie():
    if request.method=='POST':
        name = request.form['username']
        pw = request.form['password']
        resp = make_response(render_template('profile.html'))
        resp.set_cookie('name', name)
        resp.set_cookie('pw', pw)
        return redirect('/profile/')

#signup page
#needs to verify if user already exists
@app.route('/signup/')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)