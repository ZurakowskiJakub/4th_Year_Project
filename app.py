from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/MediSec"
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

    return render_template("decrypt.html", data=data)


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
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password_encrypted']
        sec_question = request.form['sec_question']
        if sec_question != "4":
            err_msg = 'Wrong security question answer!'
            return render_template('register.html', error_message=err_msg)
        document = {}
        document['email'] = email_address
        document['password'] = password
        try:
            mongo.db.Users.insert_one(document)
        except IOError as error:
            return render_template('register.html', error_message=error)
        return redirect('/')

    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """GET: Returns the page allowing the user to login into the service.\n
    POST: Processes the login information and logs the user with the service.
    """
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password_encrypted']
        sec_question = request.form['sec_question']
        if sec_question != "4":
            err_msg = 'Wrong security question answer!'
            return render_template('login.html', error_message=err_msg)
        document = mongo.db.Users.find({"email": email_address})
        if document is None:
            # TODO return 404
            return redirect('/')
        elif document.count() > 1:
            # TODO return 500
            return redirect('/')
        else:
            if document[0]['password'] == password:
                # TODO logged in
                return render_template('temp.html', message="Logged In")
            else:
                # TODO wrong password
                return render_template('temp.html', message="Wrong password")
    else:
        return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True, port=404)