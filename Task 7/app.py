from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/joke")
def get_joke():
    try:
        res = requests.get("https://official-joke-api.appspot.com/random_joke")
        data = res.json()
        joke = f"{data['setup']} 🤔 {data['punchline']}"
        return jsonify({"joke": joke})
    except:
        return jsonify({"joke": "Oops! Could not fetch a joke right now."})

if __name__ == "__main__":
    app.run(debug=True)
