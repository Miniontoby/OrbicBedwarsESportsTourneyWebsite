"""Main blueprint"""
import asyncio

from flask import (
    Blueprint, g, render_template, request
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from .auth import login_required
from .db import (
    get_db, get_players, get_playing_players, add_player, remove_player, get_teams, get_colors
)
from . import utils

bp = Blueprint('main', __name__)

@bp.route("/")
@login_required()
def index():
    """Index page"""
    return render_template('index.html')

loop = asyncio.get_event_loop()

@bp.route("/manage_players", methods=('GET', 'POST'))
@login_required("user")
def manage_players():
    """Manage players page"""
    db = get_db()
    players = get_players()
    teams = get_teams()

    if request.method == 'POST':
        for player in players:
            team_id = request.form['player-team-' + str(player['id'])]
            if team_id is not None and team_id != player["team_id"]:
                if not team_id.isdigit():
                    team_id = None
                db.execute(
                    'UPDATE player SET team_id = ?'
                    ' WHERE id = ?',
                    (team_id, player['id'])
                )
        db.commit()
        players = get_players()

    names = loop.run_until_complete(utils.get_igns_from_channel())
    names = [n.lower() for n in names]
    names_not_in = []
    names_removed = []

    for name in names:
        if not name in [p["nickname"].lower() for p in players]:
            names_not_in.append(name)

    for p in players:
        if not p["nickname"].lower() in names:
            names_removed.append(p["nickname"])

    for name in names_removed:
        print('Remove user', name)
        remove_player(nickname=name)

    for name in names_not_in:
        player_data = utils.get_player_data(name)
        if not player_data is None:
            add_player(player_data)
        else:
            print('User doesnt exist', name)
            add_player({
                'nickname': name,
                'rank': {
                    'cleanName': ""
                },
                'bedwarsLevel': {
                    'level': -1
                }
            })

    players = get_players()

    return render_template('manage_players.html', players=players, teams=teams)

@bp.route("/manage_teams", methods=('GET', 'POST'))
@login_required("user")
def manage_teams():
    """Manage teams page"""
    db = get_db()
    colors = get_colors()
    teams = get_teams()
    players = get_players() # only to show the players in their teams

    if request.method == 'POST':
        for team in teams:
            color = request.form.get('color-' + str(team['id']))
            score = request.form.get('score-' + str(team['id']))
            username = request.form.get('username-' + str(team['id']))
            password = request.form.get('password-' + str(team['id']))

            if color is not None and score is not None and username is not None:
                if password is not None and len(password) > 0:
                    db.execute(
                        'UPDATE team SET color_id = ?, score = ?, username = ?, password = ?'
                        ' WHERE id = ?',
                        (color, score, generate_password_hash(password), team['id'])
                    )
                else:
                    db.execute(
                        'UPDATE team SET color_id = ?, score = ?, username = ?'
                        ' WHERE id = ?',
                        (color, score, username, team['id'])
                    )
        db.commit()

        teams = get_teams()

    return render_template('manage_teams.html', colors=colors, teams=teams, players=players)

@bp.route("/team_page")
@login_required("team")
def team_page():
    """Team Info page"""
    all_players = get_players()
    players = [player for player in all_players if player["team_id"] == g.team["id"]]
    return render_template('team_page.html', players=players, get_vdo_link=utils.get_vdo_link)

@bp.route('/overlay/<user_type>/<int:user_id>', methods=('GET', 'PATCH'))
def overlay(user_type, user_id):
    """Overlay page, doesn't require authentication"""
    teams = get_teams()
    players = get_playing_players()
    if user_type in ["player", "camera", "commentary"] and user_id > 0:
        player = None
        if user_type == "player":
            if user_id - 1 < len(player):
                player = players[user_id - 1]
        if request.method == 'PATCH':
            return {
                "player": player,
                "teams": [{**team} for team in teams],
            }
        return render_template('overlay.html', user_type=user_type, player=player, teams=teams)
    return abort(404)
