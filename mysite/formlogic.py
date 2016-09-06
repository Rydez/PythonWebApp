"""
    This module contains Form Classes and helper functions for dealing with
    forms and form like things.

    ### Consider new modules for form like things. lol.
"""

from project import db
from project.home import redirect_url
from flask import render_template, flash, url_for, redirect
from flask.ext.wtf import Form
from flask.ext.login import login_user
from project.models import User, VotedUsers, UserPost
from wtforms import BooleanField, TextField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from passlib.hash import sha256_crypt


                        #################
                        #### Classes ####
                        #################


class PostForm(Form):
    """
    Object for creating post forms. This heavily utilizes
    the WTForms module of flask.

        Fields:
            title, link, description
    """

    title = TextField('Title', validators=[DataRequired()])
    link  = TextField('Link', validators=[DataRequired()])
    description = TextAreaField(
        'Description', validators=[DataRequired(), Length(max=150)])


class LoginForm(Form):
    """
    Object for creating login forms.
    """

    login_user = TextField('Username', validators=[DataRequired()])
    login_pass = PasswordField('Password', validators=[DataRequired()])

### Class for registration form which uses WTForms to create and validate.
class RegistrationForm(Form):
    """
    Object for creating a registration form.

        Fields:
            username, email, password, confirm password,
            accept terms of service.
    """

    username = TextField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=20)]
    )

    email = TextField(
        'Email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=50)]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )

    confirm_password = PasswordField(
        'Repeat Password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )

    accept_tos = BooleanField(
        'I accept whatever',
        validators=[DataRequired()]
    )


                        ###################
                        #### Functions ####
                        ###################


def login(login_form):
    """
    Handle user login in.

        Get info from the login form.
        Check for user existance.
        login using flash login module.
    """

    if login_form.validate_on_submit():
        input_user = login_form.login_user.data
        input_pass = login_form.login_pass.data
        user = User.query.filter_by(name=input_user).first()
        if user is not None and sha256_crypt.verify(input_pass, user.password):
            login_user(user)
            flash('Login success')
            return redirect(redirect_url())
        else:
            flash('Incorrect credentials')
            return redirect(redirect_url())
    flash('Why you no enter username and password?!')
    return redirect(redirect_url())


def registration(registration_form):
    """
    Handle registration for anons.

        Check if the form has been filled out correctly.
        Check if the username or email has been taken.
        Otherwise create user.
    """

    error = ''
    if registration_form.validate_on_submit():
        name  = registration_form.username.data
        email = registration_form.email.data
        if db.session.query(User.id).filter(User.name == name).count() > 0:
            flash('That username is already taken.')
            return redirect(url_for('home.register'))
        elif db.session.query(User.id).filter(User.email == email).count() > 0:
            flash('That email is already taken.')
            return redirect(url_for('home.register'))
        else:
            user = User(
                name, email,
                password = sha256_crypt.encrypt((str(registration_form.password.data)))
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Great Success!!!')
            return redirect(url_for('home.homepage'))

    return render_template('register.html', error=error,
                          login_form = LoginForm(prefix='login_form'),
                          registration_form = registration_form)


def validateVote(post_id, current_user, vote_value):
    """
    Handle post votes from logged in users.

        Get votes relevent to the current user.
        Determine if current user has already voted.
        If user attempts second vote, remove user's current vote.
        If user attempts first vote, create new vote for current user.

        ### Strange thing: vote_value is used weirdly.
        ### ie: if vote_value == vote_value.
        ### But it works for now.
    """

    voted_users = VotedUsers.query.filter_by(voted_user=current_user.id).all()
    already_voted = False
    for user in voted_users:
        if user.voted_post == post_id:
            vote_value    = user.vote_value
            voted_user_id = user.id
            already_voted = True

    if already_voted and vote_value == vote_value:
        selected_post = UserPost.query.filter_by(id=post_id).first()
        selected_post.votes -= vote_value
        VotedUsers.query.filter_by(id=voted_user_id).delete()

    elif not already_voted:
        selected_post = UserPost.query.filter_by(id=post_id).first()
        selected_post.votes += vote_value
        voted_user = VotedUsers(post_id, current_user.id, vote_value)
        db.session.add(voted_user)

    db.session.commit()
    return

