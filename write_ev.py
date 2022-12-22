import json

import sys
sys.path.insert(0, 'toto/')
sys.path.insert(0, 'toto/alredy set combs')
sys.path.insert(0, 'toto/write_ev')

import toto15_write_ev
import toto15
from dict_info import PATH


TOTO15_SITE = 'com'
POOLS_NUMBER = 846
STRATEGY = 15
BET_ID = 94514



with open(PATH['pinnacle_coefs'](TOTO15_SITE, POOLS_NUMBER)) as f:
    pinnacle_odds = json.load(f)

toto_api_info, _ = toto15.get_toto_api_info(TOTO15_SITE, POOLS_NUMBER)
pool = toto_api_info['combinations']




if __name__ == '__main__':
    toto15_write_ev.main_calc_mo()