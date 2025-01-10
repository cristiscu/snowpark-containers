ARG BASE_IMAGE=python:3.10-slim-buster
FROM $BASE_IMAGE
COPY main.py ./
RUN pip install --upgrade pip && \
    pip install requests
CMD ["python3", "main.py"]

