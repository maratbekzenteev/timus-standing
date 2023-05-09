import timus_parser as p
import sqlalchemy as sa
from data import db_session
from data.user import User
from data.user_task import User_task
from data.algo import Algo
from data.algo_task import Algo_task
from data.task import Task

db_session.global_init('db/standing.db')


def add_task(task_id):
    difficulty, algos = p.get_task_info(task_id)

    session = db_session.create_session()

    new_task = Task(id=task_id, difficulty=difficulty)
    session.add(new_task)
    session.commit()

    for algo in algos:
        same_algo = session.query(Algo).filter(Algo.name == algo).all()

        if len(same_algo) == 0:
            new_algo = Algo(name=algo)
            session.add(new_algo)
            session.commit()

        algo_id = session.query(Algo).filter(Algo.name == algo).first().id
        new_algo_task = Algo_task(task_id=task_id, algo_id=algo_id)
        session.add(new_algo_task)
        session.commit()


# add_task(1242)


def add_users(template):
    users = p.get_users(template)

    session = db_session.create_session()

    for id, name in users:
        same_name = session.query(User).filter(User.name == name).all()

        if len(same_name) == 0:
            new_user = User(id=id, name=name)
            session.add(new_user)
            session.commit()


# add_users('Δ')


def update_tasks():
    session = db_session.create_session()

    tasks = session.query(Task).all()
    for task in tasks:
        difficulty, algos = p.get_task_info(task.id)

        session.execute(sa.update(Task).where(Task.id == task.id).values(difficulty=difficulty))
        session.commit()


# update_tasks()


def delete_user(user_id):
    session = db_session.create_session()
    session.query(User).filter(User.id == user_id).delete()
    session.query(User_task).filter(User_task.user_id == user_id).delete()
    session.commit()


# delete_user(70735)


def update_user_tasks(user_id):
    tasks = p.get_tasks(user_id)

    session = db_session.create_session()

    for task_id, time in tasks:
        same_user_task = session.query(User_task).filter(User_task.user_id == user_id,
                                                         User_task.task_id == task_id)
        if same_user_task.filter(User_task.time == time).count() != 0:
            break
        if same_user_task.count() != 0:
            continue

        same_task = session.query(Task).filter(Task.id == task_id).all()
        if len(same_task) == 0:
            add_task(task_id)

        new_user_task = User_task(task_id=task_id, user_id=user_id, time=time)
        session.add(new_user_task)
        session.commit()

    session.commit()


# update_user_tasks(353091)


def update_all_user_tasks():
    session = db_session.create_session()

    users = session.query(User).all()
    for user in users:
        update_user_tasks(user.id)
