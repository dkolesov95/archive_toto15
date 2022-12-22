import gzip
import re
from multiprocessing import Pool


import sys 
sys.path.insert(0, '../')
sys.path.insert(0, '../../')

from dict_info import PATH



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


def write_combs(split_line):

    split_line = split_line.split('\t')
    comb = split_line[-1]
    all_combs_one_player = [format(ord(x), 'b') for x in comb]
    for z in range(0, len(all_combs_one_player), 5):
        one_comb = binary_comb_to_normal_comb(all_combs_one_player[z:z+5]) 
    

def already_bets_combs_def():

    with gzip.open(PATH['combinationsAll'](TOTO15_SITE, POOLS_NUMBER), 'rb') as f:
        open_file = f.read()
    
    open_file = open_file.decode('utf-8')

    split_file_data = re.split(r'#\s\n', open_file)
    split_each_line = split_file_data[-1].split('\n')[:-1]

    p = Pool()
    p.map(write_combs, split_each_line)
    
    
if __name__ == '__main__':
    already_bets_combs_def()