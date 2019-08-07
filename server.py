import os

import controller.database
import controller.food
import controller.home
import controller.log
import controller.login
import controller.weight
import controller.routes as routes
import pkg.config as config
import shared
from view.registration_form import RegistrationForm

import model.user as users

def init():
    config.load_config("conf/config.ini")
    shared.init()

    # TODO: config these
    shared.app.template_folder = os.path.join(os.getcwd(), "templates")
    shared.app.static_folder = os.path.join(os.getcwd(), "static")

    shared.app.register_blueprint(routes.login_controller)
    shared.app.register_blueprint(routes.db_controller)
    shared.app.register_blueprint(routes.weight_controller)
    shared.app.register_blueprint(routes.food_controller)
    shared.app.register_blueprint(routes.log_controller)
    shared.app.register_blueprint(routes.home_controller)


if __name__ == "__main__":
    init()
    shared.app.run(host=config.values["server"]["host"], port=config.values["server"]["port"])
