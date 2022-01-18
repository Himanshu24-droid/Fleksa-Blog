import os
from flask import(
    Blueprint,url_for,render_template,flash,redirect,request,current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flask_login import login_required, current_user
from .extensions import db
from .models import User, Post

bp=Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = Post.query.all()
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])

    return render_template('blog/index.html', posts=posts, files=files)

@bp.route('/user')
@login_required
def user():
    page_num = request.args.get('page_num', 1, type=int)
    users = User.query.order_by(User.id.desc()).paginate(per_page=5, page=page_num, error_out=True)

    return render_template('blog/user.html', users=users)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        error=None

        if not title:
            error='Title is required'

        if error is not None:
            flash(error)
        else:
            file = request.files['file']
            filename = secure_filename(file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    error = 'Allowed extensions are .png, .jpg, .jpeg, .gif'
                    flash(error)
                    return redirect(request.url)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            post = Post(title=title,body=body,author_id=current_user.id,author=current_user,filename=filename)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        error=None

        if not title:
            error='Title is required'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], post.filename))
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))

