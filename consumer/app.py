from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/",methods=["GET"])
def welcome():
    r = requests.get("http://localhost:8080/negotiate")
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True,port=3000)