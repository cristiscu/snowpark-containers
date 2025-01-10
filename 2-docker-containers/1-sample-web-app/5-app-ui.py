# added I/O data through UI (templates/basic_ui.html)

from flask import Flask, request, render_template
app = Flask(__name__)

def to_fahrenheit(celsius):
    return int(celsius) * 9./5 + 32

@app.route("/ui", methods=["GET", "POST"])
def ui():
    if request.method != "POST":
        return render_template("basic_ui.html")
    
    celsius = request.form.get("input")
    return render_template("basic_ui.html",
        celsius=celsius,
        fahrenheit=to_fahrenheit(celsius))

if __name__ == '__main__':
    app.run()