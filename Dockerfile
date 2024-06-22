FROM python:3.10
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ARG CORE_PORT
EXPOSE ${CORE_PORT}
COPY . .
CMD python -u main.py