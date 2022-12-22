import time

import sys

sys.path.insert(0, 'toto/')
sys.path.insert(0, 'toto/alredy_set_combs')

from selenium import webdriver
from selenium.webdriver.common.keys import Key

import funcs

import toto15
import toto15_get_odds_third
import parse_set_combs
import generate_combs
from parse_args import TOTO15_SITE, WRITE_COEFS



def main():

    toto_api_info, pools_number = toto15.get_toto_api_info(TOTO15_SITE)
    start_unixtime = toto_api_info['start'] / 1000
    
    if WRITE_COEFS in ['y']:
        funcs.put_pause(start_unixtime, 600)
        toto15_get_odds_third.write_my_prob(TOTO15_SITE, pools_number, 
                                                toto_api_info)
    
    funcs.put_pause(start_unixtime, 150)
    
    driver = webdriver.Firefox(executable_path='../../selenium drivers/geckodriver')
    toto15.toto_login(driver, TOTO15_SITE)
    money, pool = toto15.get_money_and_pool(driver, TOTO15_SITE)
    
    funcs.put_pause(start_unixtime, 90)
    
    already_set_combs = parse_set_combs.already_set_combs_main(TOTO15_SITE,
                                                                pools_number)

    bet_id = start_betting(driver, already_set_combs, money, 
                            TOTO15_SITE, pools_number)


def start_betting(driver, already_set_combs, money, toto_site, pools_number):
    print('start_betting')

    bet = driver.find_elements_by_class_name('tabs__link')
    bet[-1].click()

    data_pac = driver.find_elements_by_class_name('textarea')
    data_pac[0].click()
    
    plus_ev_combs = generate_combs.plus_ev_combs_main(toto_site, pools_number, 
                                                        already_set_combs)
    print('plus_ev_combs', len(plus_ev_combs))
    if len(plus_ev_combs) == 0: 1/0

    my_combs = '\n'.join(i[1] for i in plus_ev_combs[:money])
    driver.execute_script("""var my_combs = arguments[0]; 
                                document.getElementsByClassName
                                ('textarea')[0].value += my_combs;""", my_combs)
    
    time.sleep(1)
    data_pac[0].send_keys(Keys.CONTROL, 'a')
    data_pac[0].send_keys(Keys.CONTROL, 'c')
    data_pac[0].send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    
    button = driver.find_elements_by_class_name('btn_green')
    button[0].click()
    time.sleep(1)
    button2 = driver.find_elements_by_class_name('btn_green')
    button2[0].click()
    time.sleep(1)
    bet_id = driver.find_elements_by_class_name('modal__body')
    bet_id = bet_id[0].text.split()
    bet_id = bet_id[3]
    time.sleep(1)

    driver.quit()

    return bet_id


if __name__ == '__main__':
    main()