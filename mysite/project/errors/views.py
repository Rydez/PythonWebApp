                  #################
                  #### imports ####
                  #################


from flask import Blueprint, render_template
from formlogic import LoginForm


                ########################
                #### error handlers ####
                ########################


error_blueprint = Blueprint('errors', __name__)

### 404 errors page should be update. It's ugly.
@error_blueprint.app_errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors.
    """

    return render_template("404.html",
                           login_form = LoginForm(prefix='login_form')), 404


### 405 page should be updated. It's ugly.
@error_blueprint.app_errorhandler(405)
def method_not_found(e):
    """
    Handle 405 errors.
    """

    return render_template("405.html",
                           login_form = LoginForm(prefix='login_form')), 405




