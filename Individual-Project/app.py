from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
    "apiKey": "AIzaSyDsfaaN3JhUc-dGhaUb9Uon7FLj_iEE3pc",
  "authDomain": "record-book-efc72.firebaseapp.com",
  "projectId": "record-book-efc72",
  "storageBucket": "record-book-efc72.appspot.com",
  "messagingSenderId": "684479846983",
  "appId": "1:684479846983:web:0716979dae6388329aef62",
  "measurementId": "G-22Q7LMQBCE",
  "databaseURL": "https://record-book-efc72-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('display_user'))
        except:
            error = "Authentication Failed"    
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        # try: 
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        UID = login_session['user']['localId']
        user = {"username": username,"email": email, "password": password}
        db.child("Users").child(UID).set(user)
        return redirect(url_for('display_user'))
        # except: 
        #     error = "Authentication Failed"

    return render_template("signup.html")

@app.route("/display_user")
def display_user():
    UID = login_session['user']['localId']
    user = db.child("Users").child(UID).get().val()
    return render_template("index.html", user = user )    

if __name__ == '__main__':
    app.run(debug=True)