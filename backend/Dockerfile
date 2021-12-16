FROM python:3

WORKDIR /app/backend

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["flask", "run"]
