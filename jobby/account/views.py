from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from jobby.models import Users, Notification
from datetime import datetime
from jobby import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from utils import send_confirmation_email

account = Blueprint('account',__name__)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@account.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('manage.dashboard'))
            else:
                flash('Wrong Credentials! Check your spelling.')
                return render_template('account/login.html')
        else:
            flash('Wrong Credentials! Check your spelling.')
            return render_template('account/login.html')
    return render_template('account/login.html')

@account.route('/confirm_email/<token>')
def confirm_email(token):
    user = Users.verify_confirmation_token(token)
    if not user:
        abort(404)
    notif = Notification.query.filter_by(notification_to=current_user, not_type=2).first_or_404()
    db.session.delete(notif)
    user.email_approved = True
    db.session.commit()
    flash('Your email address has been confirmed!')
    return render_template('dashboard/dashboard.html')

@account.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    if request.method == 'POST':
        name = request.form['name'].capitalize()
        surname = request.form['surname'].capitalize()
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user is None:
            if email.startswith('demo'):
                user = Users(name=name, surname=surname, email=email,
                    password=hashed_password, member_since=datetime.utcnow(),
                    status='employer', email_approved=True)
                db.session.add(user)
                db.session.commit()
            else:
                user = Users(name=name, surname=surname, email=email,
                    password=hashed_password, member_since=datetime.utcnow(),
                    status='employer')
                notif = Notification(notification_to=user, not_type=2)
                db.session.add(user)
                db.session.add(notif)
                db.session.commit()
                #uncomment below code if you want to send confirmation email
                #send_confirmation_email(user)
            login_user(user)
            return render_template('account/welcome.html')
        flash('This email already being used!')
        return render_template('account/signup.html')

    return render_template('account/signup.html')

@account.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))
