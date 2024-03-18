FROM python:3

WORKDIR /usr/src/backend
COPY Pipfile Pipfile.lock ./
RUN pip install -U pipenv
RUN pipenv install --system
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]