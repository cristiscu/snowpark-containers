# very simple job app

def to_fahrenheit(celsius):
    return celsius * 9./5 + 32

def hello():
	celsius = 20
	return f"Fahrenheit({celsius}): {to_fahrenheit(celsius)}"

print(hello())