# w/ storage volume (logs/log.txt)

from flask import Flask
app = Flask(__name__)

def to_fahrenheit(celsius):
    fahrenheit = int(celsius) * 9./5 + 32

    # could later use with a storage volume
    with open("logs/log.txt", "a") as f:
        f.write(f"{celsius}: {fahrenheit}\n")
    return fahrenheit

@app.get('/')
def hello():
    celsius = 20
    return f"Fahrenheit({celsius}): {to_fahrenheit(celsius)}"

@app.get('/history')
def dump():
    # dump call history from file
    with open("logs/log.txt", "r") as f:
        return f.read(f)

if __name__ == '__main__':
    app.run()