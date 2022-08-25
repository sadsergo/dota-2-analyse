
import os
import json
import operator
import collections


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
                

def getWinRateStats():
    data = []
    with open('data/hero_win_matches.json', 'r') as f:
        data = json.load(f)
        f.close()

    return data


def calculateHeroWinRate(hero, enemy=''):
    data = getWinRateStats()

    if enemy == '':
        all_matches = 0
        win_matches = 0

        for opponent in data[hero].keys():
            win_matches += data[hero][opponent]
            all_matches += data[hero][opponent] + data[opponent][hero]
        
        return round(float(win_matches) / all_matches, 2)

    else:
        return round(float(data[hero][enemy]) / (data[hero][enemy] + data[enemy][hero]), 2)


def createHeroWin_LoseRateFiles():
    data = getWinRateStats()
    winRate = {}

    for hero in data:
        winRate[hero] = {}

        for enemy in data[hero]:
            winRate[hero][enemy] = calculateHeroWinRate(hero, enemy)

    with open('data/win_rate.json', 'w') as f:
        json.dump(winRate, f, indent=4)
        f.close()


def sortWinRate():
    winRate = []
    with open('data/win_rate.json', 'r') as f:
        winRate = json.load(f)
        f.close()
    
    sorted_winRate = {}
    for hero in winRate:
        sorted_heroWinRate = sorted(winRate[hero].items(), key=operator.itemgetter(1))
        sorted_heroWinRate = collections.OrderedDict(sorted_heroWinRate)
        sorted_winRate[hero] = sorted_heroWinRate

        # for i in range(len(sorted_heroWinRate) - 1, -1, -1):
        #     sorted_winRate[hero][sorted_heroWinRate[i][0]] = sorted_heroWinRate[i][1]

    with open('data/sorted_win_rate.json', 'w') as f:
        json.dump(sorted_winRate, f, indent=4)
        f.close()


def createHeroesMatchWinRateFile():
    heroes = []

    with open('data/hero_stats.json', 'r') as f:
        heroes = json.load(f)
        f.close()

    heroesWinRate = {}

    for hero in heroes:
        heroesWinRate[hero['name']] = calculateHeroWinRate(hero['name'])

    heroesWinRate = sorted(heroesWinRate.items(), key=operator.itemgetter(1))
    heroesWinRate = collections.OrderedDict(heroesWinRate)

    with open('data/heroes_winrate.json', 'w') as f:
        json.dump(heroesWinRate, f, indent=4)
        f.close()  


def suggestPick(enemy):
    data = {}
    with open('data/sorted_win_rate.json', 'r') as f:
        data = json.load(f)
        f.close()

    print(f'Suggest pick against {enemy}:')
    
    count = 0
    for hero in reversed(data[enemy].keys()):
        if count < 10:
            print(f'\t{hero}: {data[enemy][hero]}')
            count += 1
        else:
            break


def suggestBan(hero):
    data = {}
    with open('data/sorted_win_rate.json', 'r') as f:
        data = json.load(f)
        f.close()

    print(f'Suggest ban against {hero}:')

    count = 0
    for enemy in data[hero].keys():
        if count < 10:
            print(f'\t{enemy}: {data[hero][enemy]}')
            count += 1
        else:
            break


#createHeroWin_LoseRateFiles()
# sortWinRate()
# createHeroesMatchWinRateFile()

name = 'tiny'
suggestPick(name)
suggestBan(name)
