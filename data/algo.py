import sqlalchemy
import sqlalchemy.orm
from .db_session import SqlAlchemyBase


class Algo(SqlAlchemyBase):
    __tablename__ = 'algo'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    algo_tasks = sqlalchemy.orm.relationship('Algo_task', back_populates='algo')
