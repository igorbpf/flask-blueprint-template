from flask import Blueprint, render_template, request, url_for, make_response
from flask import redirect, jsonify, flash, g, abort

from ..forms.post_form import Post_Form

from ..models.post import Post
from ..models.user import User

from .. import db, app, celery

from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_mail import Mail, Message

mail = Mail(app)

from itsdangerous import URLSafeTimedSerializer

ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

login_manager.login_message_category = "danger"


#import bleach

site_mod = Blueprint('site',__name__,template_folder="templates",\
                     static_url_path="static", static_folder="../site/static")


# @site_mod.route('/', methods=['GET', 'POST'])
# def index():
#     form = Post_Form()
#
#     if form.validate_on_submit():
#
#
#         post = Post(form.title.data, form.post.data, form.tag.data)
#         db.session.add(post)
#         db.session.commit()
#
#
#         redirect(url_for('site.index'))
#
#
#     posts = Post.query.all()
#     return render_template('index.html', form=form, posts=posts)



########################################################################


@celery.task
def send_async_email(info):
    """Background task to send an email with Flask-Mail."""
    header = 'Hello from App'


    print(info['recipients'])
    print(info['message'])
    message = info['message']
    recipients = info['recipients']
    with app.app_context():
        msg = Message(header, recipients=recipients)
        msg.body = message
        mail.send(msg)


@celery.task
def send_register_email(paylod):
    """Background task to send an email with Flask-Mail."""
    header = 'Register in the app'


    # print(info['recipients'])
    # print(info['message'])
    # message = info['message']
    # recipients = info['recipients']
    email = [paylod['email']]
    subject = paylod['subject']
    html = paylod['html']
    with app.app_context():
        msg = Message(header, recipients=email)
        msg.body = subject
        msg.html = html
        mail.send(msg)



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@site_mod.route('/')
@login_required
def index():
    posts = Post.query.filter_by(user_id=g.user.id).order_by(Post.date_created.desc()).all()
    return render_template('index.html', posts=posts)


@site_mod.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    has_user = User.query.filter_by(email=email).first()
    if has_user:
        flash("This email is already in use", "warning")
        return redirect(url_for('site.register'))
    user = User(username, email)
    user.hash_password(password)

    db.session.add(user)
    db.session.commit()

    subject = "Confirm your email"

    token = ts.dumps(email, salt='email-confirm-key')

    confirm_url = url_for(
        'confirm_email',
        token=token,
        _external=True
    )

    html = render_template('activate.html',
                           confirm_url=confirm_url)

    payload = {'email': email, 'subject': subject, 'html': html}

    send_register_email.apply_async(args=[payload])

    flash('User successfully registered', 'success')

    return redirect(url_for('site.index'))


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('site.login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method  == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    remember_me = False

    if 'remember_me' in request.form:
        remember_me = True

    registered_user = User.query.filter_by(username=username).first()

    if registered_user is None or not registered_user.verify_password(password):
        flash('Username or Password is invalid', 'danger')
        return redirect(url_for('site.index'))

    # send the email
    #email = registered_user.email
    # msg = Message('Hello from Flask',
    #               recipients=[email])
    # msg.body = 'This is a test email sent from a background Celery task.'
    # send_async_email.delay(msg)

    #message = 'This is a test email sent from a background Celery task.'
    #recipients = email

    #send_async_email.apply_async(args=[{'message':message, 'recipients':[recipients]}])


    #flash('Sending email to {0}'.format(email), 'info')

    login_user(registered_user, remember=remember_me)
    flash('Logged in successfully', 'success')

    return redirect(request.args.get('next') or url_for('site.index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.login'))



@app.route('/youpost', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Title is required', 'danger')

        elif not request.form['text']:
            flash('Text is required', 'danger')

        else:
            post = Post(request.form['title'], request.form['text'])
            post.user = g.user
            db.session.add(post)
            db.session.commit()

            flash('Post item was successfully created', 'success')
            return redirect(url_for('site.index'))

    return render_template('new.html')


@app.route('/posts/<int:post_id>', methods=['GET', 'POST'])
@login_required
def show_or_update(post_id):
    post_item = Post.query.get(post_id)

    if request.method == 'GET':
        return render_template('view.html', post=post_item)

    # if post_item.user.id == g.user.id:
    #     post_item.title = request.form['title']
    #     post_item.text = request.form['text']
    #     post_item.done = ('done.%d' % post_id) in request.form
    #     db.session.commit()
    #     return redirect(url_for('index'))

    flash('You are not authorized to edit this post item', 'danger')
    return redirect(url_for('site.show_or_update', post_id=post_id))


@site_mod.route('/about')
def about():
    return render_template('about.html')

@site_mod.route('/contact')
def contact():
    return render_template('contact.html')

@site_mod.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@site_mod.before_request
def before_request():
    g.user = current_user
