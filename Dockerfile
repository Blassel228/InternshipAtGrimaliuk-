FROM python:3
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade -r /code/requirements.txt
COPY . /code
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]