import requests
import json
import gzip
import re
import binascii
import time
import sys
from pymongo import MongoClient

sys.path.insert(0, '../')
sys.path.insert(0, '../alredy set combs')
sys.path.insert(0, '../write_ev')

from payouts import payouts
from parse_set_combs import get_my_combs



MONGOCLIENT = MongoClient()
DATABASE = MONGOCLIENT['toto15']
COLLECTION = DATABASE['fun']


PATH = {
    'pinnacle_coefs': lambda site, num: f'../../{site}/files/finale_odds-{site}-{num}.json',
    'combinationsAll': lambda site, num: f'../../{site}/files/{site}-{num}.gz',
}




def get_toto_api_info(pool_number):
    url = f'https://api.thetoto.net/v1/pool/{pool_number}/all?real=true'
    toto_api = requests.get(url).json()
    return toto_api


def abbr(outcome):
    if outcome == 'hostsOver':
        return 'HO'
    elif outcome == 'visitorsOver':
        return 'VO'
    elif outcome == 'hostsUnder':
        return 'HU'
    elif outcome == 'visitorsUnder':
        return 'VU'
        

def calc_comb_result(comb, toto_api_info, my_falling_into_the_category):
    comb_split = comb.split(',')[:-1]
    winning_category = 0
    winning_category_3m = 0
    for index, i in enumerate(toto_api_info['matches']):
    
    
        winning_pick = abbr(i['winningPick']) == comb_split[index]
    

        special = i['special'] == 'true'

        if winning_pick:
            winning_category += 1
            if special:
                winning_category_3m += 1
                
    if winning_category == 0:
        my_falling_into_the_category[0] += 1
    elif winning_category >= 9:
        for i in range(9, winning_category+1):
            my_falling_into_the_category[i] += 1
            
    if winning_category_3m == 3:
        my_falling_into_the_category[3] += 1
        
    return my_falling_into_the_category


def write_results_main(site):
    # site = 'fun'

    for post in COLLECTION.find():
        num = post['num']
        bet_id = int(post['bet_id'])
        if post['return']: continue
        
        my_falling_into_the_category = {
            0: 0,
            3: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
        }
    
        toto_api_info = get_toto_api_info(num)
        if toto_api_info['status'] != 'archive': continue
        
        my_combs = get_my_combs(site, num, bet_id)

        for comb in my_combs:
            my_falling_into_the_category = calc_comb_result(comb, toto_api_info, 
                                                    my_falling_into_the_category)

        return_vager = payouts(num, my_falling_into_the_category)
    
        for i in [0, 3, *list(range(9, 16))]:
            update = {'$set': {str(i): {
                'expected_combs': post[str(i)]['expected_combs'],
                'fell_into_the_category': my_falling_into_the_category[i],
            }}}
            
            COLLECTION.update_one({'num': num}, update)
            
        update_return_vager = {'$set':{
            'return': return_vager - post['vager']
        }}
        
        COLLECTION.update_one({'num': num}, update_return_vager)
    
        print(num)
        time.sleep(10)


if __name__ == '__main__':
    main()