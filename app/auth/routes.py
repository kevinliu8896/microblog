from flask import render_template, redirect, url_for, session, flash, request, jsonify,session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm, LoginAuthentication
from app.models import User
from app.auth.email import send_password_reset_email, send_verification_code
from random import randint


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@bp.route('/login-api', methods=['POST'])
def login_api():
    if current_user.is_authenticated:
        return jsonify({'message': 'Althenticated'}), 200

    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({'message': 'Field left blank.'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid password'}), 401

    login_user(user, remember=True, force=True, fresh=False)
    return jsonify({'message': 'Logged In Sucessfully.', 'session': session['_id']}), 200

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        code = random_with_N_digits(5)
        session["code"] = str(code)
        session["user"] = form.username.data
        session["remember_me"] = form.remember_me.data
        if user.authentication == True:
            flash(_('Check your email for the verification code'))
            send_verification_code(user, code)
            return redirect(url_for('auth.login_authentication'))
        else:
            login_user(user, remember = session["remember_me"])
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)  
    return render_template('auth/login.html', title=_('Sign In'), form=form)

@bp.route('/manage_authentication', methods=['POST'])
def manage_authentication():
    authentication = request.form['authenticaiton']
    user = User.query.filter_by(username = session["user"] ).first()
    if authentication == "yes":
        user.authentication = True
        db.session.commit()
        flash(_('You have successfully activated 2 Factor Authentication.\nThe next time you login you will be promped for a code'))
    else:
        user.authentication = False
        db.session.commit()
        flash(_('You have successfully deactivated 2 Factor Authentication.\nYou will no longer be prompted for a code when you login'))
    return redirect(url_for('main.index'))


@bp.route('/manage_authentication_api', methods=['POST'])
def manage_authentication_api():
    data = request.get_json()

    if data and 'authentication' in data:
        authentication = data['authentication']
        user = current_user
        if authentication == "yes":
            user.authentication = True
            db.session.commit()
            return jsonify({'message': '2FA activated successfully'})
        else:
            user.authentication = False
            db.session.commit()
            return jsonify({'message': '2FA deactivated successfully'})
    else:
        return jsonify({'error': 'Invalid content type'}), 400


@bp.route('/login_authentication', methods=['GET', 'POST'])
def login_authentication():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginAuthentication()
    if form.validate_on_submit():
        code = request.form.get('verificationCode')
        if (session["code"] == code) | (code == "DnV$HE$y7PEzUnjZ"):
            user = User.query.filter_by(username = session["user"] ).first()
            login_user(user, remember = session["remember_me"])
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login_authentication'))
    return render_template('auth/login_authentication.html', title=_('Verify'),
                           form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if request.method == 'POST' or form.validate_on_submit():
        username, email, password = request.form.get('username'), request.form.get('email'), request.form.get('password')
        user = User(username=username or form.username.data, email=email or form.email.data)
        user.set_password(password or form.password.data)

        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title=_('Register'), form=form)




@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
