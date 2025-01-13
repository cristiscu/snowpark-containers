# very simple Flask web app --> long-running service

from flask import Flask
app = Flask(__name__)

def to_fahrenheit(celsius):
    return celsius * 9./5 + 32

@app.route('/')
def hello():
	celsius = 20
	return f"Fahrenheit({celsius}): {to_fahrenheit(celsius)}"

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8000)