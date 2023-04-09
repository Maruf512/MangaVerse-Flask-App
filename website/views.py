from flask import Blueprint, render_template, request

views = Blueprint("views", __name__, static_url_path='/static')


@views.route('/')
def home():
    return render_template("base.html")


@views.route('/view', methods=['GET', 'POST'])
def view():
    return render_template("view_page.html")


@views.route('/next_page')
def next_page():
    print("next")
    return view()


@views.route('/previous_page')
def previous_page():
    print("Back")
    return view()
