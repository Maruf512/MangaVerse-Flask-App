from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__, static_url_path='/static')


@auth.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if "@gmail.com" not in email:
            flash("Invalid Email Adress!!", category="error")
        elif password1 != password2:
            flash("First name must be greater then 1 characters.", category="error")
        elif len(password1) < 7:
            flash("Password didn't match.", category="error")
        elif len(firstName) < 2:
            flash("Password must be at least 7 characters.", category="error")
        else:
            # add user to database
            flash("Account Created!", category="success")

    return render_template("sign_up.html")
