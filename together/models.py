from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.restful import fields
from passlib.hash import bcrypt
from slugify import slugify

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime())
    confirmed_at = db.Column(db.DateTime())
    playlists = db.relationship('Playlist', backref='user', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def update_password(self, password):
        self.password = bcrypt.encrypt(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password)

    resource_fields = {
        'id': fields.Integer(),
        'name': fields.String()
    }


class PlaylistElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    youtube_id = db.Column(db.String(255))
    title = db.Column(db.String(255))
    thumbnail = db.Column(db.String(255))
    added_at = db.Column(db.DateTime())
    added_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    added_by = db.relationship('User')
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))

    resource_fields = {
        'id': fields.String(),
        'youtube_id': fields.String(),
        'title': fields.String(),
        'thumbnail': fields.String(),
        'added_at': fields.DateTime(),
        'added_by': fields.Nested(User.resource_fields)
    }


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_updated = db.Column(db.DateTime())
    elements = db.relationship('PlaylistElement', backref='playlist', lazy='dynamic')

    def update_slug(self):
        self.slug = slugify(self.name)

    resource_fields = {
        'id': fields.String(),
        'name': fields.String(),
        'slug': fields.String(),
        'user': fields.Nested(User.resource_fields),
        'elements': fields.List(fields.Nested(PlaylistElement.resource_fields)),
        'last_updated': fields.DateTime()
    }


login_manager.login_view = 'meta.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
