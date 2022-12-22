import json
import itertools
import time

from toto15 import get_toto_api_info
from dict_info import PATH
from parse_args import TOTO15_STRATEGY


TOTO15_MULTIPLY = '1|'
SORTED_REVERSE = True if TOTO15_STRATEGY == '15' else False



def abbr(outcome):
    if outcome == 'hostsOver':
        return 'HO'
    elif outcome == 'visitorsOver':
        return 'VO'
    elif outcome == 'hostsUnder':
        return 'HU'
    elif outcome == 'visitorsUnder':
        return 'VU'


def abbr_rev(outcome):
    if outcome == 'HO':
        return 'hostsOver'
    elif outcome == 'VO':
        return 'visitorsOver'
    elif outcome == 'HU':
        return 'hostsUnder'
    elif outcome == 'VU':
        return 'visitorsUnder'


def get_outcomes(pinnacle_odds, toto_api_info):
    """
    STRATAGY = 'jackpot', собирает 2(3) исхода с максимальной вероятностью
    STRATAGY = 'zero', собирает 2(3) исхода с минимальной вероятностью
    """
    event_outcomes = []
    for i in range(15):
        special_match = toto_api_info['matches'][i]['special']
        count_matches = 3 if special_match  == 'true' else 2
        match_distr = pinnacle_odds[str(i)]['odds']
        sort_match_distr = sorted(match_distr.items(), 
                                    key=lambda item: item[1], 
                                    reverse=SORTED_REVERSE)
        tmp = [abbr(sort_match_distr[i][0]) for i in range(count_matches)]
        event_outcomes.append(tmp)
        
    return event_outcomes


def calc_plus_combs(event_outcomes, pinnacle_odds, already_set_combs, toto_api_info):
    """
    combinations - генерациия всех возможных комбинаций
    """
    combinations = list(itertools.product(*event_outcomes))
    toto_pool_distr = toto_api_info['poolDistribution']
    
    ret_dict = {}
    for index, comb in enumerate(combinations):
        toto_distr_average = sum([toto_pool_distr[index][abbr_rev(i)] 
                                    for index, i in enumerate(comb)]) / 15
        pinnacle_odds_average = sum([pinnacle_odds[str(index)]['odds'][abbr_rev(i)] 
                                        for index, i in enumerate(comb)]) / 15
    
        if pinnacle_odds_average - toto_distr_average > 0.005:
            plus_ev_comb = TOTO15_MULTIPLY + ','.join(comb) + ','
            
            if plus_ev_comb not in already_set_combs:
                ret_dict[pinnacle_odds_average] = plus_ev_comb
    
    ret_dict = sorted(ret_dict.items(), key=lambda item: item[0],
                        reverse=SORTED_REVERSE)
    return ret_dict


def plus_ev_combs_main(toto_site, pools_number, already_set_combs):
    print('plus_ev_combs_main')

    with open(PATH['pinnacle_coefs'](toto_site, pools_number)) as f:
        pinnacle_odds = json.load(f)
    
    toto_api_info, _ = get_toto_api_info(toto_site)
    
    
    event_outcomes = get_outcomes(pinnacle_odds, toto_api_info)
    
    plus_ev_combs = calc_plus_combs(event_outcomes, pinnacle_odds, 
                                    already_set_combs, toto_api_info)
    
    return plus_ev_combs