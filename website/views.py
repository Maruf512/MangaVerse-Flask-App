from flask import Blueprint, render_template, request

views = Blueprint("views", __name__, static_url_path='/static')


@views.route('/')
def home():
    return render_template("home.html", Name="The 100 Girlfriends who really really love you", Details="anime details")


@views.route('/view')
def view():
    return render_template("view_page.html")


@views.route('/next_page')
def next_page():

    return view()


@views.route('/previous_page')
def previous_page():
    return view()
