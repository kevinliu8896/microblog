from flask import render_template, redirect, url_for, session, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm, LoginAuthentication
from app.models import User
from app.auth.email import send_password_reset_email, send_verification_code


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
        if user.authentication == True:
            code = "1234"
            session["code"] = code 
            session["user"] = form.username.data
            session["remember_me"] = form.remember_me.data
            flash(_('Check your email for the verification code'))
            send_verification_code(user, code)
            return redirect(url_for('auth.login_authentication'))
        login_user(user, remember = session["remember_me"])
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)  
    return render_template('auth/login.html', title=_('Sign In'), form=form)

@bp.route('/manage_authentication', methods=['POST'])
def manage_authentication():
    authentication = request.form['authenticate']
    user = User.query.filter_by(username = session["user"] ).first()
    if authentication == True:
        user.authentication = True
    else:
        user.authentication = False
    return redirect(url_for('main.index'))


@bp.route('/login_authentication', methods=['GET', 'POST'])
def login_authentication():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginAuthentication()
    if form.validate_on_submit():
        code = request.form.get('verificationCode')
        message = "Current Verification Code: " + str(code)
        flash(message)
        if session["code"] != code:
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login_authentication'))
        user = User.query.filter_by(username = session["user"] ).first()
        login_user(user, remember = session["remember_me"])
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)    
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
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'),
                           form=form)


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
