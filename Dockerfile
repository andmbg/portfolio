# syntax=docker/dockerfile:1

FROM python:3.12.3-bookworm

WORKDIR /app

COPY . .

# Initialize and update submodules
RUN git submodule update --init --recursive

COPY requirements.txt .
RUN pip3 install -r requirements.txt


CMD [ "python3", "-m" , "app"]

