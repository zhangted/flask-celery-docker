FROM python:3.9

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements.testing.txt /code/
RUN pip install --no-cache-dir -r requirements.testing.txt

COPY . /code/