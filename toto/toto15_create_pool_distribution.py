import json

import sys
sys.path.insert(0, 'alredy_set_combs')

from parse_set_combs import already_set_combs_main



def toto15_pool_distribution(toto_site, num_circ):
    all_combinations = already_set_combs_main(toto_site, num_circ)
    count_combinations = len(all_combinations)
    
    toto15_count_bets_on_outcomes = {i: {'HO': 0, 'VO': 0, 'HU': 0, 'VU': 0} 
                                        for i in range(15)}
    toto15_pool_distribution = {i: {'HO': 0, 'VO': 0, 'HU': 0, 'VU': 0} 
                                        for i in range(15)}

    for comb in all_combinations:
        for index, outcome in enumerate(comb.split(',')[:-1]):
            toto15_count_bets_on_outcomes[index][outcome] += 1

    with open('toto15_count_bets_on_outcomes.json', 'w') as f:
        json.dump(toto15_count_bets_on_outcomes, f)

    for m in toto15_count_bets_on_outcomes:
        for outcome in toto15_count_bets_on_outcomes[m]:
            count_bets_on_outcome = toto15_count_bets_on_outcomes[m][outcome]
            toto15_pool_distribution[int(m)][outcome] = (count_bets_on_outcome / 
                                                            count_combinations)

    return toto15_pool_distribution, count_combinations