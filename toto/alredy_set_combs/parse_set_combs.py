import gzip
import re
import binascii
import json
import requests
from multiprocessing import Pool
import time

import sys 
sys.path.insert(0, '../')
sys.path.insert(0, '../../')

from dict_info import PATH



def download_already_bets_combs(toto_site, pools_number):
    if toto_site == 'com':
        url = f'https://api.toto15.top/v1/combinationsAll/{pools_number}'
    elif toto_site == 'fun':
        url = f'https://api.thetoto.net/v1/combinationsAll/{pools_number}'
    
    zip_file = requests.get(url)

    with open(PATH['combinationsAll'](toto_site, pools_number), 'wb') as f:
        f.write(zip_file.content)


def binary_to_word(outcome):
    if outcome == '11':
        return 'HO,'
    elif outcome == '10':
        return 'HU,'
    elif outcome == '01':
        return 'VO,'
    elif outcome == '00':
        return 'VU,'


def binary_comb_to_normal_comb(binary_comb):
    x = ''
    for i in binary_comb:
        x += ''.join(binary_to_word(i[x:x+2]) for x in range(1, len(i), 2))
    return x


def convert_combs_one_player(info):

    split_line = info.split('\t')
    combs = split_line[-1]
    
    result = []
    
    all_combs_one_player = [format(ord(x), 'b') for x in combs]
    for z in range(0, len(all_combs_one_player), 5):
        one_comb = binary_comb_to_normal_comb(all_combs_one_player[z:z+5]) 
        result.append(one_comb)
    
    return result
    

def already_bets_combs_def(toto_site, pools_number):

    with gzip.open(PATH['combinationsAll'](toto_site, pools_number), 'rb') as f:
        open_file = f.read()
    
    open_file = open_file.decode('utf-8')

    split_file_data = re.split(r'#\s\n', open_file)
    split_each_line = split_file_data[-1].split('\n')

    set_combinations = set()
    for i in split_each_line[:len(split_each_line)-1]:
        split_line = i.split('\t')
        comb = split_line[-1]
        all_combs_one_player = [format(ord(x), 'b') for x in comb]
        for z in range(0, len(all_combs_one_player), 5):
            one_comb = binary_comb_to_normal_comb(all_combs_one_player[z:z+5]) 
            set_combinations.add(one_comb)
    return set_combinations


def already_set_combs_main(toto_site, pools_number):
    print('already_set_combs_main')

    download_already_bets_combs(toto_site, pools_number)
    r = already_bets_combs_def(toto_site, pools_number)
    return r
    
    
def get_my_combs(toto_site, pools_number, my_bet_id):

    with gzip.open(PATH['combinationsAll'](toto_site, pools_number), 'rb') as f:
        open_file = f.read()
    
    open_file = open_file.decode('utf-8')

    split_file_data = re.split(r'#\s\n', open_file)
    split_each_line = split_file_data[-1].split('\n')
    
    my_combs = []
    for i in split_each_line[:-1]:
        split_line = i.split('\t')
        bet_id = split_line[2]
        
        if bet_id == str(my_bet_id):
            multiply = int(split_line[3])
            comb = split_line[-1]
            all_combs_one_player = [format(ord(x), 'b') for x in comb]
            for z in range(0, len(all_combs_one_player), 5):
                one_comb = binary_comb_to_normal_comb(all_combs_one_player[z:z+5]) 
                one_comb_array = [one_comb] * multiply
                my_combs += one_comb_array
            return my_combs
    return []