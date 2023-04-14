from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Manga_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manga_name = db.Column(db.String(1000))
    manga_type = db.Column(db.String(150))
    manga_authors = db.Column(db.String(1000))
    manga_publish_date = db.Column(db.String(150))
    manga_rating = db.Column(db.String(150))
    manga_status = db.Column(db.String(150))
    manga_description = db.Column(db.String(10000))
    manga_image_id = db.Column(db.String(150))
    manga_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    upload_date = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    manga = db.relationship('Manga_info')
