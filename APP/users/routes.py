from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from APP.users.forms import (RegistrationForm, LoginForm,
     UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from APP.models import User
from APP import db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from flask_mail import Message

users = Blueprint('users', __name__)

@users.route('/users/registration', methods=['GET', 'POST'])
def registration():
    #Check for authentication#
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():

        #add user to database#
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f"Your account has been created. You are now able to login!", "success")
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title="Register", form=form)

@users.route('/users/login', methods=['GET', 'POST'])
def login():
    #Check for authentication#
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():

        #check to see if login is correct#
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Login successful", 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('login Unsuccessful. Please check email and password', 'danger')

    return render_template('users/login.html', title='Login', form=form)

@users.route('/users/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

def save_picture(form_picture):

    #Rename image#
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pics', picture_fn)

    #Resize image#
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    #Save Picture#
    i.save(picture_path)
    return picture_fn

@users.route('/users/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.picture.data = current_user.image_file
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('users/account.html', title='Account', image_file=image_file, form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Passsword Reset Request',
        sender='Hodges.Showcase@gmail.com',
        recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then ingore this email and no changes will be made.
'''
    mail.send(msg)

@users.route('/users/reset_password', methods=['GET', 'POST'])
def reset_request():
    #Check for authentication#
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset Password', form=form)

@users.route('/users/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
     #Check for authentication#
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():

        #add user to database#
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        flash(f"Your password has been updated. You are now able to login!", "success")
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset Password', form=form)