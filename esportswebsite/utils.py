"""Utils file"""
from base64 import b64encode
from enum import IntEnum

from flask import current_app
from requests import get
import discord

#from Crypto.Cipher import AES # pycryptodome
#from Crypto.Util.Padding import pad


def get_vdo_link(user_type, user_id):
    """Minify and encrypt the VDO link for user_type and user_id"""
    link = current_app.config.get('VDO_SETTINGS', '')
    link = link.replace('{TYPE}', user_type).replace('{ID}', str(user_id))
    if link.startswith("https://obs.ninja/"):
        link = link.replace('https://vdo.ninja/', '')
    elif link.startswith("http://obs.ninja/"):
        link = link.replace('http://vdo.ninja/', '')
    elif link.startswith("obs.ninja/"):
        link = link.replace('vdo.ninja/', '')
    elif link.startswith("https://vdo.ninja/"):
        link = link.replace('https://vdo.ninja/', 'vdo.ninja/')
    elif link.startswith("http://vdo.ninja/"):
        link = link.replace('http://vdo.ninja/', 'vdo.ninja/')

    link = (link
        .replace('&view=','&v=').replace('&view&','&v&')
        .replace('?view&','?v&').replace('?view=','?v=')
        .replace('&videobitrate=','&vb=').replace('?videobitrate=','?vb=')
        .replace('&bitrate=','&vb=').replace('?bitrate=','?vb=')
        .replace('?audiodevice=','?ad=').replace('&audiodevice=','&ad=')
        .replace('?label=','?l=').replace('&label=','&l=')
        .replace('?stereo=','?s=').replace('&stereo=','&s=')
        .replace('&stereo&','&s&').replace('?stereo&','?s&')
        .replace('?webcam&','?wc&').replace('&webcam&','&wc&')
        .replace('?remote=','?rm=').replace('&remote=','&rm=')
        .replace('?password=','?p=').replace('&password=','&p=')
        .replace('?pw=','?p=').replace('&pw=','&p=')
        .replace('&maxvideobitrate=','&mvb=').replace('?maxvideobitrate=','?mvb=')
        .replace('&maxbitrate=','&mvb=').replace('?maxbitrate=','?mvb=')
        .replace('&height=','&h=').replace('?height=','?h=')
        .replace('&width=','&w=').replace('?width=','?w=')
        .replace('&quality=','&q=').replace('?quality=','?q=')
        .replace('&cleanoutput=','&clean=').replace('?cleanoutput=','?clean=')
        .replace('&maxviewers=','&clean=').replace('?maxviewers=','?clean=')
        .replace('&framerate=','&fr=').replace('?framerate=','?fr=')
        .replace('&fps=','&fr=').replace('?fps=','?fr=')
        .replace('&permaid=','&push=').replace('?permaid=','?push=')
        .replace('&roomid=','&r=').replace('?roomid=','?r=')
        .replace('&room=','&r=').replace('?room=','?r='))

    # 32 bytes = AES-256, padding style: 'pkcs7'
    #cipher = AES.new(pad(b'OBSNINJAFORLIFE', 32), AES.MODE_CBC)
    #enc_data = cipher.encrypt(pad(link.encode('utf-8'), AES.block_size))
    #return 'https://invite.cam/' + b64encode(enc_data).decode('utf-8') # This doesnt work
    return 'https://' + link


def check_structure(struct, conf):
    """Check the structure of an object/dict

    :param dict|list|type struct: Structure
    :param dict|list|type conf: Configuration for the structure
    :returns bool: True if structure is correct, else False

    :example: check_structure(my_data, { 'nickname': str, 'rank': { 'cleanName': str } })
    :source: https://stackoverflow.com/a/45812573
    """
    if isinstance(struct, dict) and isinstance(conf, dict):
        # struct is a dict of types or other dicts
        return all(k in conf and check_structure(struct[k], conf[k]) for k in struct)
    if isinstance(struct, list) and isinstance(conf, list):
        # struct is list in the form [type or dict]
        return all(check_structure(struct[0], c) for c in conf)
    if isinstance(conf, type):
        # struct is the type of conf
        return isinstance(struct, conf)
    # struct is neither a dict, nor list, not type
    return False


class PlayerRanks(IntEnum):
    """Player Ranks Enum"""
    NON_DONOR = 1
    VIP = 2
    VIP_PLUS = 3
    MVP = 4
    MVP_PLUS = 5
    SUPERSTAR = 6
    YOUTUBER = 60
    JR_HELPER = 70
    HELPER = 80
    MODERATOR = 90
    ADMIN = 100

def get_player_rank(player, only_packages=False):
    """Extract the player rank from the hypixel player data

    :source: Some nodejs library. Forgot which one it was
    """
    found_rank = PlayerRanks.NON_DONOR
    if only_packages:
        if player.get('monthlyPackageRank'):
            rank = getattr(PlayerRanks, player['monthlyPackageRank'], None)
            if rank:
                found_rank = rank
        if player.get('newPackageRank'):
            rank = getattr(PlayerRanks, player['newPackageRank'], None)
            if rank and rank > found_rank:
                found_rank = rank
        if player.get('packageRank'):
            rank = getattr(PlayerRanks, player['packageRank'], None)
            if rank and rank > found_rank:
                found_rank = rank
    else:
        if 'rank' in player and player['rank'] != "NORMAL":
            rank = getattr(PlayerRanks, player['rank'], None)
            if rank:
                found_rank = rank
            else:
                return get_player_rank(player, True)
        else:
            return get_player_rank(player, True)

    if found_rank == PlayerRanks.VIP:
        out = {
            'priority': found_rank,
            'name': "VIP",
            'cleanName': "VIP",
            'prefix': "§a[VIP]",
            'cleanPrefix': "[VIP]",
            'staff': False,
        }
    elif found_rank == PlayerRanks.VIP_PLUS:
        out = {
            'priority': found_rank,
            'name': "VIP_PLUS",
            'cleanName': "VIP+",
            'prefix': "§a[VIP§6+§a]",
            'cleanPrefix': "[VIP+]",
            'staff': False,
        }
    elif found_rank == PlayerRanks.MVP:
        out = {
            'priority': found_rank,
            'name': "MVP",
            'cleanName': "MVP",
            'prefix': "§b[MVP]",
            'cleanPrefix': "[MVP]",
            'staff': False,
        }
    elif found_rank == PlayerRanks.MVP_PLUS:
        out = {
            'priority': found_rank,
            'name': "MVP_PLUS",
            'cleanName': "MVP+",
            'prefix': "§b[MVP§c+§b]",
            'cleanPrefix': "[MVP+]",
            'staff': False,
        }
    elif found_rank == PlayerRanks.SUPERSTAR:
        out = {
            'priority': found_rank,
            'name': "SUPERSTAR",
            'cleanName': "MVP++",
            'prefix': "§6[MVP§c++§6]",
            'cleanPrefix': "[MVP++]",
            'staff': False,
        }
    elif found_rank == PlayerRanks.YOUTUBER:
        out = {
            'priority': found_rank,
            'name': "YOUTUBER",
            'cleanName': "YOUTUBER",
            'prefix': "§c[§fYOUTUBE§c]",
            'cleanPrefix': "[YOUTUBE]",
            'staff': False,
        }
    elif found_rank == PlayerRanks.JR_HELPER:
        out = {
            'priority': found_rank,
            'name': "JR_HELPER",
            'cleanName': "JR HELPER",
            'prefix': "§9[JR HELPER]",
            'cleanPrefix': "[JR HELPER]",
            'staff': True,
        }
    elif found_rank == PlayerRanks.HELPER:
        out = {
            'priority': found_rank,
            'name': "HELPER",
            'cleanName': "HELPER",
            'prefix': "§9[HELPER]",
            'cleanPrefix': "[HELPER]",
            'staff': True,
        }
    elif found_rank == PlayerRanks.MODERATOR:
        out = {
            'priority': found_rank,
            'name': "MODERATOR",
            'cleanName': "MODERATOR",
            'prefix': "§2[MOD]",
            'cleanPrefix': "[MOD]",
            'staff': True,
        }
    elif found_rank == PlayerRanks.ADMIN:
        out = {
            'priority': found_rank,
            'name': "ADMIN",
            'cleanName': "ADMIN",
            'prefix': "§c[ADMIN]",
            'cleanPrefix': "[ADMIN]",
            'staff': True,
        }
    else:
        out = {
            'priority': found_rank,
            'name': "NON_DONOR",
            'cleanName': "DEFAULT",
            'prefix': "§7",
            'cleanPrefix': "",
            'staff': False,
        }
    return out


BEDWARS_LEVEL_CONSTANTS = {
    "EL": 4,
    "XPP": 487000,
    "LPP": 100,
    "HP": 10
}

def get_bedwars_level_info(data):
    """Extract the bedwars level info from the hypixel player data

    :source: Some nodejs library. Forgot which one it was
    """
    if isinstance(data, (int, float)):
        current_exp = data
    else:
        stats = data.get('stats', {})
        bedwars_stats = stats.get('Bedwars', {})
        current_exp = bedwars_stats.get('Experience') or bedwars_stats.get('Experience_new')

    if not isinstance(current_exp, (int, float)):  # Check for NaN
        raise TypeError("Data supplied does not contain player Bedwars experience.")

    prestiges = int(current_exp // BEDWARS_LEVEL_CONSTANTS["XPP"])
    level = prestiges * BEDWARS_LEVEL_CONSTANTS["LPP"]
    exp_without_prestiges = current_exp - prestiges * BEDWARS_LEVEL_CONSTANTS["XPP"]

    for i in range(1, BEDWARS_LEVEL_CONSTANTS["EL"] + 1):
        el_exp = 500
        r_l = i % BEDWARS_LEVEL_CONSTANTS["LPP"]
        for ii in range(r_l):
            el_exp += ii * 500
        if exp_without_prestiges < el_exp:
            break
        level += 1
        exp_without_prestiges -= el_exp

    level += int(exp_without_prestiges // 5000)
    prestige = int(level // BEDWARS_LEVEL_CONSTANTS["LPP"])

    # prestige shouldn't be higher than BEDWARS_LEVEL_CONSTANTS["HP"]
    prestige = min(prestige, BEDWARS_LEVEL_CONSTANTS["HP"])

    prestige_name = "None"
    prestige_names = {
        1: "Iron",
        2: "Gold",
        3: "Diamond",
        4: "Emerald",
        5: "Sapphire",
        6: "Ruby",
        7: "Crystal",
        8: "Opal",
        9: "Amethyst",
        10: "Rainbow"
    }

    prestige_name = prestige_names.get(prestige, prestige_name)
    level_in_current_prestige = level - prestige * BEDWARS_LEVEL_CONSTANTS["LPP"]

    return {
        "level": level,
        "prestige": prestige,
        "prestigeName": prestige_name,
        "levelInCurrentPrestige": level_in_current_prestige
    }


def get_player_data(username: str):
    """Get hypixel info for username
    Like rank and bedwars level
    """
    r = get(
        "https://api.hypixel.net/v2/player",
        params={"name": username},
        headers={"API-Key": current_app.config['HYPIXEL_API_KEY']},
        timeout=3 # 3 seconds timeout
    )
    result = r.json()

    if not r.ok or not result['success']:
        print(r, result['cause'] if result is not None else r.text)
        return False

    if result['player'] is None:
        return None

    result['player']['nickname'] = (
        result['player']['displayname']
        or (
            result['player']['knownAliases']
            and result['player']['knownAliases'][len(result['player']['knownAliases']) - 1]
        )
        or result['player']['playername']
        or result['player']['username']
     )
    result['player']['rank'] = get_player_rank(result['player'])
    result['player']['bedwarsLevel'] = get_bedwars_level_info(result['player'])
    return result['player']


async def get_igns_from_channel():
    """Extract all submitted IGNs from the discord channel"""
    if (
        current_app.config['DISCORD_TOKEN'] is None
        or current_app.config['DISCORD_CHANNEL_ID'] is None
    ):
        return []

    client = discord.Client(intents=discord.Intents.default())
    try:
        await client.login(current_app.config['DISCORD_TOKEN'])
    except Exception as e:
        print(repr(e))
        return []

    try:
        channel = await client.fetch_channel(current_app.config['DISCORD_CHANNEL_ID'])
    except Exception as e:
        print(repr(e))
        channel = None

    if channel is None:
        await client.close()
        return []

    names = []
    discord_ids = []
    messages = reversed([message async for message in channel.history(limit=100)])
    for message in messages:
        if (
            not message.author.bot and not message.author.id in discord_ids
            and len(message.content) > 0
        ):
            names.append(message.content)
            discord_ids.append(message.author.id)

    await client.close()

    return names

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    player_data = get_player_data("RedMiniontoby")
    print(
        player_data['nickname'],
        '| Rank: ' + player_data['rank']['cleanName'],
        '| BW Level: ' + str(player_data['bedwarsLevel']['level']) + ' stars'
    )

    #import asyncio
    #print(asyncio.run_until_complete(get_igns_from_channel()))
