import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .bd_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'
    user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.Text)
    first_name = sqlalchemy.Column(sqlalchemy.Text)
    second_name = sqlalchemy.Column(sqlalchemy.Text)
    email = sqlalchemy.Column(sqlalchemy.Text)
    password = sqlalchemy.Column(sqlalchemy.Text)
    user_type = sqlalchemy.Column(sqlalchemy.Text)