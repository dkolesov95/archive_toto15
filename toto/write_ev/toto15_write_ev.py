from statistics import mean
from scipy.stats import binom
import json
from multiprocessing import Pool
import time
import argparse

import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../alredy set combs')
sys.path.insert(0, '../com')

from parse_set_combs import get_my_combs, download_already_bets_combs
from generate_combs import abbr_rev
import toto15
import toto15_mongodb
from dict_info import TOTO_CATEGORY, SEND_TO_MONGODB, PATH 
from write_ev import TOTO15_SITE, POOLS_NUMBER, STRATEGY, BET_ID, pinnacle_odds, toto_api_info, pool



def main_calc_mo():
    print('main_calc_mo')
    
    download_already_bets_combs(TOTO15_SITE, POOLS_NUMBER)

    my_combs = get_my_combs(TOTO15_SITE, POOLS_NUMBER, BET_ID)

    p = Pool()
    s = time.time()
    mos = p.map(write_mo, my_combs)
    p.close()
    print('time', time.time() - s)

    for mo in mos:
        for index, i in enumerate(TOTO_CATEGORY):
            SEND_TO_MONGODB[i]['expected_combs'] += mo['fall_into_the_category'][index]

        SEND_TO_MONGODB['expected_value_sum'] += mo['expected_combs']

        for i in mo['aver_prob_info']:
            SEND_TO_MONGODB['aver_prob_info'][i] += mo['aver_prob_info'][i] / len(my_combs)
    
    SEND_TO_MONGODB['num'] = POOLS_NUMBER
    SEND_TO_MONGODB['bet_id'] = BET_ID
    SEND_TO_MONGODB['strategy'] = STRATEGY
    SEND_TO_MONGODB['vager'] = len(my_combs)
    
    toto15_mongodb.write_info(TOTO15_SITE, SEND_TO_MONGODB)


def write_mo(comb):
    real_prob = []
    toto_prob = []
    m3_real_prob = []
    m3_toto_prob = []
    for index, outcome in enumerate(comb.split(',')[:-1]):
        pp = pinnacle_odds[str(index)]['odds'][abbr_rev(outcome)]
        tp = toto_api_info['poolDistribution'][index][abbr_rev(outcome)]
        
        if toto_api_info['matches'][index]['special'] == 'true':
            m3_real_prob.append(pp)
            m3_toto_prob.append(tp)
        real_prob.append(pp)
        toto_prob.append(tp)
        
    mean_real_prob = mean(real_prob)
    mean_toto_prob = mean(toto_prob)
    mean_m3_real_prob = mean(m3_real_prob)
    mean_m3_toto_prob = mean(m3_toto_prob)
        
    mo = calc_combination_mo(pool, mean_toto_prob, mean_real_prob, 
                                mean_m3_toto_prob, mean_m3_real_prob)
    mo['aver_prob_info'] = {
        'toto15_prob': mean_toto_prob,
        'real_prob': mean_real_prob,
        'toto15_prob_3m': mean_m3_toto_prob,
        'real_prob_3m': mean_m3_real_prob,
    }
    return mo
    
    
def calc_combination_mo(pool, toto_prob, real_prob, 
                            m3_toto_prob, m3_real_prob):
    """
    Подсчет ожидания от комбинации
    """
    ret_dict = {}
    tmp_sum_ev = []
    fall_into_the_category = []
    for c in TOTO_CATEGORY:
        
        if c == '0':
            toto_prob_var = 1-toto_prob
            real_prob_var = 1-real_prob
        elif c == '3':
            toto_prob_var = m3_toto_prob
            real_prob_var = m3_real_prob
        else:
            toto_prob_var = toto_prob
            real_prob_var = real_prob
        
        g = TOTO_CATEGORY[c]['guess_matches']
        t = TOTO_CATEGORY[c]['total_matches']
        pd = TOTO_CATEGORY[c]['prize_distr']
        
        toto_prob_fall_into_z_cat = binom.pmf(g, t, toto_prob_var)
        real_prob_fall_into_z_cat = binom.pmf(g, t, real_prob_var)
        
        if c == '0':
            category_mo = calc_category_mo_0(pool, pd, toto_prob_fall_into_z_cat,
                                                real_prob_fall_into_z_cat)
        elif c == '15':
            category_mo = calc_category_mo_15(real_prob_fall_into_z_cat)
        else:
            category_mo = calc_category_mo(pool, pd, toto_prob_fall_into_z_cat,
                                            real_prob_fall_into_z_cat)

        prob = (real_prob_fall_into_z_cat if c != '0' 
                    else toto_prob_fall_into_z_cat)
        fall_into_the_category.append(prob)
        
        tmp_sum_ev.append(category_mo)
    
    r = {
        'fall_into_the_category': fall_into_the_category,
        'expected_combs': sum(tmp_sum_ev) - 1,
    }
    return r


def calc_category_mo(pool, prize_distr, toto_category_prob, 
                        real_category_prob):
    """
    Подсчет ожидания для категорий 3, 9, 10, 11, 12, 13, 14
    """
    category_prize = pool * prize_distr
    fall_into_z_category = pool * toto_category_prob
    coef = category_prize / fall_into_z_category
    mo = coef * real_category_prob  #- prize_distr
    return mo


def calc_category_mo_15(real_prob):
    """
    Подсчет ожидания для категории 15
    """
    return 5000000 * real_prob


def calc_category_mo_0(pool, prize_distr, toto_category_prob, 
                        real_category_prob):
    """
    Подсчет ожидания для категори 0
    """
    category_prize = pool * prize_distr
    fall_into_z_category = pool * real_category_prob
    coef = category_prize / fall_into_z_category
    mo = coef * toto_category_prob #- prize_distr
    return mo
