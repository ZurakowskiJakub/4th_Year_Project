from app import app

from itsdangerous import URLSafeTimedSerializer


def generateToken(email_address: str):
    """Generates a confirmation token, based on the user's email address.\n
    @param email_address the email address of the user\n
    @return str the token.
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email_address,
                            salt=app.config['SECURITY_PASSWORD_SALT'])


def confirmToken(token: str, expiration=3600):
    """Confirmes the token given.
    @param token the token to confirm.
    @param exiration=3600 the expiration duration for the token.
    @returns bool OR email_address of the confirming user.
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email_address = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except Exception:
        return False
    return email_address
