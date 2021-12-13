FROM python:3

WORKDIR /usr/backend

ENV FLASK_ENV=development

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
