from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
# import web3 

# web3 = web3.HTTPProvider('https://mainnet.infura.io/v3/9e7bd8283d1d4879932988ab9907f137')


# print(web3.isConnected())
# from web3 import Web3

# # infura_url = 'https://mainnet.infura.io/v3/9e7bd8283d1d4879932988ab9907f137'
# web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/9e7bd8283d1d4879932988ab9907f137'))

# print(web3.isConnected())









Config = {
  'apiKey': "AIzaSyBCeiwxqi_Lv6Iv8nZJjQHjp6q4LZXq3rI",
  'authDomain': "y2-project.firebaseapp.com",
  'projectId': "y2-project",
  'storageBucket': "y2-project.appspot.com",
  'messagingSenderId': "830798748410",
  'appId': "1:830798748410:web:62cf9fa7258a6711dd8743",
  'measurementId': "G-77Q49KCPFL",
  "databaseURL": "https://y2-project-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def sign_in():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('home'))
       except:
        error = "Authentication failed"
        return render_template("sign_up.html")
   else:
        return render_template("sign_in.html")

    


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       username = request.form['username']
       try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        user = {'email': email, 'password': password, 'username': username}
        db.child("Users").child(login_session['user']['localId']).set(user)
        return redirect(url_for('home'))
       except:
        error = "Authentication failed"
        return render_template("sign_up.html")
   else:
        return render_template("sign_up.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    posts = db.child('Posts').get().val()
    users = db.child('Users').child(login_session['user']['localId']).get().val()['username']
    emails = db.child('Users').child(login_session['user']['localId']).get().val()['email']
    return render_template('home.html', posts = posts, users = users, emails = emails)



@app.route('/post', methods=['GET', 'POST'])
def post():
   error = ""
   if request.method == 'POST':
    name = request.form['name']
    problem = request.form['problem']
    description= request.form['description']
    coin = request.form['coin']
    address = request.form['address'] 

    try:
        post = {'name': name, 'problem': problem, 'description': description, 'coin': coin, 'address': address, 'uid': login_session['user']['localId']}
        db.child("Posts").push(post)
        return redirect(url_for('home'))
    except:
        error = "Authentication failed"
        raise
        return render_template("post.html")
   else:
        return render_template("post.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('sign_in'))

@app.route('/view_tweet')
def view_tweet():
    posts = db.child('Posts').get().val()
    return render_template('view_tweet.html', posts = posts)


if __name__ == '__main__':
    app.run(debug=True)