from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__, static_url_path='/static')


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # get a query by an id(i am using email id in hear to find the query)
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                # print(user.email)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # check if user exists or not
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif "@gmail.com" not in email:
            flash("Invalid Email Adress!!", category="error")
        elif password1 != password2:
            flash("First name must be greater then 1 characters.", category="error")
        elif len(password1) < 7:
            flash("Password didn't match.", category="error")
        elif len(firstName) < 2:
            flash("Password must be at least 7 characters.", category="error")
        else:
            # add user to database
            new_user = User(email=email, first_name=firstName,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account Created!", category="success")

            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
