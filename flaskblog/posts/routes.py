from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment , React
from flaskblog.posts.forms import PostForm, CommentForm, ReactForm, DisReactForm
from flaskblog.users.utils import save_post_picture

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            image_file = picture_file
            post = Post(title=form.title.data, content=form.content.data, author=current_user,post_file=image_file)
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    form2 = ReactForm()
    form3 = DisReactForm()
    reactis = React.query.filter_by(author3=current_user , author4=post).all()
    reactis2 = React.query.filter_by(author3=current_user , author4=post).first()
    postreactis = React.query.filter_by(author4=post).all()
    print(reactis2)
    comments = Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.date_comment.desc()).all()
    if form.submit1.data and form.validate():
        pos = Comment(comment_content=form.comment.data, author1=current_user,author2=post)
        db.session.add(pos)
        db.session.commit()
        flash('Thank you for the comment', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    if form2.submit2.data:
        rct = React(author3=current_user, author4=post)
        db.session.add(rct)
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post_id))
    if form3.submit3.data:
        db.session.delete(reactis2)
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post_id))

    return render_template('post.html', title=post.title, post=post,form=form,commentsno=len(comments),comments=comments,form3=form3, form2=form2,postreactis =len(postreactis),reactis=len(reactis))

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
