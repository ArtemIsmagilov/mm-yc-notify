def create_app(test_config=None):
    from flask import Flask, request
    import logging, os

    app = Flask(__name__, instance_relative_config=True, static_url_path='/static', static_folder='./static')
    os.makedirs(app.instance_path, exist_ok=True)

    @app.route('/manifest.json')
    def manifest() -> dict:
        return app_handlers.manifest()

    @app.route('/bindings', methods=['GET', 'POST'])
    def on_bindings() -> dict:
        return app_handlers.bindings()

    @app.route('/ping', methods=['POST'])
    def on_ping() -> dict:
        logging.debug('ping...')
        return {'type': 'ok'}

    @app.route('/install', methods=['GET', 'POST'])
    def on_install() -> dict:
        print(f'on_install called with payload , {request.args}, {request.data}', flush=True)
        return {'type': 'ok', 'text': 'success installing...'}

    @app.route('/help_info', methods=['POST'])
    def help_info() -> dict:
        return app_handlers.help_info(request)

    @app.before_request
    def load_user():
        get_user(request)

    from .app_handlers import get_user, static_file

    from .connections import connection_app
    app.register_blueprint(connection_app.bp)

    from .calendars import calendar_app
    app.register_blueprint(calendar_app.bp)

    from .notifications import notification_app
    app.register_blueprint(notification_app.bp)

    from .checks import check_app
    app.register_blueprint(check_app.bp)

    from .database import db
    db.init_app(app)

    from .schedulers import sd
    sd.init_app(app)

    return app
