import requests
import time

import data



def toto15_api_urls(toto_site):
    if toto_site == 'com':
        urls = {
            'num_circ': 'https://api.toto15.top/v1/pools/open',
            'api': lambda x: f'https://api.toto15.top/v1/pool/{x}/all?real=true',
            'site': 'https://toto15.com/ru/members/bet/advanced',
        }
    elif toto_site == 'fun':
        urls = {
            'num_circ': 'https://api.thetoto.net/v1/pools/open',
            'api': lambda x: f'https://api.thetoto.net/v1/pool/{x}/all?real=true',
            'site': 'https://toto15.fun/ru/members/bet/advanced',
        }
    return urls


def get_number_of_circulation(toto_site):
    url = toto15_api_urls(toto_site)['num_circ']
    num = requests.get(url).json()
    return num[0] if num else None
    

def get_money_and_pool(driver, toto_site):
    money = driver.find_elements_by_class_name('m-wallet')
    money = money[0].text.split()
    money = int(float(money[0]) * 100)

    url = toto15_api_urls(toto_site)['site']
    driver.get(url)

    time.sleep(1)

    pool = driver.find_elements_by_class_name('draw__main')
    pool = pool[0].text.split()
    print(pool)
    
    return money, pool


def toto_login(driver, toto_site):
    if toto_site == 'fun':
        login = data.toto15_fun_login
        password = data.toto15_fun_password
    else:
        login = data.toto15_com_login
        password = data.toto15_com_password
    
    url1 = 'https://toto15.fun/ru/'
    driver.get(url1)
    time.sleep(5)
    input_toto15 = driver.find_elements_by_xpath('//input')
    input_toto15[0].click()
    input_toto15[0].send_keys(login)
    input_toto15[1].click()
    input_toto15[1].send_keys(password)
    submit = driver.find_elements_by_class_name('button')
    submit[0].click()
    time.sleep(3)
    
    
def get_toto_api_info(toto_site, pool_number=None):
    if not pool_number:
        pool_number = get_number_of_circulation(toto_site)
        if not pool_number:
            1/0

    url = toto15_api_urls(toto_site)['api'](pool_number)
    toto_api = requests.get(url).json()
    return toto_api, pool_number
    

   
if __name__ == '__main__':
    print(get_number_of_circulation('fun'), 'fun')
    print(get_number_of_circulation('com'), 'com')