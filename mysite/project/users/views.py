                    #################
                    #### imports ####
                    #################


from flask import flash, redirect, url_for, Blueprint
from flask.ext.login import login_required, logout_user
import gc


                    ################
                    #### config ####
                    ################


users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


                    ################
                    #### routes ####
                    ################


@users_blueprint.route('/logout/')
@login_required
def logout():
    """
    Route to logout if logged in.
    """

    logout_user()
    flash('You have logged out!')
    gc.collect()
    return redirect(url_for('home.homepage'))


@users_blueprint.route('/user/<username>/')
@login_required
def profile(username):
    """
    Route to user profile.
    """

    return

