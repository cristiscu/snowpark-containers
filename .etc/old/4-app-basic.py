# very simple Flask web app (REST API!)

from flask import Flask
app = Flask(__name__)

def to_fahrenheit(celsius):
    return celsius * 9./5 + 32

@app.route('/hello/<int:celsius>')
def hello(celsius):
	return f"Fahrenheit({celsius}): {to_fahrenheit(celsius)}"

if __name__ == '__main__':
	app.run()