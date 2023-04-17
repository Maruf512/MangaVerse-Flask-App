from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import os
import shutil
from .models import Manga_info, Manga_chapters
from . import db
from . import admin_authorization

views = Blueprint("views", __name__, static_url_path='/static')


@views.route('/')
@login_required
def home():
    # give access to admin
    admin = admin_authorization.get_access(current_user.email)

    data = Manga_info.query.all()

    return render_template("home.html", user=current_user, admin=admin, data=data)


@views.route('/view')
def view():
    # give access to admin
    admin = admin_authorization.get_access(current_user.email)

    return render_template("view_page.html", admin=admin, user=current_user)

# ===================================================================
# ========================== Manga details ==========================
# ===================================================================


@views.route('manga/<manga_id>')
def details(manga_id):
    # give access to admin
    admin = admin_authorization.get_access(current_user.email)

    data = Manga_info.query.filter_by(id=manga_id).first()

    return render_template("details.html", admin=admin, user=current_user, data=data)


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
# ============================ Add Manga  ===========================
# ===================================================================


@views.route('/add-manga', methods=['GET', 'POST'])
def add_manga():

    # =================== add chapter ========================
    # new_chapter = Manga_chapters(
    #     manga_name="solo leveling", chapter_name="chapter 2", manga_id=manga_id)
    # db.session.add(new_chapter)
    # db.session.commit()

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
        manga_rating = str(manga_rating)

        if manga_name and manga_image and manga_type and manga_authors and manga_published and manga_rating and manga_status and manga_discription != "":
            # send to db
            new_manga = Manga_info(manga_name=manga_name,
                                   manga_type=manga_type,
                                   manga_authors=manga_authors,
                                   manga_publish_date=manga_published,
                                   manga_rating=manga_rating,
                                   manga_status=manga_status,
                                   manga_description=manga_discription,
                                   manga_image_id=manga_image,
                                   )
            db.session.add(new_manga)
            db.session.commit()
            flash("added to database!", category='success')
            return redirect(url_for('.home'))
        else:
            flash("Empty Field!", category='error')

    return render_template("add_manga.html", user=current_user, manga_img=img)

# ===================================================================
# ============================ Delet Manga ===========================
# ===================================================================


@views.route('delete/<manga_id>')
def delete_manga(manga_id):

    data = Manga_info.query.filter_by(id=manga_id).first()
    delete_manga_img = f"{os.getcwd()}/website/static/files/Cover_img/{data.manga_image_id}"
    os.remove(delete_manga_img)

    delet_manga = Manga_info.query.get_or_404(manga_id)
    db.session.delete(delet_manga)
    db.session.commit()

    flash(f"Erased from database!!", category="success")
    return redirect(url_for('.home'))


# ===================================================================
# ============================ Edit Manga ===========================
# ===================================================================


@views.route('edit/<manga_id>', methods=['GET', 'POST'])
def edit_manga(manga_id):
    data = Manga_info.query.filter_by(id=manga_id).first()

    if request.method == 'POST':
        # get value from webpage
        # manga_image = img
        manga_name = request.form.get('name')
        manga_type = request.form.get('type')
        manga_authors = request.form.get('authors')
        manga_published = request.form.get('published')
        manga_rating = request.form.get('ratings')
        manga_status = request.form.get('status')
        manga_discription = request.form.get('discription')
        # save data on a database
        manga_rating = str(manga_rating)

        if manga_name != "":
            data.manga_name = manga_name
        if manga_type != "":
            data.manga_type = manga_type

        if manga_authors != "":
            data.manga_authors = manga_authors
        if manga_published != "":
            data.manga_publish_date = manga_published
        if manga_rating != "":
            data.manga_rating = manga_rating
        if manga_status != "":
            data.manga_status = manga_status
        if manga_discription != "":
            data.manga_description = manga_discription

        db.session.commit()

        return redirect(url_for('.home'))

    return render_template('add_manga.html', user=current_user, manga_img=data.manga_image_id)


# ===================================================================
# ============================ View Manga ===========================
# ===================================================================


@views.route('/next_page')
def next_page():
    return view()


@views.route('/previous_page')
def previous_page():
    return view()
