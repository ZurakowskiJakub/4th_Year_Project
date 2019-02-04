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


if __name__ == "__main__":
    app.run(debug=True)
