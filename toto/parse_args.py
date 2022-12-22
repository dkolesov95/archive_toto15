import argparse

from toto15 import get_number_of_circulation


parser = argparse.ArgumentParser()
parser.add_argument('-ts', action='store', dest='site')
parser.add_argument('-s', action='store', dest='stratagy')
parser.add_argument('-wc', action='store', dest='write_coefs')
args = parser.parse_args()

TOTO15_SITE = args.site
TOTO15_STRATEGY = args.stratagy
WRITE_COEFS = args.write_coefs
print(TOTO15_SITE, TOTO15_STRATEGY, WRITE_COEFS)
