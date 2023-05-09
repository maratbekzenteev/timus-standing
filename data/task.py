import sqlalchemy
import sqlalchemy.orm
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'task'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # a.k.a. timus' task number
    difficulty = sqlalchemy.Column(sqlalchemy.Integer)

    algo_tasks = sqlalchemy.orm.relationship('Algo_task', back_populates='task')
    user_tasks = sqlalchemy.orm.relationship('User_task', back_populates='task')
