FROM python:3.11
WORKDIR /app
COPY ./ /app/
RUN pip install flask
EXPOSE 9090
ENV FLASK_APP="main.py"
CMD ["flask", "run", "--host=0.0.0.0", "--port=9090"]