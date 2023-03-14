FROM --platform=linux/amd64 python:alpine
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
CMD [ "python", "manage.py", "runserver" ,"0.0.0.0:8000" ]
