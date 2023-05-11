FROM python:3
MAINTAINER D. M. Vanin 'dmvanin@edu.hse.ru'

COPY ./ /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

CMD [ "./start.sh" ]

