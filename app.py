from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
POSTS_FILE = "posts.json"

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)
@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]

        posts = load_posts()

        new_id = max([p["id"] for p in posts], default=0) + 1

        new_post = {
            "id": new_id,
            "title": title,
            "author": author,
            "content": content
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for("index"))
    return render_template('add.html')

@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post["id"] != post_id]
    save_posts(posts)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)