FROM python:3.10-slim-buster
COPY main.py ./
RUN pip install snowflake-snowpark-python[pandas]
CMD ["python3", "main.py"]