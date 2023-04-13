from flask import Blueprint, render_template, request
from flask_login import login_required, current_user


views = Blueprint("views", __name__, static_url_path='/static')

names = ["Solo Leveling", "Demon Slayer", "Attack on Titan", "Vinland Saga", "Violet Evergarden", "The time i got reincarnated as a slime", "Konosuba",
         "Darling in the Franxx", "Your lie in April", "Your Name", "Hunter x Hunter", "My Hero academia", "One Piece", "The 100 Girlftiends who really really love you"]

image_link = ["solo_leveling.jpg", "demon_slayer.jpg", "attack_on_titan.jpg", "vinland_saga.jpg", "violet_evergarden.jpg", "the_time_i_got_reincarnated_as_a_slime.jpg", "konosuba.jpg",
              "darling_in_the_franxx.jpg", "your_lie_in_april.jpg", "your_name.jpg", "hunter_x_hunter.jpg", "my_hero_academia.jpg", "one_piece.jpg", "The 100 Girlfriends who.jpg"]


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user, names_len=len(names), Name=names, images=image_link, Details="anime details")


@views.route('/view')
def view():
    return render_template("view_page.html", user=current_user)


@views.route('manga/<manga_id>')
def details(manga_id):
    return render_template("details.html", user=current_user, manga_img=manga_id)


@views.route('add-manga')
def add_manga():
    return render_template("add_manga.html", user=current_user)


@views.route('/next_page')
def next_page():
    return view()


@views.route('/previous_page')
def previous_page():
    return view()
