from bs4 import BeautifulSoup
import requests
import datetime
import calendar

MONTHS = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
}


def timus_to_epoch(time, date):
    hour, minute, second = [int(i) for i in time.split(':')]
    date = date.split(' ')
    day, month, year = int(date[0]), MONTHS[date[1]], int(date[2])

    t = datetime.datetime(year, month, day, hour, minute, second)
    return calendar.timegm(t.timetuple())


def html_to_epoch(date, time):
    hour, minute = [int(i) for i in time.split(':')]
    year, month, day = [int(i) for i in date.split('-')]

    t = datetime.datetime(year, month, day, hour, minute, 0)
    # на выходе должно получаться время по ЕКБ, а на вход идет время по МСК, поэтому +7200 секунд
    return calendar.timegm(t.timetuple()) + 7200


def get_tasks(user_id):
    request = requests.get(f'https://timus.online/status.aspx?author={user_id}&status=accepted&count=1000').text
    soup = BeautifulSoup(request, 'html.parser')

    tasks = soup.body.table.contents[2].td.table.contents[2:-1]
    return [(int(task.contents[3].a.contents[0]),
             timus_to_epoch(task.contents[1].contents[0].string, task.contents[1].contents[2].string)) for task in tasks]

# print(get_tasks(354143))


def get_users(template):
    request = requests.get(f'https://acm.timus.ru/search.aspx?Str={template}').text
    soup = BeautifulSoup(request, 'html.parser')

    users = [i.contents[2].a for i in soup.body.table.contents[2].td.table.tr.td.table.contents[1:]]
    return [(int(user.get('href')[user.get('href').rfind('=') + 1:]), user.string) for user in users]


# print(get_users('Δ'))


def get_task_info(task_id):
    request = requests.get(f'https://acm.timus.ru/problem.aspx?space=1&num={task_id}').text
    soup = BeautifulSoup(request, 'html.parser')

    algos = soup.body.table.contents[2].td.table.tr.td.contents[1].contents[1:-1:2]
    if algos == ['none \xa0']:
        algos = []
    else:
        algos = [i.string.rstrip(' ') for i in algos]

    difficulty = soup.body.table.contents[2].td.table.tr.td.contents[2].span.string
    difficulty = int(difficulty[difficulty.rfind(' ') + 1:])

    return difficulty, algos


# print(get_task_info(1242))
