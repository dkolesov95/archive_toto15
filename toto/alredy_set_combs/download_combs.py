import requests

import sys
sys.path.insert(0, '../')

from funcs import get_proxy_ua



def download_already_bets_combs():
    url = 'https://api.toto15.net/v1/combinationsAll/798'
    
    zip_file = requests.get(url)

    with open('already_bets.gz', 'wb') as f:
        f.write(zip_file.content)


if __name__ == "__main__":
    main()