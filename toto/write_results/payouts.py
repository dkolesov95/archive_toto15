import json
import requests

site = 'com'


REAL_CATEGORY = {
    0: 8,
    1: 9,
    2: 10,
    3: 11,
    4: 12,
    5: 13,
    6: 14,
    7: 15,
    8: 3,
    9: 0,
}

PRIZES_CATEGORY = {
    8: 0,
    9: 1,
    10: 2,
    11: 3,
    12: 4,
    13: 5,
    14: 6,
    15: 7,
    3: 8,
    0: 9,
}

TOTO_SHARES = {
    9: 0.1,
    10: 0.1,
    11: 0.1,
    12: 0.1,
    13: 0.05,
    14: 0.05,
    15: 0,
    0: 0.25,
    3: 0.15,
}


def coefs(bets_info, my_falling_into_the_category):
    real_shares = {
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
        0: 0.25,
        3: 0.15,
    }
    for index, i in enumerate(bets_info['prizes'][1:8]):
        if i == 0 and my_falling_into_the_category[index+9] == 0:
            real_shares[3] += TOTO_SHARES[index+9]
        else:
            real_shares[REAL_CATEGORY[index+1]] = TOTO_SHARES[index+9]

    combinations = bets_info['combinations']
    coefs_dict = {}
    for c in real_shares:
        money_for_deal = combinations * real_shares[c]
        if bets_info['prizes'][PRIZES_CATEGORY[c]]:
            coefs = money_for_deal / bets_info['prizes'][PRIZES_CATEGORY[c]]
            coefs_dict[c] = coefs
        else:
            coefs_dict[c] = 0
        
    return coefs_dict


def toto_bets_info(num):
    url = f'https://api.thetoto.net/v1/betsInfo/{num}'
    toto_bets_info = requests.get(url).json()
    return toto_bets_info


def payouts(num, my_falling_into_the_category):

    bets_info = toto_bets_info(num)
    
    coefs_dict = coefs(bets_info, my_falling_into_the_category)
    
    return_vager = sum([coefs_dict[c]*my_falling_into_the_category[c]  
                    for c in coefs_dict])
    
    return round(return_vager)