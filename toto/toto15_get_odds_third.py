import sys 
sys.path.insert(0, '..')
sys.path.insert(0, '../../')
from selenium import webdriver
import time
import json
import data
from funcs import *

from dict_info import PATH




def login(main_url, browser):
    login = data.oddsportal_login
    password = data.oddsportal_password

    main_url_login = main_url + '/login/'
    browser.get(main_url_login)
    pause()

    log = browser.find_element_by_id('login-username1')
    log.click()
    log.send_keys(login)

    pas = browser.find_element_by_id('login-password1')
    pas.click()
    pas.send_keys(password)

    button_login2 = browser.find_elements_by_class_name('inline-btn-2')
    button_login2[2].click()
    pause()


def all_odds(basis, browser, num, word, recursion=False):
    container = browser.find_elements_by_class_name('table-container')
    if container:
        for i in container:
            text_split = i.text.split()
            key = 2 if text_split != [] and text_split[0] == 'Asian' else 1
            if text_split != [] and text_split[key] == basis and text_split[3] != 'Sets':
                one, two = '54' if key == 2 else '43'
                plus = 1 if text_split[1+key] == 'Games' else 0
                return float(text_split[int(one)+plus]), float(text_split[int(two)+plus])
    elif recursion:
        1/0
    else:
        browser.refresh()
        pause()
        all_odds(basis, browser, num, word, True)


def calc_odds(arr):
    over_perc = 1 / arr['over']
    under_perc = 1 / arr['under']
    first_handicap_perc = 1 / arr['first_handicap']
    second_handicap_perc = 1 / arr['second_handicap']

    total_diff = (1 - (over_perc + under_perc)) / 2
    handicap_diff = (1 - (first_handicap_perc + second_handicap_perc)) / 2

    over_wo_margin = over_perc + total_diff
    under_wo_margin = under_perc + total_diff
    first_handicap_wo_margin = first_handicap_perc + handicap_diff
    second_handicap_wo_margin = second_handicap_perc + handicap_diff

    hostsOver = over_wo_margin * first_handicap_wo_margin
    visitorsOver = over_wo_margin * second_handicap_wo_margin 
    hostsUnder = under_wo_margin * first_handicap_wo_margin
    visitorsUnder = under_wo_margin * second_handicap_wo_margin

    ret = {
        'kefs': {
            'over': arr['over'],
            'under': arr['under'],
            'first_handicap': arr['first_handicap'],
            'second_handicap': arr['second_handicap'],
        },
        'odds': {
            'hostsOver': hostsOver,
            'visitorsOver': visitorsOver,
            'hostsUnder': hostsUnder,
            'visitorsUnder': visitorsUnder,
        },
    }

    return ret


def get_match_odds(main_url, info_toto15f, browser):
    login(main_url, browser)
    count = len(info_toto15f['matches'])

    kefs = {i:{'over': 0, 'under': 0, 'first_handicap': 0, 'second_handicap': 0,
                'hostsOver': 0, 'visitorsOver': 0, 'hostsUnder': 0, 'visitorsUnder': 0} for i in range(count)}

    for i in range(count):
        print(i)
    
        total = '+' + str(info_toto15f['matches'][i]['totalBasis'])
        handicap = info_toto15f['matches'][i]['handicapBasis']
        handicap = '+' + str(handicap) if handicap > 0 else str(handicap)
        sport_key = '2' if info_toto15f['matches'][i]['sport'] == 'hockey' else '1'

        tmp = {'over': 0, 'under': 0, 'first_handicap': 0, 'second_handicap': 0}

        match_url = main_url + info_toto15f['matches'][i]['link'] + '#ah;' + sport_key
        browser.get(match_url)
        pause(2)

        tmp['first_handicap'], tmp['second_handicap'] = all_odds(handicap, browser, i, 'handicap')

        over_under = browser.find_element_by_css_selector('.ul-nav > li:nth-child(5) > a:nth-child(1)')
        over_under.click()
        pause(1)

        tmp['over'], tmp['under'] = all_odds(total, browser, i, 'total')

        kefs[i] = calc_odds(tmp)
        
    return kefs


# , site, num
def write_my_prob(toto_site, pools_number, info_toto15):
    print('write_my_prob')
    oddsportal = 'https://www.oddsportal.com'

    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('headless')
    browser = webdriver.Chrome(executable_path='../../selenium drivers/chromedriver')
                                    # options=driver_options)
    
    browser.implicitly_wait(10)
    kefs = get_match_odds(oddsportal, info_toto15, browser)
    browser.quit()
    
    with open(PATH['pinnacle_coefs'](toto_site, pools_number), 'w') as f:
        json.dump(kefs, f)
    

if __name__ == '__main__':
    with open('api.json') as f:
        info_toto15f = json.load(f)
        
    write_my_prob(info_toto15f)