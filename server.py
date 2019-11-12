import app.api as api
import app.controller.blog as blog
import app.controller.database as db
import app.controller.food as food
import app.controller.home as home
import app.controller.log as log
import app.controller.login as login
import app.controller.preferences as preferences
import app.controller.tdee as tdee
import app.controller.usda as usda
import app.controller.weight as weight
import app.model.user as _user
from app.pkg.config import Config, get_secrets
from app.pkg.db import get_db
from app import create_app

def run():
    app = create_app()

    app.register_blueprint(login.login_bp)
    app.register_blueprint(db.db_bp)
    app.register_blueprint(blog.blog_bp)
    app.register_blueprint(weight.weight_bp)
    app.register_blueprint(food.food_bp)
    app.register_blueprint(log.log_bp)
    app.register_blueprint(preferences.preferences_bp)
    app.register_blueprint(tdee.tdee_bp)
    app.register_blueprint(home.home_bp)
    app.register_blueprint(usda.usda_bp)
    app.register_blueprint(api.bp)

    config = get_secrets(Config())
    if not _user.get_user_by_username(get_db(config), config.db.USERS, "admin"):
        admin_user = _user.User(
            username="admin",
            email=config.server.ADMIN_EMAIL,
            usda_api_key=config.secrets.USDA_API_KEY
        )
        admin_user.set_password(config.secrets.ADMIN_USER_PASSWORD)
        admin_user.insert(get_db(config), config.db.USERS)
        admin_user.update(get_db(config), config.db.USERS)
    app.run(host=config.server.HOST, port=config.server.PORT)

if __name__ == "__main__":
    run()
