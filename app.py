import json
from flask import Flask, render_template

app = Flask(__name__)

with open("posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)
@app.route('/')
def index():
    return render_template('index.html', posts=posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)