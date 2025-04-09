import os, asyncio
from dotenv import load_dotenv
load_dotenv()

from flask import abort, Flask, redirect, render_template, request, session, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

import auth
import utils
from models import Team, Player

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.getenv('APP_SECRET')

app.wsgi_app = ProxyFix(app.wsgi_app)

app.register_blueprint(auth.bp)

colors = ("red", "blue", "green", "yellow", "aqua", "white", "pink", "gray")

teams = (
    Team(1, "red", 2),
    Team(2, "blue", 1),
    Team(3, "green", 1),
    Team(4, "yellow", 1),
)

players = (
    Player(1, "xFlxme", teams[0]),
    Player(2, "Sololad", teams[0]),
    Player(3, "DrBoolFliker", teams[0]),
    Player(4, "Mang0sorbet", teams[0]),
    
    Player(5, "oCxmboo", teams[1]),
    Player(6, "RedMiniontoby", teams[1]),
    Player(7, "LeoNoche", teams[1]),
    Player(8, "TheTrueCheeseMan", teams[1]),

    Player(9, "RealSuper", teams[2]),
    Player(10, "Akmatras", teams[2]),
    Player(11, "MindaMann", teams[2]),
    Player(12, "Weconds", teams[2]),
    
    Player(13, "uDeath", teams[3]),
    Player(14, "AnxiousPiggy", teams[3]),
    Player(15, "SOMEBLANKET", teams[3]),
    Player(16, "xReefed", teams[3]),

    Player(17, "RedMiniontoby2"),
)


@app.route("/")
@auth.login_required
def index():
    return render_template('index.html')

loop = asyncio.get_event_loop()

@app.route("/manage_players")
@auth.login_required
def manage_players():
    players_datas = []
    #names = loop.run_until_complete(utils.get_igns_from_channel())
    names = [player.nickname for player in players]
    # Normally we just only get nicknames from discord channel, so don't expect Player objects!
    for name in names:
        player_data = utils.get_player_data(name)
        if not player_data is None:
            players_datas.append(player_data)

    return render_template('manage_players.html', players=players_datas, teams=teams)

@app.route("/manage_teams")
@auth.login_required
def manage_teams():
    return render_template('manage_teams.html', colors=colors, teams=teams)

@app.route('/overlay/<user_type>/<int:user_id>')
def overlay(user_type, user_id):
    if (user_type == "player" or user_type == "camera" or user_type == "commentary") and user_id > 0:
        player = None
        if user_type == "player":
            player = players[user_id - 1]
        return render_template('overlay.html', user_type=user_type, player=player, teams=teams)
    abort(404)

if __name__ == '__main__':
    app.run(port=os.getenv('SERVER_PORT', os.getenv('PORT', 5000)), host=os.getenv('SERVER_IP', os.getenv('HOST', '127.0.0.1')))    
