"""ESportsWebsite Main file"""
import os
from flask import abort, Flask, redirect, render_template, request, session, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app(test_config=None):
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        HYPIXEL_API_KEY=None,
        DISCORD_TOKEN=None,
        DISCORD_CHANNEL_ID=None,
        DATABASE=os.path.join(app.instance_path, 'esportswebsite.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # X-Forwarded-For 2 levels behind, since hosted behind reverse proxy behind cloudflare
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import main
    app.register_blueprint(main.bp)

    app.add_url_rule('/', endpoint='index')
    return app

if __name__ == '__main__':
    PORT = os.getenv('SERVER_PORT', os.getenv('PORT', '5000'))
    try:
        PORT = int(PORT)
    except ValueError:
        print('Port is not a number!', PORT)
        PORT = 5000
    create_app().run(
        port=PORT,
        host=os.getenv('SERVER_IP', os.getenv('HOST', '127.0.0.1'))
    )
