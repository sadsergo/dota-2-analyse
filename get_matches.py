import json, time, os
import config
import requests


def download_matches():
    #!   match_id = 6671700940
    start_id = 6670054563   # 6661472400

    # Переменная с адресом сервера в интернете
    root_url = 'https://api.steampowered.com'
    endpoint = '/IDOTA2Match_570/GetMatchDetails/v1/'  # Ручка сервера
    url = root_url + endpoint  # Формируем ссылку без параметров
    api_key = config.STEAM_API_KEY

    for i in range(200000):
        query_params = {
            'key': api_key,
            'partner': 0,
            'match_id': i + start_id,
        }

        # Отправляем GET-запрос к Steam Web API
        response = requests.get(url, query_params)
        
        if response.ok:
            data = response.json()
            if not 'error' in data['result'].keys():
                print(f'GET: {i + start_id}')

                with open(os.getcwd() + '/matches/match_' + str(i + start_id) + '.json', 'w') as f:
                    json.dump(data, f, indent=4)
                    f.close()


def delete_wrong_matches():
    os.chdir('matches')

    for match in os.listdir():
        data = []
        
        with open(match, 'r') as f:
            data = json.load(f)
            f.close()

        if 'error' in data['result'].keys():
            os.remove(match)
    
    os.chdir('..')


def get_heroes_stats():
    root_url = 'https://api.steampowered.com'
    endpoint = '/IEconDOTA2_570/GetHeroes/v1'  # Ручка сервера
    url = root_url + endpoint  # Формируем ссылку без параметров
    api_key = config.STEAM_API_KEY
    query_params = {
        'key': api_key,
        'partner': 0,
        
    }

    response = requests.get(url, query_params)

    if response.ok:
        data = response.json()['result']['heroes']

        for i in range(len(data)):
            data[i]['name'] = data[i]['name'].replace('npc_dota_hero_', '')

        with open('hero_stats.json', 'w') as f:
            json.dump(data, f, indent=4)
            f.close()

download_matches()
#get_heroes_stats()