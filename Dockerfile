FROM python:3.8-slim-buster
ENV TZ Europe/Minsk

WORKDIR /
COPY ./ ./

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r ./requirements.txt
Run pip install aiogram-calendar

CMD python ./booking4barbershop.py ./booking4barbershop.py