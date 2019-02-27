from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import abort
from flask import url_for

from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "st7x87F+9_!XyYmjr$zm8k9YdrpFDLf*\
                  XZYrDy@YDaaF5pvk6W+!s8LF%v=BXdZw"
DBNAME = "MediSec"
app.config['MONGO_URI'] = f"mongodb://localhost:27017/{DBNAME}"
mongo = PyMongo(app)


@app.route('/')
def index():
    """Returns the index.html template"""
    return render_template("index.html")


@app.route('/encrypt')
def encrypt():
    return render_template("encrypt.html")


@app.route('/decrypt')
def decrypt():
    """Returns all documents in a collection to decrypt.html"""
    data = mongo.db.Users.find({})

    return render_template("decrypt.html",
                           data=data)


@app.route('/save', methods=['POST'])
def save():
    """Saves the given encrypted_input_res to the database"""
    wrapper = {}
    for data_label, data_item in request.form.items():
        wrapper[data_label] = data_item
    mongo.db.Users.insert_one(wrapper)

    return redirect("/decrypt")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """GET: Returns the page allowing the user to register with the service.\n
    POST: Processes the register form and registers the user with the service.
    """
    if checkUserAuth():
        return redirect('/home')

    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password_hash']
        salt = request.form['password_salt']
        sec_question = request.form['sec_question']
        if sec_question != "4":
            err_msg = 'Wrong security question answer!'
            return render_template('register.html',
                                   error_message=err_msg)
        document = {}
        document['email'] = email_address
        document['password'] = password
        document['password_salt'] = salt
        try:
            mongo.db.Users.insert_one(document)
        except IOError as error:
            return render_template('register.html',
                                   error_message=error)
        return redirect('/')

    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """GET: Returns the page allowing the user to login into the service.\n
    POST: Allow the user to enter in password with retrieved salt.
    """
    if checkUserAuth():
        return redirect('/home')

    if request.method == 'POST':
        email_address = request.form['email_address']
        if getUserAccount(email_address):
            session['login_email_address'] = email_address
            document = getUserAccount(email_address)[0]
            password_salt = document['password_salt']
            return render_template('login_password.html',
                                   password_salt=password_salt,
                                   email_address=email_address)
        else:
            return render_template('login_username.html',
                                   error_message="Username not found.")
    else:
        return render_template('login_username.html')


@app.route('/validate_login', methods=['POST'])
def validate_login():
    """POST: Validates the password and logs the user in.
    """
    email_address = request.form['email_address']
    password = request.form['password_hash']
    mongo = getUserAccount(email_address)[0]
    if mongo['password'] == password:
        # Correct Password
        session['auth'] = email_address
        return redirect('/home')
    else:
        # Wrong Password
        if not session.get('login_attempts'):
            session['login_attempts'] = 1
        elif session.get('login_attempts') == 3:
            # Lockout
            pass
        elif session.get('login_attempts') >= 1:
            session['login_attempts'] += 1
        return render_template('login_username.html',
                               error_message="Incorrect password, please try again.")


@app.route('/medicalHistory', methods=['GET'])
def medicalHistory():
    if checkUserAuth():
        # TODO show all history
        return render_template('medicalHistory.html')
    else:
        # Give 401, forbidden access
        # return redirect('/login', 403)
        abort(401)


@app.route('/addMedicalHistory', methods=['GET', 'POST'])
def addMedicalHistory():
    if checkUserAuth():
        mongo = getUserAccount(session['auth'])
        return render_template('addMedicalHistory.html', encryption_key=mongo[0]['password'])
    else:
        # Give 401, forbidden access
        abort(401)


@app.errorhandler(401)
def unauthorisedRequest(error):
    return render_template('error/401.html'), 401


# TODO Make it 500
@app.errorhandler(409)
def conflictingRequest(error):
    return render_template('error/409.html'), 409


def getUserAccount(email_address: str):
    document = mongo.db.Users.find({"email": email_address})
    if document.count() == 0:
        return None
    elif document.count() > 1:
        # Make it 500
        abort(409)
    else:
        return document


def checkUserAuth() -> bool:
    """Checks if the user is authenticated already.
    """
    if session.get('auth'):
        # User is Authenticated
        return True
    elif not session.get('auth'):
        # User is not Authenticated
        return False


if __name__ == "__main__":
    app.run(debug=True, port=404)
