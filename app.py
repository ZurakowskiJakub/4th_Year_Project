from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import abort
from flask import url_for
from flask import flash

from flask_pymongo import PyMongo

from datetime import datetime
from datetime import timedelta

from util import email
from util import token

import hashlib

import random

app = Flask(__name__)

# IMPORTANT, NOT in version control.
app.config.from_json("config.json")
mongo = PyMongo(app)


# CHECK DATABASE
def print_sys_msg(msg: str) -> None:
    """Prints a system message.
    Enclosed by multiple stars and stuff.
    """
    msg = f"{datetime.now()}\t{str(msg)}"
    stars = "*" * 50
    print(stars, msg, stars, sep="\n")


# DB Collections
collections = [
    'Users'
]
for collection in collections:
    if collection not in mongo.db.collection_names(False):
        print_sys_msg(f"{collection} collection not in the Database. Dying.")
        exit()
    else:
        print_sys_msg(f"{collection} collection in the Database. OK.")


@app.route('/')
def index():
    """Returns the index.html template"""
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """GET: Returns the page allowing the user to register with the service.\n
    POST: Processes the register form and registers the user with the service.
    """
    # IF USER IS AUTHENTICATED, PUSH HIM TO HOME
    if checkUserAuth():
        return redirect(url_for('medicalHistory'))

    if request.method == 'POST':
        # TAKE IN THE INPUT
        email_address = request.form['email_address'].lower()
        password = request.form['password']

        # CHECK IF EMAIL ALREADY TAKEN
        if getUserAccount(email_address):
            return render_template('register.html',
                                   error_message="Sorry, that username is \
                                                 already taken.")

        # GENERATE SALT AND HASH
        now = str(datetime.now())
        salt = hashlib.sha256(bytes(now, encoding='utf8'))
        pass_hash = hashlib.sha256(
            bytes(
                (salt.hexdigest() + password),
                encoding='utf8'
            )
        )

        # CREATE A DICTIONARY WITH DETAILS
        document = {}
        document['email'] = email_address
        document['password'] = {
            'salt': salt.hexdigest(),
            'hash': pass_hash.hexdigest()
        }
        document['login_attempts'] = 0
        document['account_locked'] = False
        document['account_locked_time'] = datetime.utcnow()
        document['valid_email'] = False

        # GENERATE A RANDOM TOKEN FOR ENC KEY
        rand_token = '%030x' % random.randrange(16 ** 30)
        while mongo.db.Users.find({"token": rand_token}).count() > 0:
            rand_token = '%030x' % random.randrange(16 ** 30)
        document['token'] = rand_token

        # ATTEMPT TO PERSIST THE DATA
        try:
            mongo.db.Users.insert_one(document)
        except IOError:
            return render_template('register.html',
                                   error_message="There was an issue saving \
                                                 your data. Please try again.")
        verification_token = token.generateToken(email_address)
        email.sendVerificationEmail(email_address, verification_token)
        return redirect(url_for('login'))

    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """GET: Returns the page allowing the user to login into the service.\n
    POST: Allow the user to enter in password with retrieved salt.
    """
    # IF USER IS AUTHENTICATED, PUSH HIM TO HOME
    if checkUserAuth():
        return redirect(url_for('medicalHistory'))

    if request.method == 'POST':
        # GENERAL RENDER TEMPLATES
        ERROR_MESSAGE = "There was an issue logging you in, please try again."
        LOCK_MESSAGE = "This account has been locked. Please try again later."
        EMAIL_MESSAGE = "Please validate your email address."
        GEN_TEMPLATE = render_template('login.html',
                                       error_message=ERROR_MESSAGE)
        LOCK_TEMPLATE = render_template('login.html',
                                        error_message=LOCK_MESSAGE)
        EMAIL_TEMPLATE = render_template('login.html',
                                         error_message=EMAIL_MESSAGE)

        # TAKE IN THE INPUT
        email_address = request.form['email_address'].lower()
        password = request.form['password']

        # GET THE USER DOCUMENT
        if getUserAccount(email_address):
            document = getUserAccount(email_address)

            # CHECK IF ACCOUNT HAS VALIDATED EMAIL
            if document['valid_email'] is False:
                return EMAIL_TEMPLATE

            # CHECK IF ACCOUNT IS LOCKED
            if document['account_locked']:
                if document['account_locked_time'] + timedelta(minutes=5) <= datetime.utcnow():
                    if not updateUserAccount(email_address, {
                        "$set": {
                            "login_attempts": 1,
                            "account_locked": False
                        }
                    }):
                        return GEN_TEMPLATE
                else:
                    return LOCK_TEMPLATE

            # GENERATE SALT AND HASH
            salt = document['password']['salt']
            pass_hash = hashlib.sha256(
                bytes(
                    (salt + password),
                    encoding='utf8'
                )
            )

            # PASSWORDS MATCH
            if pass_hash.hexdigest() == document['password']['hash']:
                if not updateUserAccount(email_address, {
                    "$set": {
                        "login_attempts": 0,
                        "last_login": datetime.utcnow()
                    }
                }):
                    return GEN_TEMPLATE
                session['auth'] = email_address
                return redirect(url_for('medicalHistory'))

            # PASSWORDS DON'T MATCH
            else:
                # LOCK ACCOUNT ON LOGIN ATTEMPTS = 3
                if document['login_attempts'] == 3:
                    if not updateUserAccount(email_address, {
                        "$set": {
                            "account_locked": True,
                            "account_locked_time": datetime.utcnow()
                        }
                    }):
                        return GEN_TEMPLATE
                # INCREMENT LOGIN ATTEMPTS
                else:
                    if not updateUserAccount(email_address, {
                        "$inc": {
                            "login_attempts": 1
                        }
                    }):
                        return GEN_TEMPLATE
                    return GEN_TEMPLATE
        else:
            return GEN_TEMPLATE
    else:
        return render_template('login.html')


@app.route('/validateEmail/<user_token>', methods=['GET'])
def validateEmail(user_token):
    # IF LOGGED IN, REDIRECT TO HOME
    if checkUserAuth():
        return redirect(url_for('medicalHistory'))
    
    valid_token = token.confirmToken(user_token)
    if valid_token is not False:
        updateUserAccount(valid_token, {
            "$set": {
                "valid_email": True
            }
        })
        flash("Email sucessfully validated.", category="info")
        return redirect(url_for('login'))
    else:
        flash("Email unsucesfully validated. Please try again.",
              category="error")
        return redirect(url_for('resendValidationEmail'))


@app.route('/resendValidationEmail', methods=['GET', 'POST'])
def resendValidationEmail():
    """GET: Returns the page to resend the validation email.
    POST: Checks the email and sends out a new validation email.
    """
    # IF LOGGED IN, REDIRECT TO HOME
    if checkUserAuth():
        return redirect(url_for('medicalHistory'))

    if request.method == 'POST':
        email_address = request.form['email_address'].lower()
        if getUserAccount(email_address) is False:
            flash("Error sending validation email address. Please try again.",
                  category="error")
            return redirect(url_for('resendValidationEmail'))
        verification_token = token.generateToken(email_address)
        email.sendVerificationEmail(email_address, verification_token)
        flash("Validation email sent!", category="info")
        return redirect(url_for('login'))
    else:
        return render_template('resendValidationEmail.html')


@app.route('/medicalHistory', methods=['GET'])
def medicalHistory():
    if checkUserAuth():
        mongo = getUserAccount(session['auth'])
        token = mongo.get('token')
        if mongo.get('history'):
            if mongo.get('account'):
                account = mongo['account']
            else:
                account = None
            medical_history = mongo.get('history')
            medical_history.reverse()
            category = None
            if request.args.get('cat'):
                category = request.args.get('cat')
                medical_history = list(filter(lambda a: a['type'] == category, medical_history))
            sort = "dateDsc"
            if request.args.get('sort'):
                sort = request.args.get('sort')
            if sort == "dateAsc":
                medical_history.reverse()
            res_lim = "10"
            if request.args.get('lim'):
                res_lim = request.args.get('lim')
            if res_lim == "10":
                medical_history = medical_history[:10]
            return render_template('medicalHistory.html',
                                   history=medical_history,
                                   account=account,
                                   sort=sort,
                                   cat=category,
                                   lim=res_lim,
                                   token=token)
        else:
            return render_template('medicalHistory.html')
    else:
        # Give 401, forbidden access
        # return redirect('/login', 403)
        abort(401)


@app.route('/addMedicalHistory', methods=['GET', 'POST'])
def addMedicalHistory():
    if checkUserAuth():
        if request.method == 'GET':
            return render_template('addMedicalHistory.html')

        elif request.method == 'POST':
            history = {}
            if request.form['event_name_encrypted']:
                history['event_name'] = request.form['event_name_encrypted']
            if request.form['event_description_encrypted']:
                history['event_description'] = request.form['event_description_encrypted']
            if request.form['severity_encrypted']:
                history['severity'] = request.form['severity_encrypted']
            if request.form['date_encrypted']:
                history['date'] = request.form['date_encrypted']

            try:
                mongo.db.Users.update(
                    {"email": session['auth']},
                    {"$push": {
                        "history": history
                    }},
                )
            except IOError:
                return redirect(url_for('addMedicalHistory'), 500)

            return render_template('addMedicalHistory.html',
                                   info_msg="Item added sucesfully.")

        else:
            abort(401)
    else:
        abort(401)


@app.route('/addMedicalHistory/<historyType>', methods=['GET', 'POST'])
def addMedicalHistoryForm(historyType):
    history_types = [
        'DoctorVisit',
        'HospitalVisit',
        'Illness',
        'Prescription',
        'DentistVisit',
        'Other'
    ]
    if checkUserAuth():
        if historyType not in history_types:
            abort(404)
        if request.method == 'GET':
            return render_template(f"add{historyType}.html")

        elif request.method == 'POST':
            document = {}
            document['type'] = historyType

            # ADD _ID
            rand_token = '%030x' % random.randrange(16 ** 30)
            while mongo.db.Users.find({"_id": rand_token}).count() > 0:
                rand_token = '%030x' % random.randrange(16 ** 30)
            document['_id'] = rand_token
            
            for input_box in request.form:
                document[input_box] = request.form[input_box]
            updateUserAccount(session['auth'], {
                '$push': {
                    'history': document
                }
            })
            return redirect(url_for('medicalHistory'))

        else:
            abort(401)
    else:
        abort(401)


@app.route('/removeMedicalHisotryItem/<item_id>', methods=['GET'])
def removeMedicalHistoryItem(item_id):
    """GET: Removes the history item with the given _id
    """
    if checkUserAuth():
        email_address = session['auth']
        if not updateUserAccount(email_address, {
            "$pull": {
                "history": {
                    "_id": item_id
                }
            }
        }):
            flash("Error removing the item. Please try again.",
                  category="error")
            return redirect(url_for('medicalHistory'))
        flash("Item removed sucesfully.", category="info")
        return redirect(url_for('medicalHistory'))
    
    else:
        abort(401)


@app.route('/account', methods=['GET', 'POST'])
def account():
    if checkUserAuth():
        if request.method == 'POST':
            document = {"account": {}}
            for u_input in request.form:
                document['account'][u_input] = request.form[u_input]
            if not updateUserAccount(session['auth'], {
                "$set": document
            }):
                flash("Error updating account information. Please try again.",
                      category="error")
                return redirect(url_for('account'))
            flash("Account details updated sucessfully.",
                  category="info")
            return redirect(url_for('account'))
        else:
            document = getUserAccount(session['auth'])
            if not document.get('account'):
                document = None
            else:
                document = document['account']
            return render_template('account.html',
                                   account_details=document)

    else:
        abort(401)


@app.route('/logout', methods=['GET'])
def logout():
    """Logs user out, clearing the session."""
    if checkUserAuth():
        session.clear()
        flash("Sucessfully logged out.", category="info")
        return redirect(url_for('index'))
    else:
        abort(401)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')

    if request.method == 'POST':
        email_address = request.form.get('email_address')
        query = request.form.get('query')
        email.sendContactEmail(email_address, query)
        flash("Email sent sucessfully.", category="info")
        return redirect(url_for('contact'))


@app.errorhandler(401)
def unauthorisedRequest(error):
    return render_template('error/401.html'), 401


@app.errorhandler(404)
def fileNotFound(error):
    pass


@app.errorhandler(500)
def conflictingRequest(error):
    return render_template('error/500.html'), 500


def getUserAccount(email_address: str):
    """Finds and returns user account from DB
    @param email_address the target email address
    @return dict OR False
    """
    document = mongo.db.Users.find({"email": email_address})
    if document.count() == 0:
        return False
    elif document.count() > 1:
        return False
    else:
        return document[0]


def updateUserAccount(email_address: str, query: dict)->bool:
    """Updates user account by email address. \n
    @param email_address target email/account. \n
    @param query a dictionary with mongo query of items to update. \n
    @return boolean OR render_template()
    """
    try:
        mongo.db.Users.update({"email": email_address}, query)
    except IOError:
        return False
    finally:
        return True


def checkUserAuth() -> bool:
    """Checks if the user is authenticated already.
    """
    if session.get('auth'):
        # User is Authenticated
        document = getUserAccount(session.get('auth'))
        if datetime.utcnow() - timedelta(days=1) >= document['last_login']:
            return False
        return True
    elif not session.get('auth'):
        # User is not Authenticated
        return False


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=404)
