ARG BASE_IMAGE=python:3.10-slim-buster
FROM $BASE_IMAGE
COPY main.py ./
COPY templates/ ./templates/
RUN pip install --upgrade pip && pip install flask snowflake-snowpark-python
CMD ["python", "main.py"]

