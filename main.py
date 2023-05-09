from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import routines as r
import timus_parser as p
from data import db_session
from data.user import User
from data.user_task import User_task
from data.algo import Algo
from data.algo_task import Algo_task
from data.task import Task

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def standing_page():
    session = db_session.create_session()

    algos = session.query(Algo).all()
    algo_set = set([algo.name for algo in algos])
    req_user_tasks = session.query(User_task)

    if request.method == 'POST':
        min_diff = request.form['min_diff']
        max_diff = request.form['max_diff']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        req_algos = list(algo_set.intersection(set(request.form)))
        if len(req_algos) != 0:
            req_user_tasks = req_user_tasks.filter(User_task.task.has(Task.algo_tasks.any(Algo_task.algo.has(Algo.name.in_(req_algos)))))

        if min_diff != '':
            min_diff = int(min_diff)
            req_user_tasks = req_user_tasks.filter(User_task.task.has(Task.difficulty >= min_diff))

        if max_diff != '':
            max_diff = int(max_diff)
            req_user_tasks = req_user_tasks.filter(User_task.task.has(Task.difficulty <= max_diff))

        if start_time != '':
            start_time = p.html_to_epoch(*start_time.split('T'))
            req_user_tasks = req_user_tasks.filter(User_task.time >= start_time)

        if end_time != '':
            end_time = p.html_to_epoch(*end_time.split('T'))
            req_user_tasks = req_user_tasks.filter(User_task.time <= end_time)

    users = sorted([(req_user_tasks.filter(User_task.user_id == i.id).count(), i.name, i.id)
                    for i in session.query(User).all()], reverse=True)
    return render_template('standing.html', algos=algos, users=users)


@app.route('/users', methods=['GET', 'POST'])
def users_page():
    if request.method == 'POST' and request.form['template'] != '':
        template = request.form['template']
        r.add_users(template)

    session = db_session.create_session()
    users = session.query(User).all()

    return render_template('users.html', users=users)


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/delete_user/<int:user_id>')
def delete_user_page(user_id):
    r.delete_user(user_id)
    return redirect('/users')


@app.route('/update_all_user_tasks')
def update_all_user_tasks_page():
    r.update_all_user_tasks()
    return 'OK'


@app.route('/update_tasks')
def update_tasks_page():
    r.update_tasks()
    return 'OK'


if __name__ == '__main__':
    app.run()
