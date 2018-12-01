FROM python:3.6
RUN apt update && apt install build-essential

COPY requirements.txt /
RUN pip install -r /requirements.txt
WORKDIR /app
COPY . .

EXPOSE 80
RUN export FLASK_ENV=development
CMD ["python", "server.py"]
