
import json


def show_most_hero_counter_picks(name):
    with open('backend/data_proc/data/win_rate.json', 'r') as f:
        hero_data = json.load(f)
        f.close()

    lose_rate = {}

    for hero in hero_data[name]:
        win_rate = float(hero_data[name][hero]) / (hero_data[name][hero] + hero_data[hero][name])
        if win_rate < 0.5:
            lose_rate[hero] = win_rate

    return lose_rate


def show_hero_best_pick(name):
    with open('backend/data_proc/data/win_rate.json', 'r') as f:
        hero_data = json.load(f)
        f.close()

    win_rate_list = {}

    for hero in hero_data[name]:
        win_rate = float(hero_data[name][hero]) / (hero_data[name][hero] + hero_data[hero][name])
        if win_rate > 0.55:
            win_rate_list[hero] = win_rate

    return win_rate_list


def get_win_rate_hero(hero, enemy = ''):
    with open('backend/data_proc/data/win_rate.json', 'r') as f:
        hero_data = json.load(f)
        f.close()

    if enemy == '':
        return hero_data[hero]

    return float(hero_data[hero][enemy]) / (hero_data[hero][enemy] + hero_data[enemy][hero])

hero, enemy = 'tiny', 'axe'
print('win rate ' + str(hero) + ' against ' + str(enemy) + ': ' + str(get_win_rate_hero(hero, enemy)))