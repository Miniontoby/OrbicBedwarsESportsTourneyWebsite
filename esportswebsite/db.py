"""Database wrapper/utils

Copyright 2025 - Miniontoby
"""
import sqlite3
from datetime import datetime

import click
from flask import current_app, g
from werkzeug.security import generate_password_hash

from .utils import get_player_data, check_structure

def get_db():
    """Get database object or initialize one"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def get_players():
    """Get a list of all players.
    Also updates the rank and bedwarsLevel if not present"""
    db = get_db()
    players = db.execute("""
SELECT * FROM player
WHERE (rank is NULL OR rank IS NOT "") AND (bedwarsLevel IS NULL or bedwarsLevel > -1)
ORDER BY team_id, nickname COLLATE NOCASE
""").fetchall()
    updated = False
    for player in players:
        if player['rank'] is None or player['bedwarsLevel'] is None:
            player_data = get_player_data(player["nickname"])
            if player_data is False:
                db.execute(
                    'UPDATE player SET rank = ?, bedwarsLevel = -1 WHERE id = ?',
                    ("", player["id"])
                )
                updated = True
            elif player_data is not None:
                rank = player_data["rank"]["cleanName"]
                bedwars_level = player_data["bedwarsLevel"]["level"]
                db.execute(
                    'UPDATE player SET rank = ?, bedwarsLevel = ? WHERE id = ?',
                    (rank, bedwars_level, player["id"])
                )
                updated = True

    if updated:
        db.commit()
        players = db.execute("""
SELECT * FROM player
WHERE rank IS NOT "" AND bedwarsLevel > -1
ORDER BY team_id, nickname COLLATE NOCASE
""").fetchall()

    return players

def get_playing_players():
    """Get a filtered list of all players with a team"""
    all_players = get_players()
    players = []
    for player in all_players:
        if player['team_id'] is not None:
            players.append(player)
    return players

def add_player(player_data):
    """Add a new player using the player_data from hypixel"""
    if check_structure(player_data, {
        'nickname': str,
        'rank': {
            'cleanName': str
        },
        'bedwarsLevel': {
            'level': int
        }
    }):
        db = get_db()

        # Gets unused id value. Source: https://stackoverflow.com/a/907300
        player_id = db.execute("""
SELECT  id
FROM    (SELECT 1 AS id) q1
WHERE   NOT EXISTS
        (SELECT 1 FROM player WHERE id = 1)
UNION ALL
SELECT  *
FROM    (
        SELECT  id + 1
        FROM    player t
        WHERE   NOT EXISTS
                (SELECT 1 FROM player ti WHERE ti.id = t.id + 1)
        ORDER BY id
        LIMIT 1
        ) q2
ORDER BY id
LIMIT 1
""")
        nickname = player_data['nickname']
        rank = player_data['rank']['cleanName']
        bedwars_level = player_data['bedwarsLevel']['level']
        db.execute(
            'INSERT INTO player (id, nickname, rank, bedwarsLevel) VALUES (?, ?, ?, ?)',
            (player_id, nickname, rank, bedwars_level)
        )
        db.commit()
    else:
        print('not validated', player_data)

def remove_player(player_id = None, nickname = None):
    """Remove a player based on player_id or nickname"""
    db = get_db()
    if player_id is not None:
        db.execute('DELETE FROM player WHERE id = ?', (player_id, ))
    elif nickname is not None:
        return
        #db.execute('DELETE FROM player WHERE nickname = ?', (nickname, ))
    else:
        return
    db.commit()

def get_teams():
    """Get a list of all teams and their team color as color_name"""
    db = get_db()
    return db.execute("""
SELECT t.id, t.color_id, t.score, t.username, c.name AS color_name
FROM team t
LEFT JOIN color c ON t.color_id = c.id
""").fetchall()

def get_colors():
    """Get a list of all colors"""
    db = get_db()
    return db.execute('SELECT id, name FROM color').fetchall()

def close_db(e=None):
    """Close the database. Used in breakdown function"""
    db = g.pop('db', None)

    if db is not None and e is None or e is not None:
        db.close()

def init_db():
    """Execute the database schema on the current database"""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@click.option('--username', prompt=True, prompt_required=True)
@click.password_option() # Will ask for password with confirm and hide input
def init_db_command(username: str, password: str):
    """Clear the existing data and create new tables."""
    init_db()

    db = get_db()
    db.execute(
        'INSERT INTO user (id, username, password) VALUES (1, ?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()

    click.echo('Initialized the database.')

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    """Internal function for flask"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
