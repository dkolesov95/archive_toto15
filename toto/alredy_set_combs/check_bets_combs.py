from read_combs import already_bets_combs_def



def other_combinations(number, my_bet_id):
    c = already_bets_combs_def(number, my_bet_id)
    with open('check bets combs dir/other_combs.txt', 'w') as f:
        for i in c:
            f.write(i+'\n')
