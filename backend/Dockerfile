FROM --platform=linux/amd64 python:alpine3.13
RUN apk add --update busybox-suid
RUN addgroup app && adduser -S -G app app
USER app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000

ENV PATH="/home/app/.local/bin:${PATH}"

# This will run collectstatic only if path doesn't exists. Otherwise, it will do nothing.
RUN test ! -d /code/staticfiles || true && python manage.py collectstatic

# CMD [ "python", "manage.py", "runserver" ,"0.0.0.0:8000" ]
