def create_app(test_config='app.settings.Conf'):
    import logging
    import os

    from quart import Quart

    app = Quart(__name__, static_url_path='/static')

    app.config.from_object(test_config)
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

    @app.post('/navigate_to_telemost')
    async def navigate_to_telemost() -> dict:
        return {'type': 'navigate', 'navigate_to_url': 'https://telemost.yandex.ru/'}

    @app.before_serving
    async def startup():
        pass

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

    return app
