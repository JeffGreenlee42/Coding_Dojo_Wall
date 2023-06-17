from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.model_post import Post
from datetime import datetime

@app.route("/wall")
def wall():
    if 'user_id' not in session:
        return redirect("/logout")
    comments = []
    posts = Post.get_all()
    for post in posts:
        date = post['created_at'].strftime("%B %d")
        comment = {
            'post_id': post['id'],
            'users_id': post['users_id'],
            'first_name': post['first_name'],
            'date': date,
            'content': post['content']
            }
        # date = post['created_at']
        comments.append(comment)
    return render_template("wall.html", comments = comments)

@app.route("/comment", methods=['POST'])
def comment():
    # print(f"entering controller_posts comment method: data is {data}")
    isValid = Post.validate_post(request.form['comment'])
    if not isValid:
       return redirect("/wall")
    result = Post.create_post(request.form)
    return redirect("/wall")


@app.route("/delete_post", methods=['POST'])
def delete_post():
    # print(f"pos_id is: {request.form['post_id']}")
    print(f"request.form is: {request.form}")
    result = Post.delete_post(request.form)
    return redirect("/wall")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
