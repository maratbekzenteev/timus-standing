import sqlalchemy
import sqlalchemy.orm
from .db_session import SqlAlchemyBase


class Algo_task(SqlAlchemyBase):
    __tablename__ = 'algo_task'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('task.id'))
    algo_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('algo.id'))

    task = sqlalchemy.orm.relationship('Task', foreign_keys=[task_id])
    algo = sqlalchemy.orm.relationship('Algo', foreign_keys=[algo_id])
