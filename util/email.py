import app as main

import email
import smtplib

from flask import url_for


def sendVerificationEmail(recipient: str, token: str) -> bool:
    """Sends an email using the smtp connection
    Returns true if sent, false if failed.
    """
    PASSWORD = main.app.config['EMAIL_PASSWORD']
    FROM = main.app.config['EMAIL_USERNAME']
    TO = recipient

    msg = email.message_from_string(f"""
    You have sucesfully registered with MediSec.
    Please click the link below to verify your email.
    You won't be able to log-in unless you do this.
    http://{app.config['EXTERNAL_HOST']}{url_for('validateEmail', user_token=token)}
    """)
    msg['Subject'] = "MediSec"
    msg['From'] = FROM
    msg['To'] = TO

    try:
        s = smtplib.SMTP("smtp.live.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(FROM, PASSWORD)

        s.sendmail(FROM, TO, msg.as_string())
    except Exception as e:
        print(e)
        return False
    finally:
        s.quit()
    return True


def sendContactEmail(sender: str, message: str) -> bool:
    """Sends an email using the smtp connection
    Returns true if sent, false if failed.
    """
    PASSWORD = main.app.config['EMAIL_PASSWORD']
    FROM = main.app.config['EMAIL_USERNAME']
    TO = "C00205431@itCarlow.ie"

    msg = email.message_from_string(f"""
    Sender: {sender}
    Message: {message}
    """)
    msg['Subject'] = "MediSec Query"
    msg['From'] = FROM
    msg['To'] = TO

    try:
        s = smtplib.SMTP("smtp.live.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(FROM, PASSWORD)

        s.sendmail(FROM, TO, msg.as_string())
    except Exception as e:
        print(e)
        return False
    finally:
        s.quit()
    return True
