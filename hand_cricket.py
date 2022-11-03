import random

# general format of game_detail :
# game_detail = { 'no_of_wickets':10, 'no_of_overs':10, 'teamA':'6/4/5.4', 'teamB':'0/0/0.0', 'scorecard':{ 'teamA':{'player1':'30/20/not_out////4.0/24','player2':'40/15'}, 'teamB':{} } }
# considering teamA always bats first and teamB chases                                                                        'run/ball/not_out////over/run/wicket'

def total_no_of_balls(over):
    over = float(over)
    gif_over = over//1
    frac_over = over - gif_over
    no_of_balls = 6*gif_over + 10*frac_over
    return no_of_balls
    
def update_over(over, add_ball = 0):
    over = float(over) # Like over = 5.4
    gif_over = over//1 # It would give 5
    frac_over = over - gif_over # It would give 0.4
    if round(frac_over, 1) == 0.6:
        over = gif_over + 1 + 0.0 # We now here converted 2.6 to 3.0   
    over += add_ball/10 # Now adding the required balls
    gif_over = over//1 # Now the same logic as above
    frac_over = over - gif_over
    if round(frac_over, 1) == 0.6:
        over = gif_over + 1 + 0.0
    return round(over,1)

def update_scorecard_of_player(scorecard, bat_run_add, ball_add, status_bat, over_add, ball_run_add, wicket_add): # not for the over but for the scorecard
    # 'run/ball////over/run'
    s = scorecard.split('////')
    x1 = s[0].split('/')
    x2 = s[1].split('/')
    
    if bat_run_add is None:
        bat_run = int(x1[0])
    else:
        bat_run = int(x1[0]) + int(bat_run_add)
        
    if ball_add is None:
        bat_ball = int(x1[1])
    else:
        bat_ball = int(x1[1]) + int(ball_add)
        
    if status_bat is None:
        bat_status = str(x1[2])
    else:
        bat_status = status_bat
        
    if over_add is None:
        ball_over_add = float(x2[0])
    else:
        ball_over_add = update_over(float(x2[0]), int(over_add))

    if ball_run_add is None:
        ball_run_add = int(x2[1])
    else:
        ball_run_add = int(x2[1]) + int(ball_run_add)
        
    if wicket_add is None:
        ball_wicket_add = int(x2[2])
    else:
        ball_wicket_add = int(x2[2]) + int(wicket_add)

    return (str(bat_run) + "/" + str(bat_ball) + '/' + bat_status + "////" + str(ball_over_add) + "/" + str(ball_run_add) + '/' + str(ball_wicket_add))

def max_over_per_player(game_detail, no_of_players):
    return (int(game_detail['no_of_overs'])/int(no_of_players))

def check_out_no_status(scorecard):
    # 'run/ball////over/run'
    s = scorecard.split('////')
    x1 = s[0].split('/')
    return int(x1[1])

def check_status(scorecard):
    # 'run/ball////over/run'
    s = scorecard.split('////')
    x1 = s[0].split('/')
    return str(x1[2])

def check_bowl_overs(scorecard):
    # 'run/ball////over/run'
    s = scorecard.split('////')
    x2 = s[1].split('/')
    return float(x2[0])
    
def teamA_innings_end(game_detail):
    s = game_detail['teamA'].split('/')
    # splitting scoreboard ko get runs wicket and over respectively
    wicket = int(s[1])
    over = float(s[2])
    if wicket < game_detail['no_of_wickets'] and over < game_detail['no_of_overs']:
        return False
    else:
        if wicket > game_detail['no_of_wickets'] or over > game_detail['no_of_overs']:
            return "Wickets or Overs max limit exceeded!"
        return True
    
def teamB_innings_end(game_detail):
    x = game_detail['teamA'].split('/')
    s = game_detail['teamB'].split('/')
    # splitting scoreboard to get runs wicket and over respectively
    scoreA = int(x[0])
    scoreB = int(s[0])
    wicket = int(s[1])
    over = float(s[2])
    if wicket < game_detail['no_of_wickets'] and over < game_detail['no_of_overs'] and scoreB < (scoreA + 1):
        return False
    else:
        if wicket > game_detail['no_of_wickets'] or over > game_detail['no_of_overs']:
            return "Wickets or Overs max limit exceeded!"
        return True

def available_batsman(game_detail, teamA_players, teamB_players):
    x = len(teamA_players)
    y = len(teamB_players)
    if x != y :
        return 'Both team do not have equal players!'
    li = []
    if teamA_innings_end(game_detail) == False:
        for i in game_detail['scorecard']['teamA']:
            if check_out_no_status(game_detail['scorecard']['teamA'][i]) < int((int(game_detail['no_of_wickets']))/x):
                li.append(i)
    else:
        for i in game_detail['scorecard']['teamB']:
            if check_out_no_status(game_detail['scorecard']['teamB'][i]) < int((int(game_detail['no_of_wickets']))/x):
                li.append(i)
    return li

def available_bowler(game_detail, teamA_players, teamB_players):
    x = len(teamA_players)
    y = len(teamB_players)
    if x != y :
        return 'Both team do not have equal players!'
    li = []
    if teamA_innings_end(game_detail) == False:
        for i in game_detail['scorecard']['teamB']:
            if check_bowl_overs(game_detail['scorecard']['teamB'][i]) < max_over_per_player(game_detail, no_of_players = x):
                li.append(i)
    else:
        for i in game_detail['scorecard']['teamA']:
            if check_bowl_overs(game_detail['scorecard']['teamA'][i]) < max_over_per_player(game_detail, no_of_players = x):
                li.append(i)
    return li

def decide_overchange(game_detail):
    if teamA_innings_end(game_detail) == True:
        s = game_detail['teamB']
        s1 = s.split('/')
        over = float(s1[2])
        over = float(over) # Like over = 5.4
        gif_over = over//1 # It would give 5
        frac_over = over - gif_over # It would give 0.4
        if frac_over == 0:
            return True
        else:
            return False
    else:
        s = game_detail['teamA']
        s1 = s.split('/')
        over = float(s1[2])
        over = float(over) # Like over = 5.4
        gif_over = over//1 # It would give 5
        frac_over = over - gif_over # It would give 0.4
        if frac_over == 0:
            return True
        else:
            return False
    
def teamA_runrate(game_detail):
    s = game_detail['teamA'].split('/')
    score = int(s[0])
    over = float(s[2])
    no_of_balls = total_no_of_balls(over)
    if score == 0 and no_of_balls == 0:
        return 0.00
    # Calculating total balls played
    runs_per_ball = 6 * score / no_of_balls
    # Run rate is calculated as total runs in a over or 6 * avergae run per ball
    return round(runs_per_ball, 2)

def teamB_runrate(game_detail):
    s = game_detail['teamB'].split('/')
    score = int(s[0])
    over = float(s[2])
    no_of_balls = total_no_of_balls(over)
    if score == 0 and no_of_balls == 0:
        return 0.00
    # Calculating total balls played
    runs_per_ball = 6 * score / no_of_balls
    # Run rate is calculated as total runs in a over or 6 * avergae run per ball
    return round(runs_per_ball, 2)

def required_run_ball(game_detail):
    if teamA_innings_end(game_detail) == True:
        x = game_detail['teamA'].split('/')
        s = game_detail['teamB'].split('/')
        # splitting scoreboard to get runs wicket and over respectively
        scoreA = int(x[0])
        scoreB = int(s[0])
        over = float(s[2])
        no_of_balls_left = total_no_of_balls(game_detail['no_of_overs']) - total_no_of_balls(over)
        # Calculating total balls played
        d = {}
        d['runs'] = scoreA - scoreB + 1
        d['balls'] = no_of_balls_left
        return d
    else:
        return "teamA is currently playing cannot calculate required runrate"

def required_run_rate(game_detail):
    # Returns error if innings of team A is not completed
    if teamA_innings_end(game_detail) == True:
        x = game_detail['teamA'].split('/')
        s = game_detail['teamB'].split('/')
        # splitting scoreboard to get runs wicket and over respectively
        scoreA = int(x[0])
        scoreB = int(s[0])
        over = float(s[2])
        no_of_balls_left = total_no_of_balls(game_detail['no_of_overs']) - total_no_of_balls(over)
        # Calculating total balls played
        runs_per_ball = 6 * (scoreA - scoreB + 1) / no_of_balls_left
        # Run rate is calculated as total runs in a over or 6 * avergae run per ball
        return round(runs_per_ball, 2)
    else:
        return "teamA is currently playing cannot calculate required runrate"

def check_match_end(game_detail):
    if teamA_innings_end(game_detail) == True and teamB_innings_end(game_detail) == True:
        return True
    return False
    
def generate_result(game_detail, teamA = 'teamA', teamB = 'teamB'): # teamA and teamB are the names of the teams. If there are no name then it would consider as teamA and teamB
    s = game_detail['teamA'].split('/')
    # splitting scoreboard to get runs wicket and over respectively
    scoreA = int(s[0])
    wicketA = int(s[1])
    overA = float(s[2])
    s = game_detail['teamB'].split('/')
    # splitting scoreboard to get runs wicket and over respectively
    scoreB = int(s[0])
    wicketB = int(s[1])
    overB = float(s[2])
    if scoreB > scoreA:
        res = {}
        res['result'] = 'game_end'
        res['game_end'] = True
        res['game_detail'] = game_detail
        res['scoreA'] = scoreA
        res['wicketA'] = wicketA
        res['overA'] = overA
        res['run_rateA'] = teamA_runrate(game_detail)
        res['scoreB'] = scoreB
        res['wicketB'] = wicketB
        res['overB'] = overA
        res['run_rateB'] = teamB_runrate(game_detail)
        res['winner'] = (str(teamB).strip()).capitalize()
        res['winner_by_team'] = 'teamB'
        res['win_by'] = game_detail['no_of_wickets']-wicketB
        res['scoreboardA'] = res['game_detail']['scorecard']['teamA']
        res['scoreboardB'] = res['game_detail']['scorecard']['teamB']
        return res
    elif scoreB < scoreA:
        res = {}
        res['result'] = 'game_end'
        res['game_end'] = True
        res['game_detail'] = game_detail
        res['scoreA'] = scoreA
        res['wicketA'] = wicketA
        res['overA'] = overA
        res['run_rateA'] = teamA_runrate(game_detail)
        res['scoreB'] = scoreB
        res['wicketB'] = wicketB
        res['overB'] = overB
        res['run_rateB'] = teamB_runrate(game_detail)
        res['winner'] = (str(teamA).strip()).capitalize()
        res['winner_by_team'] = 'teamA'
        res['win_by'] = str(scoreA - scoreB)
        res['scoreboardA'] = res['game_detail']['scorecard']['teamA']
        res['scoreboardB'] = res['game_detail']['scorecard']['teamB']
        return res
    elif scoreB == scoreA:
        res = {}
        res['result'] = 'game_end'
        res['game_end'] = True
        res['game_detail'] = game_detail
        res['scoreA'] = scoreA
        res['wicketA'] = wicketA
        res['overA'] = overA
        res['run_rateA'] = teamA_runrate(game_detail)
        res['scoreB'] = scoreB
        res['wicketB'] = wicketB
        res['overB'] = overB
        res['run_rateB'] = teamB_runrate(game_detail)
        res['winner'] = 'draw'
        res['winner_by_team'] = 'draw'
        res['win_by'] = 'Nill'
        res['scoreboardA'] = res['game_detail']['scorecard']['teamA']
        res['scoreboardB'] = res['game_detail']['scorecard']['teamB']
        return res
    
def init(game_detail, batsman_no, baller_no, current_batsman, current_bowler, teamA_players, teamB_players, teamA = 'teamA', teamB = 'teamB'):
    
    if teamA_innings_end(game_detail) == False:
        teamA_no = batsman_no
        teamB_no = baller_no
    else:
        teamB_no = batsman_no
        teamA_no = baller_no
        
    if game_detail['scorecard']['teamA'] == {}:
        for i in teamA_players:
            game_detail['scorecard']['teamA'][i] = '0/0/yet_to_play////0/0/0'
            
    if game_detail['scorecard']['teamB'] == {}:
        for i in teamB_players:
            game_detail['scorecard']['teamB'][i] = '0/0/yet_to_play////0/0/0'
            
    if teamA_innings_end(game_detail) == False:
        # teamA is batting and teamB is balling
        s = game_detail['teamA'].split('/')
        # splitting scoreboard to get runs wicket and over respectively
        scoreA = int(s[0])
        wicket = int(s[1])
        over = float(s[2])
        if teamA_no == teamB_no:
            # player is out
            game_detail['teamA'] = (str(scoreA) + "/" + str(wicket + 1) + "/" + str(update_over(over, add_ball = 1)))
            s = game_detail['teamA'].split('/')
            # splitting scoreboard to get runs wicket and over respectively
            wicket = int(s[1])
            over = float(s[2])
            if teamA_innings_end(game_detail) == True: # now again checking whether after the wicket innings has ended or not
                game_detail['scorecard']['teamA'][current_batsman] = update_scorecard_of_player(game_detail['scorecard']['teamA'][current_batsman],0,1,'out',None,None,None)   # add one extra ball to scorecard of the player as the player played this ball and got out
                game_detail['scorecard']['teamB'][current_bowler] = update_scorecard_of_player(game_detail['scorecard']['teamB'][current_bowler],None,None,None,1,0,1) # add one wicket to the baller
                res = {}
                res['game_end'] = False
                res['game_detail'] = game_detail
                res['innings_end'] = True
                res['innings'] = 'teamB'
                res['result'] = "end of innings"
                res['over_change'] = decide_overchange(game_detail)
                res['available_batsman'] = teamB_players
                res['available_bowler'] = teamA_players
                res['run_req'] = scoreA + 1
                res['scoreA'] = scoreA
                res['wicketA'] = wicket
                res['overA'] = over
                res['run_rateA'] = teamA_runrate(game_detail)
                res['scoreB'] = 0
                res['wicketB'] = 0
                res['overB'] = 0.0
                res['run_rateB'] = 0.00
                res['req_run_inball'] = required_run_ball(game_detail)
                res['req_run_rate'] = required_run_rate(game_detail)
                res['numberA'] = teamA_no
                res['numberB'] = teamB_no
                return res
            else:
                game_detail['scorecard']['teamA'][current_batsman] = update_scorecard_of_player(game_detail['scorecard']['teamA'][current_batsman],0,1,'out',None,None,None)   # add one extra ball to scorecard of the player as the player played this ball and got out
                game_detail['scorecard']['teamB'][current_bowler] = update_scorecard_of_player(game_detail['scorecard']['teamB'][current_bowler],None,None,None,1,0,1)   # add one wicket to the baller
                res = {}
                res['game_end'] = False
                res['game_detail'] = game_detail
                res['innings_end'] = False
                res['innings'] = 'teamA'                  # if innings_end is False then only innings will generate
                res['result'] = "new batsman"             # innings means who is currently batting
                res['over_change'] = decide_overchange(game_detail)
                res['available_batsman'] = available_batsman(game_detail, teamA_players, teamB_players)
                res['available_bowler'] = available_bowler(game_detail, teamA_players, teamB_players)
                res['run_req'] = None
                res['scoreA'] = scoreA
                res['wicketA'] = wicket
                res['overA'] = over
                res['run_rateA'] = teamA_runrate(game_detail)
                res['scoreB'] = None
                res['wicketB'] = None
                res['overB'] = None
                res['run_rateB'] = None
                res['req_run_inball'] = None
                res['req_run_rate'] = None
                res['numberA'] = teamA_no
                res['numberB'] = teamB_no
                return res
        else:
            game_detail['teamA'] = (str(scoreA + teamA_no) + "/" + str(wicket) + "/" + str(update_over(over, add_ball = 1)))
            s = game_detail['teamA'].split('/')
            game_detail['scorecard']['teamA'][current_batsman] = update_scorecard_of_player(game_detail['scorecard']['teamA'][current_batsman],teamA_no,0,'not_out',None,None,None)   
            game_detail['scorecard']['teamB'][current_bowler] = update_scorecard_of_player(game_detail['scorecard']['teamB'][current_bowler],None,None,None,1,teamA_no,0)
            # splitting scoreboard to get runs wicket and over respectively
            scoreA = int(s[0])
            wicket = int(s[1])
            over = float(s[2])
            res = {}
            res['game_end'] = False
            res['game_detail'] = game_detail
            res['innings_end'] = False
            res['innings'] = 'teamA'
            res['result'] = "score increase"
            res['over_change'] = decide_overchange(game_detail)
            res['available_batsman'] = available_batsman(game_detail, teamA_players, teamB_players)
            res['available_bowler'] = available_bowler(game_detail, teamA_players, teamB_players)
            res['run_req'] = None
            res['scoreA'] = scoreA
            res['wicketA'] = wicket
            res['overA'] = over
            res['run_rateA'] = teamA_runrate(game_detail)
            res['scoreB'] = None
            res['wicketB'] = None
            res['overB'] = None
            res['run_rateB'] = None
            res['req_run_inball'] = None
            res['req_run_rate'] = None
            res['numberA'] = teamA_no
            res['numberB'] = teamB_no
            return res
        
    elif teamB_innings_end(game_detail) == False:
        # teamB is batting now and teamA is balling
        s = game_detail['teamA'].split('/')
        # splitting scoreboard to get runs wicket and over respectively
        scoreA = int(s[0])
        wicketA = int(s[1])
        overA = float(s[2])
        
        s = game_detail['teamB'].split('/')
        scoreB = int(s[0])
        wicket = int(s[1])
        over = float(s[2])
        
        if teamA_no == teamB_no:
            # player is out
            game_detail['teamB'] = (str(scoreB) + "/" + str(wicket + 1) + "/" + str(update_over(over, add_ball = 1)))
            s = game_detail['teamB'].split('/')
            # splitting scoreboard to get runs wicket and over respectively
            wicket = int(s[1])
            over = float(s[2])
            if teamB_innings_end(game_detail) == True: # now again checking whether after the wicket innings has ended or not
                game_detail['scorecard']['teamB'][current_batsman] = update_scorecard_of_player(game_detail['scorecard']['teamB'][current_batsman],0,1,'out',None,None,None)   # add one extra ball to scorecard of the player as the player played this ball and got out
                game_detail['scorecard']['teamA'][current_bowler] = update_scorecard_of_player(game_detail['scorecard']['teamA'][current_bowler],None,None,None,1,0,1) # add one wicket to the baller
                res = generate_result(game_detail, teamA, teamB) # generating final results
                return res
            else:
                game_detail['scorecard']['teamB'][current_batsman] = update_scorecard_of_player(game_detail['scorecard']['teamB'][current_batsman],0,1,'out',None,None,None)   # add one extra ball to scorecard of the player as the player played this ball and got out
                game_detail['scorecard']['teamA'][current_bowler] = update_scorecard_of_player(game_detail['scorecard']['teamA'][current_bowler],None,None,None,1,0,1)
                res = {}
                res['game_end'] = False
                res['game_detail'] = game_detail
                res['innings_end'] = False
                res['innings'] = 'teamB'                  # if innings_end is False then only innings will generate
                res['result'] = "new batsman"             # innings means who is currently batting
                res['over_change'] = decide_overchange(game_detail)
                res['available_batsman'] = available_batsman(game_detail, teamA_players, teamB_players)
                res['available_bowler'] = available_bowler(game_detail, teamA_players, teamB_players)
                res['run_req'] = None
                res['scoreA'] = scoreA
                res['wicketA'] = wicketA
                res['overA'] = overA
                res['run_rateA'] = teamA_runrate(game_detail)
                res['scoreB'] = scoreB
                res['wicketB'] = wicket
                res['overB'] = over
                res['run_rateB'] = teamB_runrate(game_detail)
                res['req_run_inball'] = required_run_ball(game_detail)
                res['req_run_rate'] = required_run_rate(game_detail)
                res['numberA'] = teamA_no
                res['numberB'] = teamB_no
                return res
        else:
            game_detail['teamB'] = (str(scoreB + teamB_no) + "/" + str(wicket) + "/" + str(update_over(over, add_ball = 1)))
            s = game_detail['teamB'].split('/')
            # splitting scoreboard to get runs wicket and over respectively
            scoreB = int(s[0])
            wicket = int(s[1])
            over = float(s[2])
            if teamB_innings_end(game_detail) == True: # now again checking whether after the wicket innings has ended or not
                if teamA_no == teamB_no:
                    game_detail['scorecard']['teamB'][current_batsman] = update_scorecard_of_player(game_detail['scorecard']['teamB'][current_batsman],0,1,'out',None,None,None)   # add one extra ball to scorecard of the player as the player played this ball and got out
                    game_detail['scorecard']['teamA'][current_bowler] = update_scorecard_of_player(game_detail['scorecard']['teamA'][current_bowler],None,None,None,1,0,1) # add one wicket to the baller
                else:
                    game_detail['scorecard']['teamB'][current_batsman] = update_scorecard_of_player(game_detail['scorecard']['teamB'][current_batsman],teamB_no,0,'not_out',None,None,None)   # add one extra ball to scorecard of the player as the player played this ball and got out
                    game_detail['scorecard']['teamA'][current_bowler] = update_scorecard_of_player(game_detail['scorecard']['teamA'][current_bowler],None,None,None,1,teamB_no,0) # add one wicket to the baller
                res = generate_result(game_detail, teamA, teamB) # generating final results
                return res
            else:
                game_detail['scorecard']['teamB'][current_batsman] = update_scorecard_of_player(game_detail['scorecard']['teamB'][current_batsman],teamB_no,0,'not_out',None,None,None)   # add one extra ball to scorecard of the player as the player played this ball and got out
                game_detail['scorecard']['teamA'][current_bowler] = update_scorecard_of_player(game_detail['scorecard']['teamA'][current_bowler],None,None,None,1,teamB_no,0)
                res = {}
                res['game_end'] = False
                res['game_detail'] = game_detail
                res['innings_end'] = False
                res['innings'] = 'teamB'                  # if innings_end is False then only innings will generate
                res['result'] = "score increase"             # innings means who is currently batting
                res['over_change'] = decide_overchange(game_detail)
                res['available_batsman'] = available_batsman(game_detail, teamA_players, teamB_players)
                res['available_bowler'] = available_bowler(game_detail, teamA_players, teamB_players)
                res['run_req'] = None
                res['scoreA'] = scoreA
                res['wicketA'] = wicketA
                res['overA'] = overA
                res['run_rateA'] = teamA_runrate(game_detail)
                res['scoreB'] = scoreB
                res['wicketB'] = wicket
                res['overB'] = over
                res['run_rateB'] = teamB_runrate(game_detail)
                res['req_run_inball'] = required_run_ball(game_detail)
                res['req_run_rate'] = required_run_rate(game_detail)
                res['numberA'] = teamA_no
                res['numberB'] = teamB_no
                return res
    else:
        res = generate_result(game_detail, teamA, teamB) # generating final results
        return res
        
        
# backend code ends here
#________________________________________________________________________________________________________________________________________________________________________________________#
'''
game_detail = { 'no_of_wickets':2, 'no_of_overs':2, 'teamA':'0/0/0', 'teamB':'0/0/0.0', 'scorecard':{ 'teamA':{}, 'teamB':{} } }
res = init(game_detail, 2, 4, 'r', 's', ['r','p'], ['s','a'], teamA = 'teamA', teamB = 'teamB')
game_detail = res['game_detail']
print(res)
res = init(game_detail, 4, 4, 'r', 's', ['r','p'], ['s','a'], teamA = 'teamA', teamB = 'teamB')
game_detail = res['game_detail']
print(res)
res = init(game_detail, 6, 4, 'p', 's', ['r','p'], ['s','a'], teamA = 'teamA', teamB = 'teamB')
game_detail = res['game_detail']
print(res)
res = init(game_detail, 6, 4, 'p', 's', ['r','p'], ['s','a'], teamA = 'teamA', teamB = 'teamB')
game_detail = res['game_detail']
print(res)
res = init(game_detail, 6, 4, 'p', 's', ['r','p'], ['s','a'], teamA = 'teamA', teamB = 'teamB')
game_detail = res['game_detail']
print(res)
res = init(game_detail, 4, 4, 'p', 's', ['r','p'], ['s','a'], teamA = 'teamA', teamB = 'teamB')
game_detail = res['game_detail']
print(res)
print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')

res = init(game_detail, 6, 4, 's', 'r', ['r','p'], ['s','a'], teamA = 'teamA', teamB = 'teamB')
game_detail = res['game_detail']
print(res)
res = init(game_detail, 6, 4, 's', 'r', ['r','p'], ['s','a'], teamA = 'teamA', teamB = 'teamB')
game_detail = res['game_detail']
print(res)
res = init(game_detail, 6, 4, 's', 'r', ['r','p'], ['s','a'], teamA = 'teamA', teamB = 'teamB')
game_detail = res['game_detail']
print(res)
res = init(game_detail, 6, 4, 's', 'r', ['r','p'], ['s','a'], teamA = 'teamA', teamB = 'teamB')
game_detail = res['game_detail']
print(res)
'''


