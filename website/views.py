from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import os
import shutil
from .models import Manga_info
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
    if request.method == 'POST':
        # get value from webpage
        manga_image1 = img
        manga_name1 = request.form.get('name')
        manga_type1 = request.form.get('type')
        manga_authors1 = request.form.get('authors')
        manga_published1 = request.form.get('published')
        manga_rating1 = request.form.get('ratings')
        manga_status1 = request.form.get('status')
        manga_discription1 = request.form.get('discription')
        # save data on a database
        manga_rating1 = str(manga_rating1)
        print(type(manga_status1))
        if manga_name1 and manga_image1 and manga_type1 and manga_authors1 and manga_published1 and manga_rating1 and manga_status1 and manga_discription1 != "":
            # send to db
            new_manga = Manga_info(manga_name=manga_name1,
                                   manga_type=manga_type1,
                                   manga_authors=manga_authors1,
                                   manga_publish_date=manga_published1,
                                   manga_rating=manga_rating1,
                                   manga_status=manga_status1,
                                   manga_description=manga_discription1,
                                   manga_image_id=manga_image1,
                                   )
            db.session.add(new_manga)
            db.session.commit()
            flash("added to database!", category='success')
        else:
            flash("Empty Field!", category='error')

    return render_template("add_manga.html", user=current_user, manga_img=img)

# ===================================================================
# ============================ Delet Manga ===========================
# ===================================================================


@views.route('delete/<manga_id>')
def delete_manga(manga_id):
    delet_manga = Manga_info.query.get_or_404(manga_id)
    db.session.delete(delet_manga)
    db.session.commit()
    flash(f"Erased from database!!", category="success")
    return redirect(url_for('.home'))


# ===================================================================
# ============================ Edit Manga ===========================
# ===================================================================


@views.route('edit/<manga_id>')
def edit_manga(manga_id):
    return redirect(url_for('.home'))


# ===================================================================
# ============================ View Manga ===========================
# ===================================================================


@views.route('/next_page')
def next_page():
    return view()


@views.route('/previous_page')
def previous_page():
    return view()
