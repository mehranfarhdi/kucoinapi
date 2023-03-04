
FROM python:3.8-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /project
COPY . /project
RUN pip install --upgrade pip
RUN pip install --upgrade cython
RUN pip install -r requirements.txt
CMD ["sh", "docker-entrypoint.sh"]