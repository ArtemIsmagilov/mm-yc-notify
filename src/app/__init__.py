def create_app(test_config=None):
    from quart import Quart
    import logging, os

    app = Quart(__name__, instance_relative_config=True, static_url_path='/static', static_folder='./static')
    os.makedirs(app.instance_path, exist_ok=True)

    @app.get('/manifest.json')
    async def manifest() -> dict:
        return app_handlers.manifest()

    @app.post('/bindings')
    async def on_bindings() -> dict:
        return app_handlers.bindings()

    @app.post('/ping')
    async def on_ping() -> dict:
        logging.debug('ping...')
        return {'type': 'ok'}

    @app.post('/install')
    async def on_install() -> dict:
        return {'type': 'ok', 'text': 'success installing...'}

    @app.post('/uninstall')
    async def un_install() -> dict:
        return {'type': 'ok', 'text': 'success uninstalling...'}

    @app.post('/help_info')
    async def help_info() -> dict:
        return await app_handlers.help_info()

    @app.after_serving
    async def shutdown():
        await engine.dispose()

    from .sql_app.database import engine
    from . import app_handlers

    from .connections import connection_app

    app.register_blueprint(connection_app.bp)

    from .calendars import calendar_app

    app.register_blueprint(calendar_app.bp)

    from .notifications import notification_app

    app.register_blueprint(notification_app.bp)

    from .checks import check_app

    app.register_blueprint(check_app.bp)

    from .sql_app import db_CLI

    db_CLI.init_app(app)

    from .settings import envs

    if envs.DEBUG:
        logging.basicConfig(level=logging.DEBUG)

    return app
