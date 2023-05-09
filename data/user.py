import sqlalchemy
import sqlalchemy.orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # a.k.a. timus id (not judge id)
    name = sqlalchemy.Column(sqlalchemy.String)

    user_tasks = sqlalchemy.orm.relationship('User_task', back_populates='user')
