from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import func
from config import db, bcrypt


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship("Recipe", back_populates="user")

    serialize_rules = ("-recipes",)

    def __repr__(self):
        return f"<USER {self.id}: {self.username}>"

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Cant access password")

    @password_hash.setter
    def password_hash(self, new_password):
        # utf-8 encoding and decoding is required in python 3
        password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
        self._password_hash = password_hash

    def authenticate(self, password_to_check):
        return bcrypt.check_password_hash(self._password_hash, password_to_check)


class Recipe(db.Model, SerializerMixin):

    __tablename__ = "recipes"
    __table_args__ = (db.CheckConstraint("length(instructions) >= 50"),)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="recipes")

    def __repr__(self):
        return f'<Recipe {self.id}: instructions"{self.instructions}">'
