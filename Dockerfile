FROM python:3.10
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ARG CORE_PORT
EXPOSE ${CORE_PORT}
COPY . /code/
ENV PYTHONPATH=/code
CMD ["sh", "-c", "alembic upgrade head && python -u main.py"]