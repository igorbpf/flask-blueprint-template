from flask import Blueprint, render_template, request, url_for, make_response
from flask import redirect, jsonify, flash

from ..forms.post_form import Post_Form
from ..models.post import Post

from .. import db

#import bleach

site_mod = Blueprint('site',__name__,template_folder="templates",\
                     static_url_path="static", static_folder="../site/static")


@site_mod.route('/', methods=['GET', 'POST'])
def index():
    form = Post_Form()

    if form.validate_on_submit():

        post = Post(form.title.data, form.post.data)
        db.session.add(post)
        db.session.commit()

        redirect(url_for('site.index'))
    posts = Post.query.all()
    
    return render_template('index.html', form=form, posts=posts)
