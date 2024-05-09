import json
from textwrap import indent 
import requests
import config
import os
import time


def get_player_matches(account_id, game_mode, match_requested):
    root_url = 'https://api.steampowered.com'
    command_type = '/IDOTA2Match_570'
    command = '/GetMatchHistory/v1'

    url = root_url + command_type + command
    api_key = config.STEAM_API_KEY
    query_params = {
        'key': api_key,
        'partner': 0,
        'account_id': account_id,
        'matches_requested': match_requested,
        "game_mode": game_mode,
    }

    res = requests.get(url, query_params)

    if res.ok:
        data = res.json()

        # with open(os.getcwd() + '/data/playerStatsInMatches.json', 'w') as f:
        #     json.dump(data, f, indent=4)
        #     f.close()

        return data

    return None


def get_match_details(match_id):
    root_url = 'https://api.steampowered.com'
    command_type = '/IDOTA2Match_570'
    command = '/GetMatchDetails/v1'

    url = root_url + command_type + command
    api_key = config.STEAM_API_KEY
    query_params = {
        'key': api_key,
        'partner': 0,
        'match_id': match_id,
        'include_persona_names': 1,
    }

    res = requests.get(url, query_params)

    if res.ok:
        data = res.json()
        if not 'error' in data['result'].keys():

            # with open('match.json', 'w') as f:
            #     json.dump(data, f, indent=4)
            #     f.close()

            return data
    
    return None


def get_player_match_stats(match_id, account_id):
    match = get_match_details(match_id)
    player_stats = {
        "persona": '',
        "team_number": 0,
        "kills": 0,
        "deaths": 0,
        "assists": 0,
        "last_hits": 254,
        "denies": 0,
        "gold_per_min": 0,
        "xp_per_min": 0,
        "level": 0,
        "net_worth": 0,
        "hero_damage": 0,
        "tower_damage": 0,
        "hero_healing": 0,
        "gold_spent": 0,
        "scaled_hero_damage": 0,
        "scaled_tower_damage": 0,
        "scaled_hero_healing": 0,
    }

    if match is not None:
        for player in match['result']['players']:
            try:
                if player['account_id'] == account_id:
                    for stat in player_stats.keys():
                        player_stats[stat] = player[stat]
            except Exception as e:
                continue

        #!print(player_stats)

        player_stats['win'] = 1 if (not player_stats['team_number'] and match['result']['radiant_win']
                                    or player_stats['team_number'] and not match['result']['radiant_win']) else 0
        # print('match:', match['result']['match_id'], 'team_number', player_stats['team_number'], 'radiant_win:',
        #       match['result']['radiant_win'], 'win:', player_stats['win'])

        return player_stats

    return None


def process_player_data(account_id, game_mode, match_requested):
    data = get_player_matches(account_id, game_mode, match_requested)
    name = ''
    middle_stats = {
        "win": 0,
        "team_number": 0,
        "kills": 0,
        "deaths": 0,
        "assists": 0,
        "last_hits": 254,
        "denies": 0,
        "gold_per_min": 0,
        "xp_per_min": 0,
        "level": 0,
        "net_worth": 0,
        "hero_damage": 0,
        "tower_damage": 0,
        "hero_healing": 0,
        "gold_spent": 0,
        "scaled_hero_damage": 0,
        "scaled_tower_damage": 0,
        "scaled_hero_healing": 0,
    }

    if data is not None and 'matches' in data['result'].keys():
        for match in data['result']['matches']:
            #!print(match['match_id'])
            match_stats = get_player_match_stats(match['match_id'], account_id)
                
            if match is not None:
                name = match_stats['persona']
                del match_stats['persona']
                for stat in match_stats.keys():
                    middle_stats[stat] += match_stats[stat]
            
        for stat in middle_stats.keys():
            middle_stats[stat] /= len(data['result']['matches'])
            
        middle_stats['team_number'] = 1 - middle_stats['team_number']
        middle_stats['matches'] = len(data['result']['matches'])
        middle_stats['radiant'] = middle_stats['team_number']
        middle_stats['name'] = name
        middle_stats['account_id'] = account_id
        
        del middle_stats['team_number']
        
        return middle_stats

    return None


def GetMatchHistoryBySequenceNum():
    root_url = 'https://api.steampowered.com'
    command_type = '/IDOTA2Match_205790'
    command = '/GetMatchHistory/v1'

    url = root_url + command_type + command
    api_key = config.STEAM_API_KEY
    query_params = {
        'key': api_key,
        'partner': 0,
        'game_mode': 0,
    }

    res = requests.get(url, query_params)

    if res.ok:
        data = res.json()
        for match in data['result']['matches']:
            print(match['match_id'])


def show_player_stats(steam_id):
    # account_id = 178749178  # 241992999  # 178749178
    game_mode = 0
    match_requested = 10

    data = process_player_data(steam_id, game_mode, match_requested)

    if data is not None:
        with open(os.getcwd() + '/data/player_' + str(steam_id) + '.json', encoding='utf-8', mode='w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.close()


# GetMatchHistoryBySequenceNum()
# show_player_stats(178749178)
