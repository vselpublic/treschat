from flask import g, jsonify,request, current_app
from flask.ext.httpauth import HTTPBasicAuth
from ..dao import User, Anonymous
from . import api
from errors import forbidden, unauthorized

authenticate = HTTPBasicAuth()

@authenticate.verify_password
def verify_password(email_or_token, password):
    #current_app.logger.error('An error occurred')
    if email_or_token == '':
        g.current_user = Anonymous()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return True
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@api.before_request
@authenticate.login_required
def before_request():
    if g.current_user.is_anonymous():
        return forbidden('Unconfirmed account')

@authenticate.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.route('/token')
def get_token():
    if g.current_user.is_anonymous() or g.token_used:
        return forbidden('Unconfirmed account')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=360000), 'expiration': 360000})
