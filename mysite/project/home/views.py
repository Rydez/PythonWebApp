                    #################
                    #### imports ####
                    #################


from project import db
from project.models import UserPost, VotedUsers
from project.home import redirect_url
from flask import render_template, request, redirect, flash, url_for, Blueprint
from flask.ext.login import login_required, current_user
from formlogic import login, registration, LoginForm, RegistrationForm, \
    PostForm, validateVote


                #######################
                #### configuration ####
                #######################


home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


                    ################
                    #### routes ####
                    ################


### This route probably needs help, and has been neglected throughout
### updating the rest of the application.
@home_blueprint.route('/admin/', methods = ['GET', 'POST'])
@login_required
def admin():
    """
    Route to the admin page.

        Get all posts from the database.
        Create the object, post form.
        Handle adding a post.
    """

    posts = db.session.query(UserPost).all()
    post_form = PostForm(prefix='post_form')

    if post_form.validate_on_submit():
        new_post = UserPost(
            post_form.title.data,
            post_form.description.data,
            current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Way to go! you made a post :)')
        return redirect(url_for('home.homepage'))

    return render_template("admin.html", posts=posts, post_form=post_form)


@home_blueprint.route('/upvotepost/<post_id>', methods=['GET', 'POST'])
@login_required
def upvotepost(post_id):
    """
    Route to upvote a post.

        Convert the post ID (from the web address) to an integer.
        Use the validateVote function from the formlogic module.
    """

    post_id = int(post_id)
    vote_value = 1
    validateVote(post_id, current_user, vote_value)
    return redirect(redirect_url())


@home_blueprint.route('/downvotepost/<post_id>', methods=['GET', 'POST'])
@login_required
def downvotepost(post_id):
    """
    Route to downvote a post.

        Convert the post ID (from the web address) to an integer.
        Use the validateVote function from the formlogic module.
    """

    post_id = int(post_id)
    vote_value = -1
    validateVote(post_id, current_user, vote_value)
    return redirect(redirect_url())


### Currently only available on the admin page.
### Should be an option on the homepage for an admin user.
@home_blueprint.route('/deletepost/<post_id>', methods=['GET', 'POST'])
def deletepost(post_id):
    """
    Route to delete a post.

        Convert the post ID (from the web address) to an integer.
        Delete the post with that ID and commit.
    """

    post_id = int(post_id)
    UserPost.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(redirect_url())


@home_blueprint.route('/register/', methods = ['GET', 'POST'])
def register():
    """
    Route to the register page.

        Create the login and registration form objects.
        Determine whether to login or register based on button pressed.
        Return the appropriate function.
        login and register functions are from the formlogic module.
    """

    login_form = LoginForm(prefix='login_form')
    registration_form = RegistrationForm(prefix='registration_form')

    if request.form.get('button') == 'Login':
        return login(login_form)
    elif request.form.get('button') == 'Register':
        return registration(registration_form)

    return render_template('register.html',
                          login_form = LoginForm(prefix='login_form'),
                          registration_form = RegistrationForm(prefix='registration_form'))


### The form for posting is not locked by a login required wrapper.
### Instead, the main.html template handles hiding this feature
### from users which are not logged in. <--Change this to be handled here.
@home_blueprint.route('/', methods = ['GET', 'POST'])
def homepage():
    """
    Route to the main page.

        Create the object, login form.
        Get posts in order, by vote count.
        Create the object, post form.
        Create a list which contains all of the IDs of posts which have votes.
        Get the votes relevent to the current user (if they're logged in).
        Determine whether the login button has been pressed.
        Handle posting.
    """

    login_form = LoginForm(prefix='login_form')
    posts = db.session.query(UserPost).order_by(UserPost.votes.desc()).all()
    post_form = PostForm(prefix='post_form')

    ### This creates a list, but the format is strange.
    ### The list created looks like: [(1,), (2,), (3,)]
    ### This had to be compensated for in the template.
    voted_posts = [vote for vote in db.session.query(VotedUsers.voted_post).all()]

    user_votes = None
    if current_user.is_authenticated():
        user_votes  = VotedUsers.query.filter_by(voted_user=current_user.id).all()

    if request.form.get('button') == 'Login':
        return login(login_form)

    ### This should probably be a function in the form logic module.
    if post_form.validate_on_submit():
        vote_count = 0
        new_post = UserPost(
            post_form.title.data,
            post_form.description.data,
            post_form.link.data,
            vote_count,
            current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Way to go! You made a post :)')
        return redirect(url_for('home.homepage'))

    return render_template('main.html',
                           user_votes=user_votes,
                           post_form=post_form, posts=posts,
                           voted_posts=voted_posts,
                           login_form=LoginForm(prefix='login_form'))




