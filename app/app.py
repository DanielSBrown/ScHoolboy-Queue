from flask import Flask, redirect, url_for, request, render_template, make_response

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login/', methods= ['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/group/', methods= ['GET', 'POST'])
def group():
    if request.method=='POST':
        groupcode = request.form['groupcode']
        return render_template('group.html')

@app.route('/profile/', methods= ['GET', 'POST'])
def user_profile():
    name = request.cookies.get('name')
    pw = request.cookies.get('pw')
    return render_template('profile.html', name = name)

@app.route('/setcookie/', methods=['POST', 'GET'])
def setcookie():
    if request.method=='POST':
        name = request.form['username']
        pw = request.form['password']
        resp = make_response(render_template('profile.html'))
        resp.set_cookie('name', name)
        resp.set_cookie('pw', pw)
        return redirect('/profile/')
if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)