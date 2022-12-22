PATH = {
    'pinnacle_coefs': lambda site, num: f'files/finale_odds-{site}-{num}.json',
    'combinationsAll': lambda site, num: f'files/{site}-{num}.gz',
}


def tmp_dict():
    r = {
        0: None,
        3: None,
        9: None,
        10: None,
        11: None,
        12: None,
        13: None,
        14: None,
        15: None,
        'expected_value_sum': None,
    }
    return r
    

SEND_TO_MONGODB = {
    '0': {
        'expected_combs': 0,
        'fell_into_the_category': None,
    }, '3': {
        'expected_combs': 0,
        'fell_into_the_category': None,
    }, '9': {
        'expected_combs': 0,
        'fell_into_the_category': None,
    }, '10': {
        'expected_combs': 0,
        'fell_into_the_category': None,
    }, '11': {
        'expected_combs': 0,
        'fell_into_the_category': None,
    }, '12': {
        'expected_combs': 0,
        'fell_into_the_category': None,
    }, '13': {
        'expected_combs': 0,
        'fell_into_the_category': None,
    }, '14': {
        'expected_combs': 0,
        'fell_into_the_category': None,
    }, '15': {
        'expected_combs': 0,
        'fell_into_the_category': None,
    }, 'aver_prob_info': {
        'toto15_prob': 0,
        'real_prob': 0,
        'toto15_prob_3m': 0,
        'real_prob_3m': 0,
    },
    'num': None,
    'bet_id': None,
    'strategy': None,
    'vager': 0,
    'expected_value_sum': 0,
    'return': None,
}


TOTO_CATEGORY = {
    '0': {
        'guess_matches': 15,
        'total_matches': 15,
        'prize_distr': 0.25,
    }, '3': {
        'guess_matches': 3,
        'total_matches': 3,
        'prize_distr': 0.15,
    }, '9': {
        'guess_matches': 9,
        'total_matches': 15,
        'prize_distr': 0.1,
    }, '10': {
        'guess_matches': 10,
        'total_matches': 15,
        'prize_distr': 0.1,
    }, '11': {
        'guess_matches': 11,
        'total_matches': 15,
        'prize_distr': 0.1,
    }, '12': {
        'guess_matches': 12,
        'total_matches': 15,
        'prize_distr': 0.1,
    }, '13': {
        'guess_matches': 13,
        'total_matches': 15,
        'prize_distr': 0.05,
    }, '14': {
        'guess_matches': 14,
        'total_matches': 15,
        'prize_distr': 0.05,
    }, '15': {
        'guess_matches': 15,
        'total_matches': 15,
        'prize_distr': 0,
    }
}