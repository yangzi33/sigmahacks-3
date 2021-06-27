from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import *
from app.models import Post 

# For user authentication/login/logout
from flask_login import current_user, login_user, logout_user
from app.models import User
from datetime import datetime

@app.route("/")
@app.route("/index")
# Require user to login
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Listing is not live.")
        return redirect(url_for("index"))
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    posts = current_user.followed_posts().all()

    return render_template("index.html", title="Home Page", form=form, posts=posts)

# the methods arguments indicates that this view function accepts
# GET and POST requests, overriding the default of accepting only
# GET request.
@app.route("/login", methods=["GET", "POST"])
def login():
    # Check if logged in
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    # Accept and validte the data submitted by user
    # validate_on_submit: this method does all the form processing stuff.
    # When the browser sends the GET reques to receive the webpage with
    # the form, this method returns False, so the function skips the if
    # statement and render the template directly.
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # check password
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)

        # get next when not logged in, so we can redirect to next after login 
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
        
    # Render template
    return render_template("login.html", title = "Sign In", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User {} is successfully registered.".format(form.username.data))
        return redirect(url_for("login"))
    return render_template("register.html", title="register", form=form)


# Logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    form = EmptyForm()
    return render_template("user.html", user=user, posts=posts, form=form)


# Record the last visit time for a User
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# Edit profile view
@app.route("/edit_profile", methods=["POST", "GET"])        
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", title="Edit Profile", form=form)


@app.route("/explore")
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html", title="Explore", post=posts)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
















