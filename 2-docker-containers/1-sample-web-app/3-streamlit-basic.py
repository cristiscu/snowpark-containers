# very simple Streamlit app

import streamlit as st

def to_fahrenheit(celsius):
    return celsius * 9./5 + 32

def hello():
	celsius = 20
	return f"Fahrenheit({celsius}): {to_fahrenheit(celsius)}"

if __name__ == '__main__':
	st.write(hello())
    #print(hello())