from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
POSTS_FILE = "posts.json"

def load_posts():
    '''Loads posts from posts.json'''
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    '''Saves posts to posts.json'''
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

def fetch_post_by_id(post_id):
    '''Fetches post by id'''
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return None
@app.route('/')
def index():
    '''Render index page'''
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handles the addition of a new blog post.

    On GET request:
        - Renders the form for creating a new blog post.

    On POST request:
        - Retrieves form data.
        - Adds the new post to the data store.
        - Redirects the user back to the index page.
    """
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
    '''Handles deletion of a blog post.'''
    posts = load_posts()
    posts = [post for post in posts if post["id"] != post_id]
    save_posts(posts)
    return redirect(url_for("index"))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    '''Handles updating of a blog post.'''
        posts = load_posts()
        post = next((p for p in posts if p["id"] == post_id), None)

        if post is None:
            return "Post not found", 404

        if request.method == 'POST':
            post["author"] = request.form.get("author")
            post["title"] = request.form.get("title")
            post["content"] = request.form.get("content")

            save_posts(posts)

            return redirect(url_for('index'))

        return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    """
    Increments the like count for the blog post with the given post_id.

    Retrieves the post by ID, increases its like counter by one,
    updates the data store, and redirects back to the index page.
    """
    posts = load_posts()

    for post in posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break

    save_posts(posts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)