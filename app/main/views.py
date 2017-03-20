# coding=utf-8
from flask import abort
from flask import current_app
from flask import render_template,redirect, url_for,make_response
from flask import request
from flask_login import current_user, login_required

from app import db
from . import main
from app.main.forms import PostForm, CommentForm
from app.models import Post, User, Comment


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', title=u'我的博客',form=form,posts=posts,pagination=pagination)



@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return username


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    pass


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
def edit_profile_admin(id):

    return 'edit_profile_admin'



@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment=form.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    print str(page)
    if page == -1:
        page = 1
            # (post.comments.count() - 1) // current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', post=post, form=form, comments=comments,pagination=pagination)

@main.route('/comment/<int:id>', methods=['GET', 'POST'])
def comment(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment = form.comment.data,
                          author=current_user._get_current_object(),
                          post=post)
        db.session.add(comment)
        return redirect(url_for('.post',post=post,form=form))
    comments = Comment.query.all()
    return render_template('post.html',post=post,form=form,comments = comments)



    return '评论列表'



@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        return redirect(url_for('.index', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    post = Post.query.filter_by(id=id).first_or_404()
    db.session.delete(post)
    return redirect(url_for('.index'))





















