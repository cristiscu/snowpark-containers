FROM python:3.10-slim-buster
COPY main.py ./
COPY templates/ ./templates/
COPY logs/ ./logs/
RUN pip install flask && \
    pip install requests
CMD ["python3", "main.py"]