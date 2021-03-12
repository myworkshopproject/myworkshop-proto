ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}
RUN apt-get update && apt-get -y dist-upgrade
RUN apt install -y netcat
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY Makefile Makefile
RUN make venv
COPY requirements.in requirements.in
RUN make install
COPY . .
