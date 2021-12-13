FROM python:3

WORKDIR /app/backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=development

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
