import app.api as api
import app.controller.database as db
import app.controller.food as food
import app.controller.home as home
import app.controller.log as log
import app.controller.login as login
import app.controller.preferences as preferences
import app.controller.usda as usda
import app.controller.weight as weight
from app.pkg.config import Config
from app import create_app


def run():
    app = create_app()

    app.register_blueprint(login.login_bp)
    app.register_blueprint(db.db_bp)
    app.register_blueprint(weight.weight_bp)
    app.register_blueprint(food.food_bp)
    app.register_blueprint(log.log_bp)
    app.register_blueprint(preferences.preferences_bp)
    app.register_blueprint(home.home_bp)
    app.register_blueprint(usda.usda_bp)
    app.register_blueprint(api.bp)

    config = Config()
    app.run(host=config.server.HOST, port=config.server.PORT)


if __name__ == "__main__":
    run()
