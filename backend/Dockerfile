FROM python:3.8-slim

WORKDIR /app/backend

COPY Pipfile Pipfile.lock ./

# RUN pip install pipenv && \
#     apt-get update && \
#     apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
#     pipenv install --deploy --system && \
#     apt-get remove -y gcc python3-dev libssl-dev && \
#     apt-get autoremove -y && \
#     pip uninstall pipenv -y

RUN pip install pipenv && pipenv install --deploy --system

COPY . .

ENV FLASK_ENV=development

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
