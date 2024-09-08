from flask import Flask

app = Flask(__name__)

@app.route("/")
def start_page():
    return "<h1>Hello, World!</h1><a href='https://www.google.de/' >Google</a>"

if __name__ == "__main__":
    app.run(debug=True)