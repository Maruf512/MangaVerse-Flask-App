from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import os
import shutil

views = Blueprint("views", __name__, static_url_path='/static')


names = ["Solo Leveling", "Demon Slayer", "Attack on Titan", "Vinland Saga", "Violet Evergarden", "The time i got reincarnated as a slime", "Konosuba",
         "Darling in the Franxx", "Your lie in April", "Your Name", "Hunter x Hunter", "My Hero academia", "One Piece", "The 100 Girlftiends who really really love you"]

image_link = ["solo_leveling.jpg", "demon_slayer.jpg", "attack_on_titan.jpg", "vinland_saga.jpg", "violet_evergarden.jpg", "the_time_i_got_reincarnated_as_a_slime.jpg", "konosuba.jpg",
              "darling_in_the_franxx.jpg", "your_lie_in_april.jpg", "your_name.jpg", "hunter_x_hunter.jpg", "my_hero_academia.jpg", "one_piece.jpg", "The 100 Girlfriends who.jpg"]


@views.route('/')
@login_required
def home():
    if current_user.email == "marufsarkar512@gmail.com":
        admin = True
    else:
        admin = False

    return render_template("home.html", user=current_user, admin=admin, names_len=len(names), Name=names, images=image_link, Details="anime details")


@views.route('/view')
def view():
    if current_user.email == "marufsarkar512@gmail.com":
        admin = True
    else:
        admin = False

    return render_template("view_page.html", admin=admin, user=current_user)


@views.route('manga/<manga_id>')
def details(manga_id):
    if current_user.email == "marufsarkar512@gmail.com":
        admin = True
    else:
        admin = False

    return render_template("details.html", admin=admin, user=current_user, manga_img=manga_id)


# ===================================================================
# ========================= Load Manga Image ========================
# ===================================================================

@views.route('/load-manga-image', methods=['GET', 'POST'])
def load_manga_image():
    if request.method == 'POST':
        uploaded_file = request.files['cover_img']
        if uploaded_file.filename != '':
            global img
            img = uploaded_file.filename
            uploaded_file.save(img)
            new_path = "D:\Pton\Flask Web App\website\static\\files\Cover_img\\" + img
            old_path = "D:\Pton\Flask Web App\\" + img
            shutil.move(old_path, new_path)

            return redirect(url_for('.add_manga'))

    return render_template("load_manga_image.html", user=current_user)

# ===================================================================
# ========================= Load Manga Image ========================
# ===================================================================


@views.route('/add-manga', methods=['GET', 'POST'])
def add_manga():
    if request.method == 'POST':
        # get value from webpage
        manga_image = img
        manga_name = request.form.get('name')
        manga_type = request.form.get('type')
        manga_authors = request.form.get('authors')
        manga_published = request.form.get('published')
        manga_rating = request.form.get('ratings')
        manga_status = request.form.get('status')
        manga_discription = request.form.get('discription')
        # save data on a database

        print(manga_image)
        print(manga_name)
        print(manga_type)
        print(manga_authors)
        print(manga_published)
        print(manga_rating)
        print(manga_status)
        print(manga_discription)

    return render_template("add_manga.html", user=current_user, manga_img=img)

# ===================================================================
# ============================ View Manga ===========================
# ===================================================================


@views.route('/next_page')
def next_page():
    return view()


@views.route('/previous_page')
def previous_page():
    return view()
