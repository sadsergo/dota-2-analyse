from ast import MatchSequence
import os, json
import pandas as pd
import dota2api
from config import STEAM_API_KEY
import matplotlib as plt
import matplotlib.pyplot as pp
import numpy as np


def collect_bans_picks():
    os.chdir('matches')
    matches = os.listdir()
    data = []

    for match in matches:
        teams_data = {}
        match_data = {}

        team_radiant_bans = []
        team_radiant_picks = []
        team_dire_bans = []
        team_dire_picks = []
        
        with open (match, 'r') as f:
            match_data = json.load(f)
            f.close()

        teams_data["match_id"] = match_data['result'].get('match_id')
        teams_data["radiant_win"] = match_data['result'].get('radiant_win')
        teams_data["duration"] = match_data['result'].get('duration')
        try:
            teams_data["first_team_ban"] = match_data['result'].get('picks_bans')[
                0]['team']
        except Exception as e:
            teams_data["first_team_ban"] = 0
        
        for i in range(12):
            try:
                if match_data['result']["picks_bans"][i]['team'] == 0:
                    team_radiant_bans.append(
                        match_data['result']["picks_bans"][i]["hero_id"])
                else:
                    team_dire_bans.append(
                        match_data['result']["picks_bans"][i]["hero_id"])
            except Exception as e:
                #teams_data[f"{i + 1}" + "_ban"] = 'Nope'
                continue

        for i in range(10):
            try:
                if match_data['result']["players"][i]['team_number'] == 0:
                    team_radiant_picks.append(
                        match_data['result']["players"][i]["hero_id"])
                else:
                    team_dire_picks.append(
                        match_data['result']["players"][i]["hero_id"])
            except Exception as e:
                print(e)
                continue
        teams_data['radiant_ban'] = team_radiant_bans
        teams_data['dire_ban'] = team_dire_bans
        teams_data['radiant_pick'] = team_radiant_picks
        teams_data['dire_pick'] = team_dire_picks

        data.append(teams_data)

    os.chdir("..")

    hero_data = []
    with open('hero_stats.json', 'r') as f:
        hero_data = json.load(f)
        f.close()

    for i in range(len(data)):
        if len(data[i]['radiant_ban']):
            for j in range(len(data[i]['radiant_ban'])):
                for z in range(len(hero_data)):
                    if hero_data[z]['id'] == data[i]['radiant_ban'][j]:
                        data[i]['radiant_ban'][j] = hero_data[z]['name']
                        break
        if len(data[i]['dire_ban']):
            for j in range(len(data[i]['dire_ban'])):
                for z in range(len(hero_data)):
                    if hero_data[z]['id'] == data[i]['dire_ban'][j]:
                        data[i]['dire_ban'][j] = hero_data[z]['name']
                        break

        for j in range(len(data[i]['radiant_pick'])):
            for z in range(len(hero_data)):
                if hero_data[z]['id'] == data[i]['radiant_pick'][j]:
                    data[i]['radiant_pick'][j] = hero_data[z]['name']
                    break
        for j in range(len(data[i]['dire_pick'])): 
            for z in range(len(hero_data)):
                if hero_data[z]['id'] == data[i]['dire_pick'][j]:
                    data[i]['dire_pick'][j] = hero_data[z]['name']
                    break          

    with open('pick_ban_info.json', 'w') as f:
        json.dump(data, f, indent=4)
        f.close()

    


def show_graph_ban():
    df = pd.read_json('pick_ban_info.json')
    df.to_csv('pick_ban_info.csv', encoding='utf-8', index=False)

    df = pd.read_csv('pick_ban_info.csv')

    #!  Show matches by their duration 
    # max_minutes = np.max(df["duration"]) / 60
    
    # df["minutes"] = df["duration"].apply(lambda x: x / 60)
    # grouply_minutes = df.groupby(['minutes']).count()
    

    # plt.hist(grouply_minutes.index, histtype='bar', color='green')
    # plt.show()

    #!  Show winrate to sides
    # base1 = df.loc[df['radiant_win'] == True]
    # base2 = df.loc[df['radiant_win'] == False]
    
    # temp_a = ['radiant', 'dire']
    # temp_b = [len(base1), len(base2)]
    
    # pp.bar(temp_a, temp_b)
    # pp.show()

    #! Show first ban
    # ban_1 = df['1_ban']
    # ban1_count = df.groupby(df['1_ban']).size()

    # #plt.rcParams['figure.figsize'] = 22.6
    # pp.xticks(rotation='vertical')
    # pp.grid()
    # pp.plot(ban1_count.index, ban1_count.values)
    # pp.show()

    #! Show all bans
    heroes_list = []
    heroes_dict = {}

    with open('hero_stats.json', 'r') as f:
        hero_data = json.load(f)
        
        for i in range(len(hero_data)):
            heroes_dict[hero_data[i]["id"]] = hero_data[i]["name"]
        
        f.close()

    for i, j in enumerate(heroes_dict):
        hero_name = heroes_dict[j]
        heroes_list.append(hero_name)

    total_ban = 12
    columns = ['1_ban', '2_ban', '3_ban', '4_ban', '5_ban',
               '6_ban', '7_ban', '8_ban', '9_ban', '10_ban', '11_ban', '12_ban']

    all_data = pd.DataFrame(columns=columns, index=heroes_list)
    all_data.sort_index()
    
    for i in range(total_ban):
        all_data[columns[i]] = df.groupby(df[columns[i]]).size()

    all_data = all_data.fillna(value=0)

    sum_all_data = all_data.sum(axis=1)
    
    pp.grid()
    pp.plot(sum_all_data.index, sum_all_data.values)
    pp.xticks(rotation='vertical')
    pp.yticks(np.arange(0, 350, 500))
    pp.show()


def show_graph_pick():
    df = pd.read_json('pick_ban_info.json')
    df.to_csv('pick_ban_info.csv', encoding='utf-8', index=False)

    df = pd.read_csv('pick_ban_info.csv')

    heroes_list = []
    heroes_dict = {}

    with open('hero_stats.json', 'r') as f:
        hero_data = json.load(f)

        for i in range(len(hero_data)):
            heroes_dict[hero_data[i]["id"]] = hero_data[i]["name"]

        f.close()

    for i, j in enumerate(heroes_dict):
        hero_name = heroes_dict[j]
        heroes_list.append(hero_name)

    total_pick = 10
    columns = ['1_pick', '2_pick', '3_pick', '4_pick', '5_pick',
               '6_pick', '7_pick', '8_pick', '9_pick', '10_pick']
    pick_all_data = pd.DataFrame(columns=columns, index=heroes_list)

    for i in range(total_pick):
        pick_all_data[columns[i]] = df.groupby(df[columns[i]]).size()

    pick_all_data = pick_all_data.fillna(0)

    sum_all_pick_data = pick_all_data.sum(axis=1)
    sum_all_pick_data.head(2)

    pp.grid()
    pp.plot(sum_all_pick_data.index, sum_all_pick_data.values)
    pp.xticks(rotation='vertical')
    pp.yticks(np.arange(0, 3000, 5000))
    pp.show()


def get_most_pop_hero():
    df = pd.read_json('pick_ban_info.json')
    df.to_csv('pick_ban_info.csv', encoding='utf-8', index=False)

    df = pd.read_csv('pick_ban_info.csv')

    #temp = df.loc(df[])


def calculate_wr_each_hero():
    matches = []
    win_rate = []

    with open('pick_ban_info.json', 'r') as f:
        matches = json.load(f)
        f.close()

    for match in matches:
        for i in range(1, 11):
            if not match['radiant_pick'][i] in win_rate.keys() or not match['dire_pick'][i] in win_rate.keys():
                win_rate[match['radiant_pick'][i]] = []
            else:
                win_rate[match['radiant_pick'][i]] += 1


collect_bans_picks()
#show_graph_ban()
#show_graph_pick()