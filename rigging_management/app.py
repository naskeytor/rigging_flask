from flask import Flask, render_template
from rigging_management.extensions import db, migrate
from flask_login import LoginManager
from rigging_management.models.models import User
from config import DevelopmentConfig
from context_processors import (inject_rigging_types, inject_rigs, inject_rigging_sizes, inject_manufacturers,
                                inject_rigging, inject_rigging_components, inject_component_processor)
import mysql.connector
from mysql.connector import errorcode


def create_app():
    application = Flask(__name__)
    application.config.from_object(DevelopmentConfig)

    login_manager = LoginManager()
    login_manager.init_app(application)
    login_manager.login_view = 'auth.login'  # Redirige a la vista de login si no está autenticado

    db.init_app(application)
    migrate.init_app(application, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from blueprints.auth.routes import auth_bp
    from blueprints.components.routes import components_bp
    from blueprints.rigs.routes import rigs_bp
    from blueprints.rigging.routes import rigging_bp
    from blueprints.manufacturers.routes import manufacturers_bp
    from blueprints.sizes.routes import sizes_bp
    from blueprints.statuses.routes import statuses_bp
    from blueprints.component_types.routes import component_types_bp
    from blueprints.models.routes import models_bp
    from blueprints.main.routes import main_bp

    application.register_blueprint(auth_bp)
    application.register_blueprint(components_bp)
    application.register_blueprint(rigs_bp)
    application.register_blueprint(rigging_bp)
    application.register_blueprint(manufacturers_bp)
    application.register_blueprint(sizes_bp)
    application.register_blueprint(statuses_bp)
    application.register_blueprint(component_types_bp)
    application.register_blueprint(models_bp)
    application.register_blueprint(main_bp)

    application.context_processor(inject_rigging)
    application.context_processor(inject_rigging_types)
    application.context_processor(inject_rigging_components)
    application.context_processor(inject_rigs)
    application.context_processor(inject_component_processor)
    application.context_processor(inject_rigging_sizes)
    application.context_processor(inject_manufacturers)

    @application.route('/')
    def index():
        return render_template('index.html')

    return application

