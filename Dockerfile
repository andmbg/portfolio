# syntax=docker/dockerfile:1

FROM python:3.12.3-bookworm

WORKDIR /app

COPY . .

# Initialize and update submodules
RUN git submodule update --init --recursive

WORKDIR /app/dashapps/elternsein
RUN git checkout troubleshoot
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 8080
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD [ "python3", "-m" , "app"]

