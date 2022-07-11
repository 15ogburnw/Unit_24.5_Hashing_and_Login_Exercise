from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):

    db.app = app
    db.init_app(app)


class User(db.Model):

    @classmethod
    def register(cls, **kwargs):
        """
        Generate a hashed password and return a user instance containing the hashed password.
        """
        user = kwargs
        hashed = bcrypt.generate_password_hash(user['password'])
        hashed_utf8 = hashed.decode('utf8')
        user['password'] = hashed_utf8

        return cls(**user)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)


class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.Text, db.ForeignKey('users.username'))

    user = db.relationship('User', backref='feedback')
