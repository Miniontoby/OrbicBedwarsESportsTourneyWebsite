import os
from json import loads as json_loads, dumps as json_dumps
from requests import get
import discord

class PlayerRanks:
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
    if isinstance(data, (int, float)):
        current_exp = data
    else:
        stats = data.get('stats', {})
        bedwars_stats = stats.get('Bedwars', {})
        current_exp = bedwars_stats.get('Experience') or bedwars_stats.get('Experience_new')
    
    if not isinstance(current_exp, (int, float)) or current_exp != current_exp:  # Check for NaN
        raise TypeError("Data supplied does not contain player Bedwars experience.")
    
    prestiges = int(current_exp // BEDWARS_LEVEL_CONSTANTS["XPP"])
    level = prestiges * BEDWARS_LEVEL_CONSTANTS["LPP"]
    exp_without_prestiges = current_exp - prestiges * BEDWARS_LEVEL_CONSTANTS["XPP"]
    
    for i in range(1, BEDWARS_LEVEL_CONSTANTS["EL"] + 1):
        el_exp = 500
        rL = i % BEDWARS_LEVEL_CONSTANTS["LPP"]
        for ii in range(rL):
            el_exp += ii * 500
        if exp_without_prestiges < el_exp:
            break
        level += 1
        exp_without_prestiges -= el_exp
    
    level += int(exp_without_prestiges // 5000)
    prestige = int(level // BEDWARS_LEVEL_CONSTANTS["LPP"])
    
    if prestige > BEDWARS_LEVEL_CONSTANTS["HP"]:
        prestige = BEDWARS_LEVEL_CONSTANTS["HP"]
    
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
    """
    Get hypixel info for username
    Like rank and bedwars level
    """

    result = { "success": False }
    existed = False

    try:
        f = open("users/" + username + ".json", "r")
        result = { "success": True, "player": json_loads(f.read()) }
        f.close()
        existed = True
    except:
        r = get("https://api.hypixel.net/v2/player", params={"name": username}, headers={"API-Key": os.getenv('HYPIXEL_API_KEY')})
        if not r.ok:
            print(r, r.text)
            return None
        else: result = r.json()

    if result['success']:
        if not existed:
            f = open("users/" + username + ".json", "w")
            f.write(json_dumps(result["player"]))
            f.close()

        result['player']['displayname'] = result['player']['displayname'] or (result['player']['knownAliases'] and (result['player']['knownAliases'][len(result['player']['knownAliases']) - 1])) or result['player']['playername'] or result['player']['username']
        result['player']['rank'] = get_player_rank(result['player'])
        result['player']['bedwarsLevel'] = get_bedwars_level_info(result['player'])
        return result['player']
    return None


async def get_igns_from_channel():
    return ["RedMiniontoby"]

    client = discord.Client(intents=discord.Intents.default())
    try:
        await client.login(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print(repr(e))
        return None

    try:
        channel = await client.fetch_channel(os.getenv('DISCORD_CHANNEL_ID'))
    except Exception as e:
        print(repr(e))
        channel = None

    if channel is None:
        await client.close()
        return None

    names = []
    discord_ids = []
    messages = reversed([message async for message in channel.history(limit=100)])
    for message in messages:
        if not message.author.bot and not message.author.id in discord_ids and len(message.content) > 0:
            names.append(message.content)
            discord_ids.append(message.author.id)

    await client.close()

    return names


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    player_data = get_player_data("RedMiniontoby")
    print(player_data['displayname'], '| Rank: ' + player_data['rank']['cleanName'], '| BW Level: ' + str(player_data['bedwarsLevel']['level']) + ' stars');

    #import asyncio
    #print(asyncio.run_until_complete(get_igns_from_channel()))
    

