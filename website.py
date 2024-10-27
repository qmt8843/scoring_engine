from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

app.config['DEBUG'] = True

@app.route("/")
def scoreboard():
    return render_template("index.html", data="Hello")
    #return "Hello", 200
    #return "<h1>Bad Request</h1>\nMissing sentence query, or issue with query data", 400 #BAD REQUEST

if __name__ == "__main__":
    # use 0.0.0.0 to use it in container
    app.run(host='0.0.0.0', port=8080)