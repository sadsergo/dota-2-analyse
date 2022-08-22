
import get_player_stats
import json
import os


def getTeammatesWinRate(account_id, match_id=0):
    
    data = []
    
    if not match_id:
        #*  Get last match by account_id
        match = get_player_stats.get_player_matches(account_id, game_mode=0, match_requested=1)
        ids = [player['account_id'] for player in match['result']['matches'][0]['players']]

        for player in ids:
            data.append(get_player_stats.process_player_data(player, game_mode=0, match_requested=10))
    else:
        match = get_player_stats.get_match_details(match_id)
        ids = [player['account_id'] for player in match['result']['players']]
        
        for player in ids:
            data.append(get_player_stats.process_player_data(
                player, game_mode=0, match_requested=10))

    with open('data/winrate-teammates.json', 'w') as f:
        json.dump(data, f, indent=4)
        f.close()


getTeammatesWinRate(241992999, match_id=6714844231)
