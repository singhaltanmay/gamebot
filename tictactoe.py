from shutil import move
from telegram import InlineKeyboardButton
import random

def c1r1(game_arena, player):
    if player=='p1':
        game_arena[0][0]=InlineKeyboardButton("❌", callback_data="done")
        return game_arena
    else:
        game_arena[0][0]=InlineKeyboardButton("⭕", callback_data="done")
        return game_arena
    
def c1r2(game_arena, player):
    if player=='p1':
        game_arena[1][0]=InlineKeyboardButton("❌", callback_data="done")
        return game_arena
    else:
        game_arena[1][0]=InlineKeyboardButton("⭕", callback_data="done")
        return game_arena

def c1r3(game_arena, player):
    if player=='p1':
        game_arena[2][0]=InlineKeyboardButton("❌", callback_data="done")
        return game_arena
    else:
        game_arena[2][0]=InlineKeyboardButton("⭕", callback_data="done")
        return game_arena

def c2r1(game_arena, player):
    if player=='p1':
        game_arena[0][1]=InlineKeyboardButton("❌", callback_data="done")
        return game_arena
    else:
        game_arena[0][1]=InlineKeyboardButton("⭕", callback_data="done")
        return game_arena

def c2r2(game_arena, player):
    if player=='p1':
        game_arena[1][1]=InlineKeyboardButton("❌", callback_data="done")
        return game_arena
    else:
        game_arena[1][1]=InlineKeyboardButton("⭕", callback_data="done")
        return game_arena

def c2r3(game_arena, player):
    if player=='p1':
        game_arena[2][1]=InlineKeyboardButton("❌", callback_data="done")
        return game_arena
    else:
        game_arena[2][1]=InlineKeyboardButton("⭕", callback_data="done")
        return game_arena

def c3r1(game_arena, player):
    if player=='p1':
        game_arena[0][2]=InlineKeyboardButton("❌", callback_data="done")
        return game_arena
    else:
        game_arena[0][2]=InlineKeyboardButton("⭕", callback_data="done")
        return game_arena

def c3r2(game_arena, player):
    if player=='p1':
        game_arena[1][2]=InlineKeyboardButton("❌", callback_data="done")
        return game_arena
    else:
        game_arena[1][2]=InlineKeyboardButton("⭕", callback_data="done")
        return game_arena

def c3r3(game_arena, player):
    if player=='p1':
        game_arena[2][2]=InlineKeyboardButton("❌", callback_data="done")
        return game_arena
    else:
        game_arena[2][2]=InlineKeyboardButton("⭕", callback_data="done")
        return game_arena

game=[['.','.','.'],
      
      ['.','.','.'],

      ['.','.','.']]

def checker(game, chance):
    if game[0][0]=='x' and game[0][1]=='x' and game[0][2]=='x' and chance<=9:
        return ['won','p1']
    elif game[1][0]=='x' and game[1][1]=='x' and game[1][2]=='x' and chance<=9:
        return ['won','p1']
    elif game[2][0]=='x' and game[2][1]=='x' and game[2][2]=='x' and chance<=9:
        return ['won','p1']
    elif game[0][0]=='x' and game[1][0]=='x' and game[2][0]=='x' and chance<=9:
        return ['won','p1']
    elif game[0][1]=='x' and game[1][1]=='x' and game[2][1]=='x' and chance<=9:
        return ['won','p1']
    elif game[0][2]=='x' and game[1][2]=='x' and game[2][2]=='x' and chance<=9:
        return ['won','p1']
    elif game[0][0]=='x' and game[1][1]=='x' and game[2][2]=='x' and chance<=9:
        return ['won','p1']
    elif game[0][2]=='x' and game[1][1]=='x' and game[2][0]=='x' and chance<=9:
        return ['won','p1']
    elif game[0][0]=='o' and game[0][1]=='o' and game[0][2]=='o' and chance<=9:
        return ['won','p2']
    elif game[1][0]=='o' and game[1][1]=='o' and game[1][2]=='o' and chance<=9:
        return ['won','p2']
    elif game[2][0]=='o' and game[2][1]=='o' and game[2][2]=='o' and chance<=9:
        return ['won','p2']
    elif game[0][0]=='o' and game[1][0]=='o' and game[2][0]=='o' and chance<=9:
        return ['won','p2']
    elif game[0][1]=='o' and game[1][1]=='o' and game[2][1]=='o' and chance<=9:
        return ['won','p2']
    elif game[0][2]=='o' and game[1][2]=='o' and game[2][2]=='o' and chance<=9:
        return ['won','p2']
    elif game[0][0]=='o' and game[1][1]=='o' and game[2][2]=='o' and chance<=9:
        return ['won','p2']
    elif game[0][2]=='o' and game[1][1]=='o' and game[2][0]=='o' and chance<=9:
        return ['won','p2']
    elif chance==9:
        return ['draw']
    else:
        return ['playon']


    

def legal_moves(ttt_game):
    moves=[]
    for i in range(len(ttt_game[0])):
        if ttt_game[0][i]=='.':
            moves.append(f'c{i+1}r1')
        else:
            continue
    for i in range(len(ttt_game[1])):
        if ttt_game[1][i]=='.':
            moves.append(f'c{i+1}r2')
        else:
            continue
    for i in range(len(ttt_game[2])):
        if ttt_game[2][i]=='.':
            moves.append(f'c{i+1}r3')
        else:
            continue
    return moves

def blocker(game, moves):
    
    r1=game[0]
    r2=game[1]
    r3=game[2]

    if r1[0]=='x' and r1[1]=='x' and 'c3r1' in moves:
        move='c3r1'
    elif r1[0]=='x' and r1[2]=='x' and 'c2r1' in moves:
        move='c2r1'
    elif r1[1]=='x' and r1[2]=='x' and 'c1r1' in moves:
        move='c1r1'
    elif r2[0]=='x' and r2[1]=='x' and 'c3r2' in moves:
        move='c3r2'
    elif r2[0]=='x' and r2[2]=='x' and 'c2r2' in moves:
        move='c2r2'
    elif r2[1]=='x' and r2[2]=='x' and 'c1r2' in moves:
        move='c1r2'
    elif r3[0]=='x' and r3[1]=='x' and 'c3r3' in moves:
        move='c3r3'
    elif r3[0]=='x' and r3[2]=='x' and 'c2r3' in moves:
        move='c2r3'
    elif r3[1]=='x' and r3[2]=='x' and 'c1r3' in moves:
        move='c1r3'
    elif r1[0]=='x' and r3[2]=='x' and 'c2r2' in moves:
        move='c2r2'
    elif r1[0]=='x' and r2[1]=='x' and 'c3r3' in moves:
        move='c3r3'
    elif r2[1]=='x' and r3[2]=='x' and 'c1r1' in moves:
        move='c1r1'
    elif r1[2]=='x' and r3[0]=='x' and 'c2r2' in moves:
        move='c2r2'
    elif r1[2]=='x' and r2[1]=='x' and 'c1r3' in moves:
        move='c1r3'
    elif r2[1]=='x' and r3[0]=='x' and 'c3r1' in moves:
        move='c3r1'    
    elif r1[0]=='x' and r2[0]=='x' and 'c1r3' in moves:
        move='c1r3'
    elif r1[0]=='x' and r3[0]=='x' and 'c1r2' in moves:
        move='c1r2'
    elif r2[0]=='x' and r3[0]=='x' and 'c1r1' in moves:
        move='c1r1'
    elif r1[1]=='x' and r2[1]=='x' and 'c2r3' in moves:
        move='c2r3'
    elif r1[1]=='x' and r3[1]=='x' and 'c2r2' in moves:
        move='c2r2'
    elif r2[1]=='x' and r3[1]=='x' and 'c2r1' in moves:
        move='c2r1'
    elif r1[2]=='x' and r2[2]=='x' and 'c3r3' in moves:
        move='c3r3'
    elif r1[2]=='x' and r3[2]=='x' and 'c3r2' in moves:
        move='c3r2'
    elif r2[2]=='x' and r3[2]=='x' and 'c3r1' in moves:
        move='c3r1'
    

    elif r1[0]=='o' and r1[1]=='o' and 'c3r1' in moves:
        move='c3r1'
    elif r1[0]=='o' and r1[2]=='o' and 'c2r1' in moves:
        move='c2r1'
    elif r1[1]=='o' and r1[2]=='o' and 'c1r1' in moves:
        move='c1r1'
    elif r2[0]=='o' and r2[1]=='o' and 'c3r2' in moves:
        move='c3r2'
    elif r2[0]=='o' and r2[2]=='o' and 'c2r2' in moves:
        move='c2r2'
    elif r2[1]=='o' and r2[2]=='o' and 'c1r2' in moves:
        move='c1r2'
    elif r3[0]=='o' and r3[1]=='o' and 'c3r3' in moves:
        move='c3r3'
    elif r3[0]=='o' and r3[2]=='o' and 'c2r3' in moves:
        move='c2r3'
    elif r3[1]=='o' and r3[2]=='o' and 'c1r3' in moves:
        move='c1r3'
    elif r1[0]=='o' and r3[2]=='o' and 'c2r2' in moves:
        move='c2r2'
    elif r1[0]=='o' and r2[1]=='o' and 'c3r3' in moves:
        move='c3r3'
    elif r2[1]=='o' and r3[2]=='o' and 'c1r1' in moves:
        move='c1r1'
    elif r1[2]=='o' and r3[0]=='o' and 'c2r2' in moves:
        move='c2r2'
    elif r1[2]=='o' and r2[1]=='o' and 'c1r3' in moves:
        move='c1r3'
    elif r2[1]=='o' and r3[0]=='o' and 'c3r1' in moves:
        move='c3r1'
    elif r1[0]=='o' and r2[0]=='o' and 'c1r3' in moves:
        move='c1r3'
    elif r1[0]=='o' and r3[0]=='o' and 'c1r2' in moves:
        move='c1r2'
    elif r2[0]=='o' and r3[0]=='o' and 'c1r1' in moves:
        move='c1r1'
    elif r1[1]=='o' and r2[1]=='o' and 'c2r3' in moves:
        move='c2r3'
    elif r1[1]=='o' and r3[1]=='o' and 'c2r2' in moves:
        move='c2r2'
    elif r2[1]=='o' and r3[1]=='o' and 'c2r1' in moves:
        move='c2r1'
    elif r1[2]=='o' and r2[2]=='o' and 'c3r3' in moves:
        move='c3r3'
    elif r1[2]=='o' and r3[2]=='o' and 'c3r2' in moves:
        move='c3r2'
    elif r2[2]=='o' and r3[2]=='o' and 'c3r1' in moves:
        move='c3r1'
    else:
        idx = random.randint(0,len(moves)-1)
        move=moves[idx]
    return move

def placer(game, move, chance):
    
    game_given=game
    
    if move=='c1r1' and chance%2==1:
        game[0][0]='x'
    elif move=='c2r1' and chance%2==1:
        game[0][1]='x'
    elif move=='c3r1' and chance%2==1:
        game[0][2]='x'
    elif move=='c1r2' and chance%2==1:
        game[1][0]='x'
    elif move=='c2r2' and chance%2==1:
        game[1][1]='x'
    elif move=='c3r2' and chance%2==1:
        game[1][2]='x'
    elif move=='c1r3' and chance%2==1:
        game[2][0]='x'
    elif move=='c2r3' and chance%2==1:
        game[2][1]='x'
    elif move=='c3r3' and chance%2==1:
        game[2][2]='x'
        
    elif move=='c1r1' and chance%2==0:
        game[0][0]='o'
    elif move=='c2r1' and chance%2==0:
        game[0][1]='o'
    elif move=='c3r1' and chance%2==0:
        game[0][2]='o'
    elif move=='c1r2' and chance%2==0:
        game[1][0]='o'
    elif move=='c2r2' and chance%2==0:
        game[1][1]='o'
    elif move=='c3r2' and chance%2==0:
        game[1][2]='o'
    elif move=='c1r3' and chance%2==0:
        game[2][0]='o'
    elif move=='c2r3' and chance%2==0:
        game[2][1]='o'
    elif move=='c3r3' and chance%2==0:
        game[2][2]='o'

    print(game)
    print(game_given)
    return game

    
    
def dr_strange():
    outcomes={}
    c1r1={}
    c2r1={}
    c3r1={}
    c1r2={}
    c2r2={}
    c3r2={}
    c1r3={}
    c2r3={}
    c3r3={}
    game=[['.', '.', '.'],
          ['.', '.', '.'],
          ['.', '.', '.']
        ]
    moves=legal_moves(game)
    count=1
    chance=1
    line=[]

    move1=legal_moves(placer(game, 'c1r1', chance))
    game=placer(game, 'c1r1', chance)
    chance=2

    for a in move1:
        
        game2=placer(game, a, chance)

        chance=3
        move2=legal_moves(game2)
        c1r1[a]={'status':checker(game2, chance), 'game' : game2}
        
        if 'playon' in c1r1[a]['status']:

            for b in move2:
                
                game3=placer(game2, b, chance)
                chance=4
                move3=legal_moves(game3)
                c1r1[a][b]={'status':checker(game3, chance), 'game' : game3}
                
                if 'playon' in c1r1[a][b]['status']:

                    for c in move3:
                        
                        game4=placer(game3, c, chance)

                        chance=5
                        move4=legal_moves(game4)
                        c1r1[a][b][c]={'status':checker(game3, chance), 'game' : game4}
                        
                        if 'playon' in c1r1[a][b][c]['status']:

                            for d in move4:
                        
                                game5=placer(game4, d, chance)

                                chance=6
                                move5=legal_moves(game5)
                                c1r1[a][b][c][d]={'status':checker(game3, chance), 'game' : game5}
                                
                                
                                if 'playon' in c1r1[a][b][c][d]['status']:

                                    for e in move5:
                                        
                                        game6=placer(game5, e, chance)

                                        chance=7
                                        move6=legal_moves(game6)
                                        c1r1[a][b][c][d][e]={'status':checker(game3, chance), 'game' : game6}
                                        
                                        
                                        if 'playon' in c1r1[a][b][c][d][e]['status']:

                                            for f in move6:
                                               
                                                game7=placer(game6, f, chance)

                                                chance=8
                                                move7=legal_moves(game7)
                                                c1r1[a][b][c][d][e][f]={'status':checker(game3, chance), 'game' : game7}
                                                
                                                
                                                if 'playon' in c1r1[a][b][c][d][e][f]['status']:

                                                    for g in move7:
                                                        
                                                        game8=placer(game7, g, chance)

                                                        chance=9
                                                        move8=legal_moves(game8)
                                                        c1r1[a][b][c][d][e][f][g]={'status':checker(game3, chance), 'game' : game8}
                                                        
                                                        if 'playon' in c1r1[a][b][c][d][e][f][g]['status']:

                                                            for h in move8:
                                                                
                                                                game9=placer(game8, h, chance)

                                                                chance=9
                                                                move9=legal_moves(game9)
                                                                c1r1[a][b][c][d][e][f][g][h]={'status':checker(game3, chance), 'game' : game9}
                                                                
        
                                                        else:
                                                            
                                                            continue
                                                    
                                                else:
                                                    continue

                                            
                                        else:
                                            
                                            continue
                                    
                                else:
                                    
                                    continue



                            
                        else:
                            
                            continue

                    
                else:
                    
                    continue
                
        else:
            
            continue
    print(c1r1['c2r1']['c1r2']['c2r2']['c1r3'])

#dr_strange()
    


def AI(ttt_details, diff='normal'):
    
    moves = legal_moves(ttt_details['ttt_game'])
    game_arena=ttt_details['ttt_arena']
    if diff=='normal':
   
        move = blocker(ttt_details['ttt_game'], moves)

        if move == 'c1r1':
            ttt_details['game_arena']=c1r1(game_arena, 'p2')
            ttt_details['ttt_game'][0][0]= 'o'
        elif move == 'c2r1':
            ttt_details['game_arena']=c2r1(game_arena, 'p2')
            ttt_details['ttt_game'][0][1]= 'o'
        elif move == 'c3r1':
            ttt_details['game_arena']=c3r1(game_arena, 'p2')
            ttt_details['ttt_game'][0][2]= 'o'
        elif move == 'c1r2':
            ttt_details['game_arena']=c1r2(game_arena, 'p2')
            ttt_details['ttt_game'][1][0]= 'o'
        elif move == 'c2r2':
            ttt_details['game_arena']=c2r2(game_arena, 'p2')
            ttt_details['ttt_game'][1][1]= 'o'
        elif move == 'c3r2':
            ttt_details['game_arena']=c3r2(game_arena, 'p2')
            ttt_details['ttt_game'][1][2]= 'o'
        elif move == 'c1r3':
            ttt_details['game_arena']=c1r3(game_arena, 'p2')
            ttt_details['ttt_game'][2][0]= 'o'
        elif move == 'c2r3':
            ttt_details['game_arena']=c2r3(game_arena, 'p2')
            ttt_details['ttt_game'][2][1]= 'o'
        elif move == 'c3r3':
            ttt_details['game_arena']=c3r3(game_arena, 'p2')
            ttt_details['ttt_game'][2][2]= 'o'
        else:
            'error'
        return [ttt_details, move]
            
            
   















