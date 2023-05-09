import sqlalchemy
import sqlalchemy.orm
from .db_session import SqlAlchemyBase


class User_task(SqlAlchemyBase):
    __tablename__ = 'user_task'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'))
    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('task.id'))
    time = sqlalchemy.Column(sqlalchemy.Integer)

    user = sqlalchemy.orm.relationship('User', foreign_keys=[user_id])
    task = sqlalchemy.orm.relationship('Task', foreign_keys=[task_id])
