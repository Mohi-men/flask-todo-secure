from flask import Flask
from flask_assets import Bundle
from .extensions import db, migrate, login_manager, assets

def create_app(config_class="config.DevConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    assets.init_app(app)

    # SCSS bundles (fixed paths)
    auth_scss = Bundle(
        "scss/auth/auth.scss",
        filters="libsass,cssmin",
        output="css/auth.min.css",
        depends="scss/auth/*.scss"
    )
    todo_scss = Bundle(
        "scss/todos/todo.scss",
        filters="libsass,cssmin",
        output="css/todo.min.css",
        depends="scss/todos/*.scss"
    )
    edit_scss = Bundle(
        "scss/todos/edit.scss",
        filters="libsass,cssmin",
        output="css/edit.min.css",
        depends="scss/todos/*.scss"
    )
    main_scss = Bundle(
    "scss/main/main.scss",
    filters="libsass,cssmin",
    output="css/main.min.css",
    depends="scss/main/*.scss"
    )

    # register bundles
    assets.register("main_css", main_scss)
    assets.register("auth_css", auth_scss)
    assets.register("todo_css", todo_scss)
    assets.register("edit_css", edit_scss)

    # blueprints...
    from .auth import bp as auth_bp
    from .todo import bp as todo_bp
    from .main import bp as main_bp
    from .ai import bp as ai_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(todo_bp, url_prefix="/todos")
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_bp)


    return app