#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''Importing all required telegram library'''
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext import Updater, MessageHandler, Filters
import telegram

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''Importing all other required library'''
import telepot
import os
import telebot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes
import tictactoe
import hand_cricket
import random
import time
import pickle
#import Chess

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''Function for fetching saved data'''
def open_dict(file_name):
        a_file = open("Data/" + file_name + ".pkl" , "rb")
        output = pickle.load(a_file)
        a_file.close()
        return output
    
def save_dict(file_name,dictionary):
        a_file = open("Data/" + file_name + ".pkl", "wb")
        pickle.dump(dictionary, a_file)
        a_file.close()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''Updating the dictionary after fetching the data'''

api_open = open("Data/API.txt", "r")
API = str(api_open.read()).strip()

main_img = os.path.expanduser("Data//image_main.png")
# To display in the Start Message

hc_game_list = open_dict('hc_game_list')
# 'link' : [status_of_game, game_detail, [admin,player1,player2], [teamA], [teamB], [current_batsman, no_selected], [current_bowler, no_selected]]

userlist = open_dict('userlist')
# Main dictionary containing UserID : UserName pairs

ttt_game_list = open_dict('ttt_game_list')
# 'link':{ status_of_game, game_detail}

chess_game_list = open_dict('chess_game_list') 
# 'link' : {status_of_game, game_detail, {black:[], white:[]}}

bj_game_list = open_dict('bj_game_list')

'''Updating dictionary ends'''

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''Assigning some variables'''

# Three status of game : lobby , started , ended
player_dict = {}
game_end = False # display the criteria whether the game ended or not
game = None # gives current game
hc_list = [] # list of players
hc_text = {}

'''Assigning ends'''

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''Some General Game Functions'''
    
def shuffle_player(li):
    # Shuffles all the player in li into a team of 2
    # li is the list
    teamA = []
    teamA.append(li[0])
    li.pop(0)
    length = (len(li)-1)/2
    teamB = []
    i = 1
    while i < (length+1):
        x = random.randint(0,len(li)-1)
        teamA.append(li[x])
        li.pop(x)
        i = i + 1
    teamB = li
    return [teamA,teamB]
        
def generate_link():
    # Randomly Generates a 6 letter string
    global hc_game_list
    while True:
        comb = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '-', '_', '+', '=', ':', '?', '*','1','2','3','4','5','6','7','8','9','0']
        s1 = random.randint(0,len(comb)-1)
        s2 = random.randint(0,len(comb)-1)
        s3 = random.randint(0,len(comb)-1)
        s4 = random.randint(0,len(comb)-1)
        s5 = random.randint(0,len(comb)-1)
        s6 = random.randint(0,len(comb)-1)
        string = comb[s1] + comb [s2] + comb[s3] + comb [s4] + comb[s5] + comb [s6]
        if string  not in hc_game_list:
            break
    return string

def assign_link(username,game_detail, game = 'hc'):
    global hc_game_list
    global userlist
    global ttt_game_list
    global chess_game_list

    if game == 'hc':
        link = generate_link()
        hc_game_list[link] = ['lobby',game_detail,[userlist[username]],[],[],[],[],'','',[]] # The last one is for bowler list
        save_dict('hc_game_list',hc_game_list)
        return link

    elif game == 'tic_tac_toe':
        link = generate_link()
        ttt_game_list[link] = ['lobby',game_detail, {'p1':[], 'p2':[]}]
        save_dict('ttt_game_list',ttt_game_list)
        return link    

    elif game == 'chess':
        link = generate_link()
        chess_game_list[link] = ['lobby', game_detail, {'black':[], 'white':[]}]
        save_dict('chess_game_list',chess_game_list)
        return link
    
def generate_sb(link,team):
    global hc_game_list
    if team == 'teamA':
        string = ""
        l = hc_game_list[link][1]['scorecard']['teamA']
        for i in l:
            string = string + "\n<b>" + i + " :</b> " + l[i]
        return string
    else:
        string = ""
        l = hc_game_list[link][1]['scorecard']['teamB']
        for i in l:
            string = string + "\n<b>" + i + " :</b> " + l[i]
        return string

def get_bowler_list(link):
    global hc_game_list
    return hc_game_list[link][9]

def getlink(data):
    return (data.split('//')[1]).strip()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''Some General Telegram Functions'''

def get_user_ID(update):
    user = update.callback_query.from_user
    return int(user['id'])

def get_user_ID_from_msg(update):
    user = update.message.from_user
    return int(user['id'])

def get_user_ID_msg(update):
    user = update.message.from_user
    return int(user['id'])

def info_msg(message,update): # Showing the info message
    update.callback_query.answer(text = message , show_alert = True)
    
def get_text(context): # To get the text of a message after command
    k = context.args
    y = ""
    try:
        if k==0:
            y=""
        else:
            for i in k:
                y=y+" "+i
            z=y.strip()
            y=z
        return y
    except Exception as e:
        print(str(e))
        return ""

def send_message(update,context,reply,reply_to_reply="Decide"):
    reply_to_message=update.message.reply_to_message
    if reply_to_reply=="Decide":
        if reply_to_message is None:
            bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING, timeout=1)
            bot.sendMessage(chat_id=update.message.chat_id,text=reply,reply_to_message_id = update.message.message_id,parse_mode=telegram.ParseMode.HTML)
        else:
            bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING, timeout=1)
            bot.sendMessage(chat_id=update.message.chat_id,text=reply,reply_to_message_id=reply_to_message['message_id'],parse_mode=telegram.ParseMode.HTML)
    elif reply_to_reply=="True":
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING, timeout=1)
        bot.sendMessage(chat_id=update.message.chat_id,text=reply,reply_to_message_id=reply_to_message['message_id'],parse_mode=telegram.ParseMode.HTML)
    elif reply_to_reply=="False":
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING, timeout=1)
        bot.sendMessage(chat_id=update.message.chat_id,text=reply,reply_to_message_id = update.message.message_id,parse_mode=telegram.ParseMode.HTML)
    elif reply_to_reply=="NoReply":
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING, timeout=1)
        bot.sendMessage(chat_id=update.message.chat_id,text=reply,parse_mode=telegram.ParseMode.HTML)
    else:
        print("reply_to_reply: Unknown text specified")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''Telegram Commands Starts Here'''

def start(update: Update, context: CallbackContext):
    global main_img
    text = '[this is the hello message]'
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(main_img,'rb'), caption = text, reply_to_message_id = update.message.message_id, parse_mode=telegram.ParseMode.HTML)

def register(update: Update, context: CallbackContext):
    username = get_text(context)
    if get_user_ID_from_msg(update) in userlist:
        send_message(update, context, '[user already registered]', 'False')
    else:
            if username not in userlist:
                userlist[get_user_ID_from_msg(update)] = username
                save_dict('userlist',userlist)
                send_message(update, context, '[registration successfull]', 'False')
            else:
                send_message(update, context, '[username already exist]', 'False')

def help(update: Update, context: CallbackContext):
    text = '[this is the help]'
    
    keyboard = [
            [
                InlineKeyboardButton("Add to a Group", url = 'https://t.me/RT_GameBot?startgroup=a')
            ],]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING, timeout=1)
    update.message.reply_text(text, reply_markup=reply_markup, reply_to_message_id = update.message.message_id, parse_mode=telegram.ParseMode.HTML)

def new_member(bot, update):
    global main_img
    text = '[this is the hello message]'
    for member in update.message.new_chat_members:
        if member.username == 'RT_GameBot':
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(main_img,'rb'), caption = text, parse_mode=telegram.ParseMode.HTML)

            
def display_all_game(update: Update, context: CallbackContext):
    global player_dict
    global game_detail
    no_display = [
        [
            InlineKeyboardButton("Hand Cricket", callback_data="h_c"),
    ],[
            InlineKeyboardButton("Tic Tac Toe", callback_data="t_t_t"),
    ],[
            InlineKeyboardButton("Chess", callback_data="chess"),
    ],[
            InlineKeyboardButton("Blackjack", callback_data="blackjack"),
    ],]
    reply_markup = InlineKeyboardMarkup(no_display)
    update.message.reply_text("Welcome <b>" + str(userlist[get_user_ID_msg(update)]) + "</b> !\n Please choose one of the below games", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def game_handler(update: Update, context: CallbackContext):
    
    global game
    global hc_list
    global game_end
    global hc_game_list
    global userlist
    global hc_text
    global ttt_game_list
    global chess_game_list
    query=update.callback_query
    data=query.data
    user = update.callback_query.from_user
    if data == 'h_c':
        keyboard = [
            [
                InlineKeyboardButton("Single Player", callback_data=("hc_single"))
            ],[
                InlineKeyboardButton("Multi Player", callback_data=("hc_multi")),
        ],]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("OK! Now choose your <b>Game Type</b>\n<b>Single Player</b> means that you would be playing with a <i>computer</i>.\n<b>Multi Player</b> means that you can play with your <i>friends</i>.", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

    elif data=='t_t_t':
        keyboard = [
            [
                InlineKeyboardButton("Single Player", callback_data=("ttt_single"))
            ],[
                InlineKeyboardButton("Multi Player", callback_data=("ttt_multi")),
        ],]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("OK! Now choose your <b>Game Type</b>\n<b>Single Player</b> means that you would be playing with a <i>computer</i>.\n<b>Multi Player</b> means that you can play with your <i>friends</i>.", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

    elif data == 'blackjack':
        keyboard = [
            [
                InlineKeyboardButton("Single Player", callback_data=("bj_single"))
            ],[
                InlineKeyboardButton("Multi Player", callback_data=("bj_multi")),
        ],]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("OK! Now choose your <b>Game Type</b>\n<b>Single Player</b> means that you would be playing with a <i>computer</i>.\n<b>Multi Player</b> means that you can play with your <i>friends</i>.", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

    elif data=='chess':
        keyboard = [
            [
                InlineKeyboardButton("Single Player", callback_data=("chess_single"))
            ],[
                InlineKeyboardButton("Multi Player", callback_data=("chess_multi")),
        ],]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("OK! Now choose your <b>Game Type</b>\n<b>Single Player</b> means that you would be playing with a <i>computer</i>.\n<b>Multi Player</b> means that you can play with your <i>friends</i>.", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
    
    elif data=='chess_multi':
        game_details={
                'fen':'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                 'board': Chess.fen_to_board(),
                 'arena': None
                }
        link = assign_link(int(get_user_ID(update)), game_details, game='chess')
        chess_game_list[link][2]['white']=[user['id'], user['first_name']]
        print(chess_game_list)
        keyboard = [
            [
                InlineKeyboardButton("Join the Game", callback_data=("chess_p2//" + link))
            ],[
                InlineKeyboardButton("Cancel the Game (only for Admin i.e. "+chess_game_list[link][2]['white'][1]+')', callback_data=("chess_cancel//" + link))
            ]]
        reply_markup=InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Your Chess <b> Game Created </b> with details as follows \n\n Admin (and White) : "+chess_game_list[link][2]['white'][1]+'\n Player 2 (black) : <i> Waiting.... </i>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)                         

    elif data=='ttt_single':
        ttt_details={'ttt_game':[['.','.','.'],
      
                       ['.','.','.'],

                       ['.','.','.']],
             'ttt_arena':[
          [
            InlineKeyboardButton(" ", callback_data="c1r1_single//"),
            InlineKeyboardButton(" ", callback_data="c2r1_single//"),
            InlineKeyboardButton(" ", callback_data="c3r1_single//"),
        ],[
            InlineKeyboardButton(" ", callback_data="c1r2_single//"),
            InlineKeyboardButton(" ", callback_data="c2r2_single//"),
            InlineKeyboardButton(" ", callback_data="c3r2_single//"),
        ],[
            InlineKeyboardButton(" ", callback_data="c1r3_single//"),
            InlineKeyboardButton(" ", callback_data="c2r3_single//"),
            InlineKeyboardButton(" ", callback_data="c3r3_single//"),
         ]], 'chance':1}
        link = assign_link(int(get_user_ID(update)), ttt_details, game='tic_tac_toe')
        ttt_game_list[link][2]['p1']=[user['id'], user['first_name'], 0]
        ttt_game_list[link][2]['admin']=[user['id'], user['first_name']]
        keyboard = [
            [
                InlineKeyboardButton("AI Unbeatable", callback_data=("ttt_aiu//" + link))
            ],[
                InlineKeyboardButton('AI Normal', callback_data=("ttt_ain//" + link))
            ]]
        reply_markup=InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Your Tic Tac Toe <b> Game Created </b> with details as follows \n\n Admin (and Player 1) : "+ttt_game_list[link][2]['admin'][1]+' (❌) \n Player 2 : <i>Choose difficulty.... </i>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)   
    
    elif 'ttt_ain' in data or 'ttt_aiu' in data:
        link = data.split('//')[1]
        if user['id'] in ttt_game_list[link][2]['admin'] and 'ttt_ain' in data:
            ttt_game_list[link][2]['p2'] = [f'normal//{link}', 'AI Normal', 0]
            keyboard = [
                [
                    InlineKeyboardButton("START GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_ai_begin//'+link)),
                ],]
            reply_markup = InlineKeyboardMarkup(keyboard)
            print(ttt_game_list)
            query.edit_message_text("Game creation completed with details as follows \n\n Admin (and Player 1) : "+ttt_game_list[link][2]['p1'][1]+' (❌) \n Player 2 : '+ttt_game_list[link][2]['p2'][1]+' (⭕) \n\n Click button below to begin the game!!', reply_markup=reply_markup)
        
        elif user['id'] in ttt_game_list[link][2]['admin'] and 'ttt_aiu' in data:
            ttt_game_list[link][2]['p2'] = [f'unbeatable//{link}', 'AI Unbeatable', 0]
            keyboard = [
                [
                    InlineKeyboardButton("START GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_ai_begin//'+link)),
                ],]
            reply_markup = InlineKeyboardMarkup(keyboard)
            print(ttt_game_list)
            query.edit_message_text("Game creation completed with details as follows \n\n Admin (and Player 1) : "+ttt_game_list[link][2]['p1'][1]+' (❌) \n Player 2 : '+ttt_game_list[link][2]['p2'][1]+' (⭕) \n\n Click button below to begin the game!!', reply_markup=reply_markup)

        else:
            info_msg('Why are you clicking', update)

    elif data=='ttt_multi':
        ttt_details={'ttt_game':[['.','.','.'],
      
                       ['.','.','.'],

                       ['.','.','.']],
             'ttt_arena':[
          [
            InlineKeyboardButton(" ", callback_data="c1r1"),
            InlineKeyboardButton(" ", callback_data="c2r1"),
            InlineKeyboardButton(" ", callback_data="c3r1"),
        ],[
            InlineKeyboardButton(" ", callback_data="c1r2"),
            InlineKeyboardButton(" ", callback_data="c2r2"),
            InlineKeyboardButton(" ", callback_data="c3r2"),
        ],[
            InlineKeyboardButton(" ", callback_data="c1r3"),
            InlineKeyboardButton(" ", callback_data="c2r3"),
            InlineKeyboardButton(" ", callback_data="c3r3"),
         ]], 'chance':1}
        link = assign_link(int(get_user_ID(update)), ttt_details, game='tic_tac_toe')
        ttt_game_list[link][2]['admin']=[user['id'], user['first_name']]
        ttt_game_list[link][2]['p1']=[user['id'], user['first_name'], 0]
        keyboard = [
            [
                InlineKeyboardButton("Join the Game", callback_data=("ttt_p2//" + link))
            ],[
                InlineKeyboardButton("Cancel the Game (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=("ttt_cancel//" + link))
            ]]
        reply_markup=InlineKeyboardMarkup(keyboard)
        print(ttt_game_list)
        query.edit_message_text("Your Tic Tac Toe <b> Game Created </b> with details as follows \n\n Admin (and Player 1) : "+ttt_game_list[link][2]['admin'][1]+' (❌) \n Player 2 : <i> Waiting.... </i>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)                         

    elif 'ttt_again' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        keyboard = [
                [
                    InlineKeyboardButton("ACCEPT (only for "+player_dict['p2'][1]+')', callback_data=('ttt_re//'+link)),
                ],
                [
                    InlineKeyboardButton("CANCEL (only for "+player_dict['p2'][1]+')', callback_data=('ttt_end//'+link)),
                ],]
        reply_markup=InlineKeyboardMarkup(keyboard)
        query.edit_message_text(player_dict['p1'][1]+' Offered a rematch to '+player_dict['p2'][1]+'\n\n Would you Accept or Decline?', reply_markup=reply_markup)

    elif 'ttt_re' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        keyboard = [
        [
            InlineKeyboardButton(" ", callback_data="c1r1//"+link),
            InlineKeyboardButton(" ", callback_data="c2r1//"+link),
            InlineKeyboardButton(" ", callback_data="c3r1//"+link),
        ],[
            InlineKeyboardButton(" ", callback_data="c1r2//"+link),
            InlineKeyboardButton(" ", callback_data="c2r2//"+link),
            InlineKeyboardButton(" ", callback_data="c3r2//"+link),
        ],[
            InlineKeyboardButton(" ", callback_data="c1r3//"+link),
            InlineKeyboardButton(" ", callback_data="c2r3//"+link),
            InlineKeyboardButton(" ", callback_data="c3r3//"+link),
        ]]
        ttt_game_list[link][1]['ttt_arena']=keyboard
        ttt_game_list[link][1]['ttt_game']=[['.','.','.'],
      
                       ['.','.','.'],

                       ['.','.','.']]
        ttt_game_list[link][1]['chance']=1
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        if player_dict['p1']!=[] and player_dict['p2']!=[]:
            text=player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
            if user_id in player_dict['p2']:
                query.edit_message_text(text, reply_markup=reply_markup)
            else:
                info_msg('You dont have any games in queue', update)
        else:
            info_msg('No players registered', update)
            
    elif 'ttt_end' in data:
        link=data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        if player_dict['p1'][2] > player_dict['p2'][2]:
            query.edit_message_text('Tic Tac Toe between '+player_dict['p1'][1]+' and '+player_dict['p2'][1]+' ended with following score \n\n'+player_dict['p1'][1]+' : '+str(player_dict['p1'][2])+'\n'+player_dict['p2'][1]+' : '+str(player_dict['p2'][2])+"\n\n Evidently "+player_dict['p1'][1]+" won")                                                      
        elif player_dict['p2'][2] > player_dict['p1'][2]:
            query.edit_message_text('Tic Tac Toe between '+player_dict['p1'][1]+' and '+player_dict['p2'][1]+' ended with following score \n\n'+player_dict['p1'][1]+' : '+str(player_dict['p1'][2])+'\n'+player_dict['p2'][1]+' : '+str(player_dict['p2'][2])+"\n\n Evidently "+player_dict['p2'][1]+" won")
        else:
            query.edit_message_text('Tic Tac Toe between '+player_dict['p1'][1]+' and '+player_dict['p2'][1]+' ended with following score \n\n'+player_dict['p1'][1]+' : '+str(player_dict['p1'][2])+'\n'+player_dict['p2'][1]+' : '+str(player_dict['p2'][2])+"\n\n Evidently "+player_dict['p1'][1]+" and "+player_dict['p2'][1]+" drew")
        ttt_game_list[link][0]='end'
                                    
    elif 'ttt_end_admin' in data:
        link=data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        if user_id in player_dict['admin']:
            if player_dict['p1'][2] > player_dict['p2'][2]:
                query.edit_message_text('Tic Tac Toe between '+player_dict['p1'][1]+' and '+player_dict['p2'][1]+' ended with following score \n\n'+player_dict['p1'][1]+' : '+str(player_dict['p1'][2])+'\n'+player_dict['p2'][1]+' : '+str(player_dict['p2'][2])+"\n\n Evidently "+player_dict['p1'][1]+" won")                                                      
            elif player_dict['p2'][2] > player_dict['p1'][2]:
                query.edit_message_text('Tic Tac Toe between '+player_dict['p1'][1]+' and '+player_dict['p2'][1]+' ended with following score \n\n'+player_dict['p1'][1]+' : '+str(player_dict['p1'][2])+'\n'+player_dict['p2'][1]+' : '+str(player_dict['p2'][2])+"\n\n Evidently "+player_dict['p2'][1]+" won")
            else:
                query.edit_message_text('Tic Tac Toe between '+player_dict['p1'][1]+' and '+player_dict['p2'][1]+' ended with following score \n\n'+player_dict['p1'][1]+' : '+str(player_dict['p1'][2])+'\n'+player_dict['p2'][1]+' : '+str(player_dict['p2'][2])+"\n\n Evidently "+player_dict['p1'][1]+" and "+player_dict['p2'][1]+" drew")
            ttt_game_list[link][0]='end'
        else:
            info_msg('Option is only for admin', update)
                                    
    elif 'ttt_cancel' in data:
        link=data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id = user['id']
        no_display = [
        [
            InlineKeyboardButton("Hand Cricket", callback_data="h_c"),
    ],[
            InlineKeyboardButton("Tic Tac Toe", callback_data="t_t_t"),
    ],]
        reply_markup = InlineKeyboardMarkup(no_display)
        if user_id in player_dict['admin']:
            query.edit_message_text('<b> Game canceled </b>!\n Please choose one of the games below', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
            ttt_game_list[link][0]='end'
        else:
            info_msg('Option is only for admin', update)

    elif 'chess_p2' in data:
        link=data.split('//')[1]
        if user['id'] != chess_game_list[link][2]['white'][0]:
            chess_game_list[link][2]['black']=[user['id'], user['first_name']]
        
            keyboard = [
                [
                    InlineKeyboardButton("START GAME (only for Admin i.e. "+chess_game_list[link][2]['white'][1]+')', callback_data=('chess_begin//'+link)),
                ],]
            reply_markup = InlineKeyboardMarkup(keyboard)
            print(chess_game_list)
            query.edit_message_text("Game creation completed with details as follows \n\n Admin (and White) : "+chess_game_list[link][2]['white'][1]+'\n Player 2 (black) : '+chess_game_list[link][2]['black'][1]+'\n\n Click button below to begin the game!!', reply_markup=reply_markup)
        else:
            info_msg('Bring new people', update)
                    
    elif 'ttt_p2' in data:
        
        link=data.split('//')[1]
        if user['id'] != ttt_game_list[link][2]['p1'][0]:
            ttt_game_list[link][2]['p2']=[user['id'], user['first_name'], 0]
        
            keyboard = [
                [
                    InlineKeyboardButton("START GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_begin//'+link)),
                ],]
            reply_markup = InlineKeyboardMarkup(keyboard)
            print(ttt_game_list)
            query.edit_message_text("Game creation completed with details as follows \n\n Admin (and Player 1) : "+ttt_game_list[link][2]['p1'][1]+' (❌) \n Player 2 : '+ttt_game_list[link][2]['p2'][1]+' (⭕) \n\n Click button below to begin the game!!', reply_markup=reply_markup)
        else:
            info_msg('Bring new people', update)

    elif 'chess_begin' in data:
        link = data.split('//')[1]
        user_id=user['id']
        player_dict=chess_game_list[link][2]
        keyboard=Chess.board_to_keyboard([['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
                                          ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                                          ['.', '.', '.', '.', '.', '.', '.', '.'], 
                                          ['.', '.', '.', '.', '.', '.', '.', '.'], 
                                          ['.', '.', '.', '.', '.', '.', '.', '.'], 
                                          ['.', '.', '.', '.', '.', '.', '.', '.'], 
                                          ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
                                          ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']], link)

        chess_game_list[link][1]['arena']=keyboard
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if player_dict['white']!=[] and player_dict['black']!=[]:
            text=player_dict['white'][1]+ ' (White))    VS   '+player_dict['black'][1]+' (black)'
            if user_id in player_dict['white']:
                query.edit_message_text(text, reply_markup=reply_markup)
            else:
                info_msg('You dont have any games in queue', update)
        else:
            info_msg('No players registered', update)

    elif 'coords' in data:
        print(data)
            
    elif 'ttt_ai_begin' in data:
        link = data.split('//')[1]
        user_id=user['id']
        player_dict=ttt_game_list[link][2]
        keyboard = [
        [
            InlineKeyboardButton(" ", callback_data="c1r1_single//"+link),
            InlineKeyboardButton(" ", callback_data="c2r1_single//"+link),
            InlineKeyboardButton(" ", callback_data="c3r1_single//"+link),
        ],[
            InlineKeyboardButton(" ", callback_data="c1r2_single//"+link),
            InlineKeyboardButton(" ", callback_data="c2r2_single//"+link),
            InlineKeyboardButton(" ", callback_data="c3r2_single//"+link),
        ],[
            InlineKeyboardButton(" ", callback_data="c1r3_single//"+link),
            InlineKeyboardButton(" ", callback_data="c2r3_single//"+link),
            InlineKeyboardButton(" ", callback_data="c3r3_single//"+link),
        ]]
        ttt_game_list[link][1]['ttt_arena']=keyboard
        ttt_game_list[link][1]['ttt_game']=[['.','.','.'],
      
                       ['.','.','.'],

                       ['.','.','.']]
        ttt_game_list[link][1]['chance']=1
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        if player_dict['p1']!=[] and player_dict['p2']!=[]:
            text=player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
            if user_id in player_dict['admin']:
                query.edit_message_text(text, reply_markup=reply_markup)
            else:
                info_msg('You dont have any games in queue', update)
        else:
            info_msg('No players registered', update)
        
    elif 'ttt_begin' in data:
        link = data.split('//')[1]
        user_id=user['id']
        player_dict=ttt_game_list[link][2]
        keyboard = [
        [
            InlineKeyboardButton(" ", callback_data="c1r1//"+link),
            InlineKeyboardButton(" ", callback_data="c2r1//"+link),
            InlineKeyboardButton(" ", callback_data="c3r1//"+link),
        ],[
            InlineKeyboardButton(" ", callback_data="c1r2//"+link),
            InlineKeyboardButton(" ", callback_data="c2r2//"+link),
            InlineKeyboardButton(" ", callback_data="c3r2//"+link),
        ],[
            InlineKeyboardButton(" ", callback_data="c1r3//"+link),
            InlineKeyboardButton(" ", callback_data="c2r3//"+link),
            InlineKeyboardButton(" ", callback_data="c3r3//"+link),
        ]]
        ttt_game_list[link][1]['ttt_arena']=keyboard
        ttt_game_list[link][1]['ttt_game']=[['.','.','.'],
      
                       ['.','.','.'],

                       ['.','.','.']]
        ttt_game_list[link][1]['chance']=1
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        if player_dict['p1']!=[] and player_dict['p2']!=[]:
            text=player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
            if user_id in player_dict['admin']:
                query.edit_message_text(text, reply_markup=reply_markup)
            else:
                info_msg('You dont have any games in queue', update)
        else:
            info_msg('No players registered', update)


    elif 'c1r1' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        text = player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
        if ttt_game_list[link][1]['chance']%2==1 and user_id in ttt_game_list[link][2]['p1']:
            ttt_game_list[link][1]['ttt_game'][0][0]='x'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                    
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c1r1(ttt_game_list[link][1]['ttt_arena'],'p1')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p1 pressed c1r1')
                ttt_game_list[link][1]['chance']+=1

                if 'single' in data:
                        
                    if 'Normal' in player_dict['p2'][1]:
                        
                        resp = tictactoe.AI(ttt_game_list[link][1])
                        
                        ttt_game_list[link][1] = resp[0]
                        status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
                        
                        if 'playon' in status:
                            time.sleep(1)
                
                            game_markup2 = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                            
                            
                            query.edit_message_text(text=text, reply_markup=game_markup2)
                            print(f'AI pressed {resp[1]}')
                            ttt_game_list[link][1]['chance']+=1
                            
                        elif 'won' in status:
                            ttt_game_list[link][2]['p2'][2]+=1
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                                ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                                ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
                        
                        elif 'draw' in status:
                            ttt_game_list[link][2]['p1'][2]+=0.5
                            ttt_game_list[link][2]['p2'][2]+=0.5
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                            ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                            ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)

                        else:
                            'error'
                

                    elif 'Unbeatable' in player_dict['p2'][1]:
                        resp = tictactoe.AI(ttt_game_list[link][1], diff='unbeatable')
                    else:
                        'error'
                else:
                    query=query

            elif 'won' in status:
                ttt_game_list[link][2]['p1'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        elif ttt_game_list[link][1]['chance']%2==0 and user_id in ttt_game_list[link][2]['p2']:
            ttt_game_list[link][1]['ttt_game'][0][0]='o'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c1r1(ttt_game_list[link][1]['ttt_arena'],'p2')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p2 pressed c1r1')
                ttt_game_list[link][1]['chance']+=1
            elif 'won' in status:
                ttt_game_list[link][2]['p2'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p1'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        else:
            info_msg("Either its not your turn or you aren't playing", update)
    elif 'c1r2' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        text = player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
        if ttt_game_list[link][1]['chance']%2==1 and user_id in ttt_game_list[link][2]['p1']:
            ttt_game_list[link][1]['ttt_game'][1][0]='x'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c1r2(ttt_game_list[link][1]['ttt_arena'],'p1')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p1 pressed c1r2')
                ttt_game_list[link][1]['chance']+=1
                if 'single' in data:
                        
                    if 'Normal' in player_dict['p2'][1]:
                        
                        resp = tictactoe.AI(ttt_game_list[link][1])
                        
                        ttt_game_list[link][1] = resp[0]
                        status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
                        
                        if 'playon' in status:
                            time.sleep(1)
                
                            game_markup2 = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                            
                            
                            query.edit_message_text(text=text, reply_markup=game_markup2)
                            print(f'AI pressed {resp[1]}')
                            ttt_game_list[link][1]['chance']+=1
                            
                        elif 'won' in status:
                            ttt_game_list[link][2]['p2'][2]+=1
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                                ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                                ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
                        
                        elif 'draw' in status:
                            ttt_game_list[link][2]['p1'][2]+=0.5
                            ttt_game_list[link][2]['p2'][2]+=0.5
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                            ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                            ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)

                        else:
                            'error'
                

                    elif 'Unbeatable' in player_dict['p2'][1]:
                        resp = tictactoe.AI(ttt_game_list[link][1], diff='unbeatable')
                    else:
                        'error'
                else:
                    query=query
                
            elif 'won' in status:
                ttt_game_list[link][2]['p1'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        elif ttt_game_list[link][1]['chance']%2==0 and user_id in ttt_game_list[link][2]['p2']:
            ttt_game_list[link][1]['ttt_game'][1][0]='o'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c1r2(ttt_game_list[link][1]['ttt_arena'],'p2')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p2 pressed c1r2')
                ttt_game_list[link][1]['chance']+=1
                
            elif 'won' in status:
                ttt_game_list[link][2]['p2'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p1'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
        else:
            info_msg("Either its not your turn or you aren't playing", update)

    elif 'c1r3' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        text = player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
        if ttt_game_list[link][1]['chance']%2==1 and user_id in ttt_game_list[link][2]['p1']:
            ttt_game_list[link][1]['ttt_game'][2][0]='x'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c1r3(ttt_game_list[link][1]['ttt_arena'],'p1')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p1 pressed c1r3')
                ttt_game_list[link][1]['chance']+=1
                if 'single' in data:
                        
                    if 'Normal' in player_dict['p2'][1]:
                        
                        resp = tictactoe.AI(ttt_game_list[link][1])
                        
                        ttt_game_list[link][1] = resp[0]
                        status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
                        
                        if 'playon' in status:
                            time.sleep(1)
                
                            game_markup2 = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                            
                            
                            query.edit_message_text(text=text, reply_markup=game_markup2)
                            print(f'AI pressed {resp[1]}')
                            ttt_game_list[link][1]['chance']+=1
                            
                        elif 'won' in status:
                            ttt_game_list[link][2]['p2'][2]+=1
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                                ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                                ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
                        
                        elif 'draw' in status:
                            ttt_game_list[link][2]['p1'][2]+=0.5
                            ttt_game_list[link][2]['p2'][2]+=0.5
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                            ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                            ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)

                        else:
                            'error'
                

                    elif 'Unbeatable' in player_dict['p2'][1]:
                        resp = tictactoe.AI(ttt_game_list[link][1], diff='unbeatable')
                    else:
                        'error'
                else:
                    query=query
                
            elif 'won' in status:
                ttt_game_list[link][2]['p1'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
                
        elif ttt_game_list[link][1]['chance']%2==0 and user_id in ttt_game_list[link][2]['p2']:
            ttt_game_list[link][1]['ttt_game'][2][0]='o'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c1r3(ttt_game_list[link][1]['ttt_arena'],'p2')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p2 pressed c1r3')
                ttt_game_list[link][1]['chance']+=1
                
            elif 'won' in status:
                ttt_game_list[link][2]['p2'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p1'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'

        else:
            info_msg("Either its not your turn or you aren't playing", update)

    elif 'c2r1' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        text = player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
        if ttt_game_list[link][1]['chance']%2==1 and user_id in ttt_game_list[link][2]['p1']:
            ttt_game_list[link][1]['ttt_game'][0][1]='x'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c2r1(ttt_game_list[link][1]['ttt_arena'],'p1')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p1 pressed c2r1')
                ttt_game_list[link][1]['chance']+=1
                if 'single' in data:
                        
                    if 'Normal' in player_dict['p2'][1]:
                        
                        resp = tictactoe.AI(ttt_game_list[link][1])
                        
                        ttt_game_list[link][1] = resp[0]
                        status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
                        
                        if 'playon' in status:
                            time.sleep(1)
                
                            game_markup2 = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                            
                            
                            query.edit_message_text(text=text, reply_markup=game_markup2)
                            print(f'AI pressed {resp[1]}')
                            ttt_game_list[link][1]['chance']+=1
                            
                        elif 'won' in status:
                            ttt_game_list[link][2]['p2'][2]+=1
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                                ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                                ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
                        
                        elif 'draw' in status:
                            ttt_game_list[link][2]['p1'][2]+=0.5
                            ttt_game_list[link][2]['p2'][2]+=0.5
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                            ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                            ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)

                        else:
                            'error'
                

                    elif 'Unbeatable' in player_dict['p2'][1]:
                        resp = tictactoe.AI(ttt_game_list[link][1], diff='unbeatable')
                    else:
                        'error'
                else:
                    query=query
                
            elif 'won' in status:
                ttt_game_list[link][2]['p1'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        elif ttt_game_list[link][1]['chance']%2==0 and user_id in ttt_game_list[link][2]['p2']:
            ttt_game_list[link][1]['ttt_game'][0][1]='o'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c2r1(ttt_game_list[link][1]['ttt_arena'],'p2')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p2 pressed c2r1')
                ttt_game_list[link][1]['chance']+=1
                
            elif 'won' in status:
                ttt_game_list[link][2]['p2'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p1'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        else:
            info_msg("Either its not your turn or you aren't playing", update)

    elif 'c2r2' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        text = player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
        if ttt_game_list[link][1]['chance']%2==1 and user_id in ttt_game_list[link][2]['p1']:
            ttt_game_list[link][1]['ttt_game'][1][1]='x'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c2r2(ttt_game_list[link][1]['ttt_arena'],'p1')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p1 pressed c2r2')
                ttt_game_list[link][1]['chance']+=1
                if 'single' in data:
                        
                    if 'Normal' in player_dict['p2'][1]:
                        
                        resp = tictactoe.AI(ttt_game_list[link][1])
                        
                        ttt_game_list[link][1] = resp[0]
                        status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
                        
                        if 'playon' in status:
                            time.sleep(1)
                
                            game_markup2 = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                            
                            
                            query.edit_message_text(text=text, reply_markup=game_markup2)
                            print(f'AI pressed {resp[1]}')
                            ttt_game_list[link][1]['chance']+=1
                            
                        elif 'won' in status:
                            ttt_game_list[link][2]['p2'][2]+=1
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                                ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                                ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
                        
                        elif 'draw' in status:
                            ttt_game_list[link][2]['p1'][2]+=0.5
                            ttt_game_list[link][2]['p2'][2]+=0.5
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                            ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                            ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)

                        else:
                            'error'
                

                    elif 'Unbeatable' in player_dict['p2'][1]:
                        resp = tictactoe.AI(ttt_game_list[link][1], diff='unbeatable')
                    else:
                        'error'
                else:
                    query=query
                
            elif 'won' in status:
                ttt_game_list[link][2]['p1'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        elif ttt_game_list[link][1]['chance']%2==0 and user_id in ttt_game_list[link][2]['p2']:
            ttt_game_list[link][1]['ttt_game'][1][1]='o'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c2r2(ttt_game_list[link][1]['ttt_arena'],'p2')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p2 pressed c2r2')
                ttt_game_list[link][1]['chance']+=1
                
            elif 'won' in status:
                ttt_game_list[link][2]['p2'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p1'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        else:
            info_msg("Either its not your turn or you aren't playing", update)

    elif 'c2r3' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        text = player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
        if ttt_game_list[link][1]['chance']%2==1 and user_id in ttt_game_list[link][2]['p1']:
            ttt_game_list[link][1]['ttt_game'][2][1]='x'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c2r3(ttt_game_list[link][1]['ttt_arena'],'p1')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p1 pressed c2r3')
                ttt_game_list[link][1]['chance']+=1
                if 'single' in data:
                        
                    if 'Normal' in player_dict['p2'][1]:
                        
                        resp = tictactoe.AI(ttt_game_list[link][1])
                        
                        ttt_game_list[link][1] = resp[0]
                        status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
                        
                        if 'playon' in status:
                            time.sleep(1)
                
                            game_markup2 = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                            
                            
                            query.edit_message_text(text=text, reply_markup=game_markup2)
                            print(f'AI pressed {resp[1]}')
                            ttt_game_list[link][1]['chance']+=1
                            
                        elif 'won' in status:
                            ttt_game_list[link][2]['p2'][2]+=1
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                                ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                                ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
                        
                        elif 'draw' in status:
                            ttt_game_list[link][2]['p1'][2]+=0.5
                            ttt_game_list[link][2]['p2'][2]+=0.5
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                            ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                            ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)

                        else:
                            'error'
                

                    elif 'Unbeatable' in player_dict['p2'][1]:
                        resp = tictactoe.AI(ttt_game_list[link][1], diff='unbeatable')
                    else:
                        'error'
                else:
                    query=query
                
            elif 'won' in status:
                ttt_game_list[link][2]['p1'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        
        elif ttt_game_list[link][1]['chance']%2==0 and user_id in ttt_game_list[link][2]['p2']:
            ttt_game_list[link][1]['ttt_game'][2][1]='o'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c2r3(ttt_game_list[link][1]['ttt_arena'],'p2')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p2 pressed c2r3')
                ttt_game_list[link][1]['chance']+=1
                
            elif 'won' in status:
                ttt_game_list[link][2]['p2'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p1'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        else:
            info_msg("Either its not your turn or you aren't playing", update)
            
    elif 'c3r1' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        text = player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
        if ttt_game_list[link][1]['chance']%2==1 and user_id in ttt_game_list[link][2]['p1']:
            ttt_game_list[link][1]['ttt_game'][0][2]='x'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c3r1(ttt_game_list[link][1]['ttt_arena'],'p1')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p1 pressed c3r1')
                ttt_game_list[link][1]['chance']+=1
                if 'single' in data:
                        
                    if 'Normal' in player_dict['p2'][1]:
                        
                        resp = tictactoe.AI(ttt_game_list[link][1])
                        
                        ttt_game_list[link][1] = resp[0]
                        status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
                        
                        if 'playon' in status:
                            time.sleep(1)
                
                            game_markup2 = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                            
                            
                            query.edit_message_text(text=text, reply_markup=game_markup2)
                            print(f'AI pressed {resp[1]}')
                            ttt_game_list[link][1]['chance']+=1
                            
                        elif 'won' in status:
                            ttt_game_list[link][2]['p2'][2]+=1
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                                ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                                ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
                        
                        elif 'draw' in status:
                            ttt_game_list[link][2]['p1'][2]+=0.5
                            ttt_game_list[link][2]['p2'][2]+=0.5
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                            ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                            ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)

                        else:
                            'error'
                

                    elif 'Unbeatable' in player_dict['p2'][1]:
                        resp = tictactoe.AI(ttt_game_list[link][1], diff='unbeatable')
                    else:
                        'error'
                else:
                    query=query
                
            elif 'won' in status:
                ttt_game_list[link][2]['p1'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        elif ttt_game_list[link][1]['chance']%2==0 and user_id in ttt_game_list[link][2]['p2']:
            ttt_game_list[link][1]['ttt_game'][0][2]='o'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c3r1(ttt_game_list[link][1]['ttt_arena'],'p2')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p2 pressed c3r1')
                ttt_game_list[link][1]['chance']+=1
                
            elif 'won' in status:
                ttt_game_list[link][2]['p2'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p1'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        else:
            info_msg("Either its not your turn or you aren't playing", update)

    elif 'c3r2' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        text = player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
        if ttt_game_list[link][1]['chance']%2==1 and user_id in ttt_game_list[link][2]['p1']:
            ttt_game_list[link][1]['ttt_game'][1][2]='x'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c3r2(ttt_game_list[link][1]['ttt_arena'],'p1')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p1 pressed c3r2')
                ttt_game_list[link][1]['chance']+=1
                if 'single' in data:
                        
                    if 'Normal' in player_dict['p2'][1]:
                        
                        resp = tictactoe.AI(ttt_game_list[link][1])
                        
                        ttt_game_list[link][1] = resp[0]
                        status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
                        
                        if 'playon' in status:
                            time.sleep(1)
                
                            game_markup2 = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                            
                            
                            query.edit_message_text(text=text, reply_markup=game_markup2)
                            print(f'AI pressed {resp[1]}')
                            ttt_game_list[link][1]['chance']+=1
                            
                        elif 'won' in status:
                            ttt_game_list[link][2]['p2'][2]+=1
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                                ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                                ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
                        
                        elif 'draw' in status:
                            ttt_game_list[link][2]['p1'][2]+=0.5
                            ttt_game_list[link][2]['p2'][2]+=0.5
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                            ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                            ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)

                        else:
                            'error'
                

                    elif 'Unbeatable' in player_dict['p2'][1]:
                        resp = tictactoe.AI(ttt_game_list[link][1], diff='unbeatable')
                    else:
                        'error'
                else:
                    query=query
                
            elif 'won' in status:
                ttt_game_list[link][2]['p1'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        elif ttt_game_list[link][1]['chance']%2==0 and user_id in ttt_game_list[link][2]['p2']:
            ttt_game_list[link][1]['ttt_game'][1][2]='o'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c3r2(ttt_game_list[link][1]['ttt_arena'],'p2')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p2 pressed c3r2')
                ttt_game_list[link][1]['chance']+=1
                
            elif 'won' in status:
                ttt_game_list[link][2]['p2'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p1'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        else:
            info_msg("Either its not your turn or you aren't playing", update)

    elif 'c3r3' in data:
        link = data.split('//')[1]
        player_dict=ttt_game_list[link][2]
        user_id=user['id']
        text = player_dict['p1'][1]+ ' (❌)    VS   '+player_dict['p2'][1]+' (⭕)'
        if ttt_game_list[link][1]['chance']%2==1 and user_id in ttt_game_list[link][2]['p1']:
            ttt_game_list[link][1]['ttt_game'][2][2]='x'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c3r3(ttt_game_list[link][1]['ttt_arena'],'p1')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p1 pressed c3r3')
                ttt_game_list[link][1]['chance']+=1
                if 'single' in data:
                        
                    if 'Normal' in player_dict['p2'][1]:
                        
                        resp = tictactoe.AI(ttt_game_list[link][1])
                        
                        ttt_game_list[link][1] = resp[0]
                        status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
                        
                        if 'playon' in status:
                            time.sleep(1)
                
                            game_markup2 = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                            
                            
                            query.edit_message_text(text=text, reply_markup=game_markup2)
                            print(f'AI pressed {resp[1]}')
                            ttt_game_list[link][1]['chance']+=1
                            
                        elif 'won' in status:
                            ttt_game_list[link][2]['p2'][2]+=1
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                                ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                                ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
                        
                        elif 'draw' in status:
                            ttt_game_list[link][2]['p1'][2]+=0.5
                            ttt_game_list[link][2]['p2'][2]+=0.5
                            keyboard = [
                            [
                            InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                            ],
                            [
                            InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                            ],]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)

                        else:
                            'error'
                

                    elif 'Unbeatable' in player_dict['p2'][1]:
                        resp = tictactoe.AI(ttt_game_list[link][1], diff='unbeatable')
                    else:
                        'error'
                else:
                    query=query
                
            elif 'won' in status:
                ttt_game_list[link][2]['p1'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p2'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
            else:
                'error'
        elif ttt_game_list[link][1]['chance']%2==0 and user_id in ttt_game_list[link][2]['p2']:
            ttt_game_list[link][1]['ttt_game'][2][2]='o'
            status=tictactoe.checker(ttt_game_list[link][1]['ttt_game'], ttt_game_list[link][1]['chance'])
            if 'playon' in status:
                ttt_game_list[link][1]['ttt_arena']=tictactoe.c3r3(ttt_game_list[link][1]['ttt_arena'],'p2')
                game_markup = InlineKeyboardMarkup(ttt_game_list[link][1]['ttt_arena'])
                query.edit_message_text(text=text, reply_markup=game_markup)
                print('p2 pressed c3r3')
                ttt_game_list[link][1]['chance']+=1
                
            elif 'won' in status:
                ttt_game_list[link][2]['p2'][2]+=1
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict[status[1]][1]+' won!!! \n\nTake your revenge '+player_dict['p1'][1]+'... Have a rematch', reply_markup=reply_markup)                
            
            elif 'draw' in status:
                ttt_game_list[link][2]['p1'][2]+=0.5
                ttt_game_list[link][2]['p2'][2]+=0.5
                keyboard = [
                [
                    InlineKeyboardButton("PLAY AGAIN (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_again//'+link)),
                ],
                [
                    InlineKeyboardButton("END GAME (only for Admin i.e. "+ttt_game_list[link][2]['admin'][1]+')', callback_data=('ttt_end_admin//'+link)),
                ],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text=player_dict['p1'][1]+' and '+player_dict['p2'][1]+' drew \n\nSettle the debate... Have a rematch', reply_markup=reply_markup)
                
                
            else:
                'error'
        else:
            info_msg("Either its not your turn or you aren't playing", update)      
    
    elif data == 'hc_single':
        game_detail = { 'no_of_wickets':2, 'no_of_overs':2, 'teamA':'0/0/0.0', 'teamB':'0/0/0.0', 'scorecard':{ 'teamA':{}, 'teamB':{} } }
        link = assign_link(int(get_user_ID(update)),game_detail)
        hc_game_list[link][0] = 'started'
        hc_game_list[link][2].append('AI Bot')
        hc_game_list[link][3] = [hc_game_list[link][2][0]]
        hc_game_list[link][4] = ['AI Bot']
        query.edit_message_text("<i>Your Singleplayer Game has been created!</i>\n<b>Game ID :</b> " + link + "\n<b>Your Match will begin in 5 seconds.....</b>", parse_mode=telegram.ParseMode.HTML)
        time.sleep(5)
        query.edit_message_text("Gear Up ! It's the time for toss.....", parse_mode=telegram.ParseMode.HTML)
        time.sleep(3)
        keyboard = [
        [
                InlineKeyboardButton("Head", callback_data=("hc_head//" + link + "//" + hc_game_list[link][2][0] + "//" + hc_game_list[link][2][1])),
                InlineKeyboardButton("Tail", callback_data=("hc_tail//" + link + "//" + hc_game_list[link][2][0] + "//" + hc_game_list[link][2][1])),
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('<b>' + hc_game_list[link][2][0] + "</b> make your call for the toss.\nChoose Heads or Tails", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        
    elif data == 'hc_multi':
        game_detail = { 'no_of_wickets':2, 'no_of_overs':2, 'teamA':'0/0/0.0', 'teamB':'0/0/0.0', 'scorecard':{ 'teamA':{}, 'teamB':{} } }
        link = assign_link(int(get_user_ID(update)),game_detail)
        lis = hc_game_list[link][2]
        player_string = ""
        try:
            for i in range(1,len(lis)): # 0 index is for admin
                player_string += (str(userlist[int(get_user_ID(update))])).strip() + ", "
        except:
            player_string = ", "
        player_string = player_string[:-2]
        keyboard = [
            [
                InlineKeyboardButton("Start the Game (only for '" + str(hc_game_list[link][2][0]).strip() + "' )", callback_data=("start_hc//" + link)),
            ],[
                InlineKeyboardButton("Join the Game", callback_data=("add_hc//" + link))
            ],[
                InlineKeyboardButton("Leave the Game", callback_data=("remove_hc//" + link))
            ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("<i>Your Multiplayer Game has been created!</i>\n<b>Game ID :</b> " + link + "\nFor New players click on <b>'Join the Game'</b> to join the Game. New players cannot join once the Game starts.\nTo start the Game click on <b>'Start the Game'</b>. Only Admin of the Game can start the Game\n<b>Admin :</b> <i>" + (str(hc_game_list[link][2][0])).strip() + "</i>\n<b>Players :</b> <i>" + player_string + "</i>", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

    elif 'add_hc' in data:
        link = getlink(data)
        try:
            if hc_game_list[link][0] == 'lobby': # 'lobby' , 'started' , 'finished' only 3 possibility
                lis = hc_game_list[link][2]
                if userlist[get_user_ID(update)] not in lis:
                    hc_game_list[link][2] == hc_game_list[link][2].append(userlist[int(get_user_ID(update))])
                    admin = hc_game_list[link][2][0]
                    lis = hc_game_list[link][2]
                    player_string = ""
                    try:
                        for i in range(1,len(lis)): # 0 index is for admin
                            player_string += (str(lis[i])).strip() + ", "
                    except:
                        player_string = ", "
                    player_string = player_string[:-2]
                    keyboard = [
                        [
                        InlineKeyboardButton("Start the Game (only for '" + str(hc_game_list[link][2][0]).strip() + "' )", callback_data=("start_hc//" + link)),
                    ],[
                        InlineKeyboardButton("Join the Game", callback_data=("add_hc//" + link))
                    ],[
                        InlineKeyboardButton("Leave the Game", callback_data=("remove_hc//" + link))
                    ]]
                            
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    query.edit_message_text("<i>Your multiplayer Game has been created!</i>\n<b>Game ID :</b> " + link + "\nFor New players click on <b>'Join the Game'</b> to join the Game. New players cannot join once the Game starts.\nTo start the Game click on <b>'Start the Game'</b>. Only Admin of the Game can start the Game\n<b>Admin :</b> <i>" + (str(hc_game_list[link][2][0])).strip() + "</i>\n<b>Players :</b> <i>" + player_string + "</i>", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    save_dict('hc_game_list',hc_game_list)
                else:
                    info_msg('You are already in the Game',update)
            else:
                info_msg('You cannot join a Game which has already started!',update)
        except Exception as e:
            print(str(e))
            info_msg('The Game probably does not exists!',update)

    elif 'remove_hc' in data:
        link = getlink(data)
        try:
            if hc_game_list[link][0] == 'lobby': # 'lobby' , 'started' , 'finished' only 3 possibility
                lis = hc_game_list[link][2]
                if userlist[get_user_ID(update)] in lis:
                    hc_game_list[link][2] == hc_game_list[link][2].remove(userlist[int(get_user_ID(update))])
                    admin = hc_game_list[link][2][0]
                    lis = hc_game_list[link][2]
                    player_string = ""
                    try:
                        for i in range(1,len(lis)): # 0 index is for admin
                            player_string += (str(lis[i])).strip() + ", "
                    except:
                        player_string = ", "
                    player_string = player_string[:-2]
                    keyboard = [
                        [
                        InlineKeyboardButton("Start the Game (only for '" + str(hc_game_list[link][2][0]).strip() + "' )", callback_data=("start_hc//" + link)),
                    ],[
                        InlineKeyboardButton("Join the Game", callback_data=("add_hc//" + link))
                    ],[
                        InlineKeyboardButton("Leave the Game", callback_data=("remove_hc//" + link))
                    ]]
                            
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    query.edit_message_text("<i>Your multiplayer Game has been created!</i>\n<b>Game ID :</b> " + link + "\nFor New players click on <b>'Join the Game'</b> to join the Game. New players cannot join once the Game starts.\nTo start the Game click on <b>'Start the Game'</b>. Only Admin of the Game can start the Game\n<b>Admin :</b> <i>" + (str(hc_game_list[link][2][0])).strip() + "</i>\n<b>Players :</b> <i>" + player_string + "</i>", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    save_dict('hc_game_list',hc_game_list)
                else:
                    info_msg('You are already not in the Game',update)
            else:
                info_msg('You cannot leave a Game which has already started!',update)
        except Exception as e:
            print(str(e))
            info_msg('The Game probably does not exists!',update)
            
    elif 'start_hc' in data:
        link = getlink(data)
        if userlist[int(get_user_ID(update))] == hc_game_list[link][2][0]:
            try:
                if (len(hc_game_list[link][2])) % 2 == 0:
                    if (len(hc_game_list[link][2])) % hc_game_list[link][1]['no_of_wickets'] == 0 :
                        teams = shuffle_player(hc_game_list[link][2])
                        team1 = teams[0]
                        team2 = teams[1]
                        hc_game_list[link][3] = team1
                        hc_game_list[link][4] = team2
                        
                        str_team1 = ""
                        str_team2 = ""
                        
                        for i in range(0,len(team1)):
                            if i == 0:
                                str_team1 += (str(team1[i])).strip() + "</i><b>(c)</b><i>, "
                            elif i == (len(team1)-1):
                                str_team1 += (str(team1[i])).strip()
                            else:
                                str_team1 += (str(team1[i])).strip() +", "
                                
                        for i in range(0,len(team2)):
                            if i == 0:
                                str_team2 += (str(team2[i])).strip() + "</i><b>(c)</b><i>, "
                            elif i == (len(team2)-1):
                                str_team2 += (str(team2[i])).strip()
                            else:
                                str_team2 += (str(team2[i])).strip() +", " 
                        hc_game_list[link][0] = 'started'   
                        query.edit_message_text("<b>TeamA :</b> <i>" + str_team1 + "</i>\n<b>TeamB :</b> <i>" + str_team2 + "</i>\n<b>Your Match will begin in 10 seconds.....</b>", parse_mode=telegram.ParseMode.HTML)
                        time.sleep(10)
                        query.edit_message_text("Gear Up Everyone! It's the time for toss. Captains be ready!")
                        time.sleep(3)
                        x = random.randint(0,1)
                        if x == 0:
                            keyboard = [
                                [
                                    InlineKeyboardButton("Head", callback_data=("hc_head//" + link + "//" + teams[0][0] + "//" + teams[1][0])),
                                    InlineKeyboardButton("Tail", callback_data=("hc_tail//" + link + "//" + teams[0][0] + "//" + teams[1][0])),
                            ]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text('<b>' + teams[0][0] + "</b> make your call for the toss.\nChoose Heads or Tails", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                            
                        else:
                            keyboard = [
                                [
                                    InlineKeyboardButton("Head", callback_data=("hc_head//" + link + "//" + teams[1][0] + "//" + teams[0][0])),
                                    InlineKeyboardButton("Tail", callback_data=("hc_tail//" + link + "//" + teams[1][0] + "//" + teams[0][0])),
                            ]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.edit_message_text('<b>' + teams[1][0] + "</b> make your call for the toss.\nChoose Heads or Tails", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        info_msg('Error You cannot start the match because of mismatch between wickets and total number of players!',update)
                else:
                    info_msg('Total number of players should be even. Two Teams could not be formed from odd number of players!',update)
            except Exception as e:
                print(str(e))
                info_msg('An unexpected Error occured! Cannot start the match.....',update)
        else:
            info_msg('Only Admin of the Game can start the Game!',update)
            
    elif 'hc_head' in data:
        link = getlink(data)
        captain1 = data.split('//')[2]
        captain2 = data.split('//')[3]
        if userlist[get_user_ID(update)] == captain1:
            x = random.randint(0,1)
            if x == 0 :
                keyboard = [
                    [
                        InlineKeyboardButton("Bat", callback_data=("hc_bat//" + link + "//" + captain1 + '//' + captain2)),
                        InlineKeyboardButton("Bowl", callback_data=("hc_ball//" + link + "//" + captain1 + '//' + captain2)),
                ]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text('And the coin tosses mid in the air. It shows <b>Heads</b>!\n<b>' + captain1 + "</b> you won the toss.\n<b>" + captain1 + "</b>, you can now choose <i>Bat</i> or <i>Bowl</i>", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
            else :
                if captain2 == 'AI Bot':
                        y = random.randint(0,1)
                        if y == 0:
                                # Bot chooses to Bat
                                query.edit_message_text('And the coin tosses mid in the air. It shows <b>Tails</b>!\n<b>' + captain1 + "</b> you lost the toss.\n<b>" + captain2 + "</b> chooses to <i>Bat</i>", parse_mode=telegram.ParseMode.HTML)
                                hc_game_list[link] = [hc_game_list[link][0],hc_game_list[link][1],hc_game_list[link][2],hc_game_list[link][4],hc_game_list[link][3],hc_game_list[link][5],hc_game_list[link][6],hc_game_list[link][7],hc_game_list[link][8],hc_game_list[link][9]]
                                # InterChange is Required
                        elif y == 1:
                                # Bot chooses to Ball
                                query.edit_message_text('And the coin tosses mid in the air. It shows <b>Tails</b>!\n<b>' + captain1 + "</b> you lost the toss.\n<b>" + captain2 + "</b> chooses to <i>Ball</i>", parse_mode=telegram.ParseMode.HTML)
                                hc_game_list[link] = [hc_game_list[link][0],hc_game_list[link][1],hc_game_list[link][2],hc_game_list[link][3],hc_game_list[link][4],hc_game_list[link][5],hc_game_list[link][6],hc_game_list[link][7],hc_game_list[link][8],hc_game_list[link][9]]
                                # No interchange is Required
                        time.sleep(5)
                        keyboard = []
                        for i in hc_game_list[link][3]:
                                keyboard.append([InlineKeyboardButton(i,callback_data = ('hc_first_player_to_bat//' + link + '//' + str(i)))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text('<b>' + hc_game_list[link][3][0] + '</b> choose your first Batsman', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                else:
                        keyboard = [
                            [
                                InlineKeyboardButton("Bat", callback_data=("hc_bat//" + link + "//" + captain2 + '//' + captain1)),
                                InlineKeyboardButton("Bowl", callback_data=("hc_ball//" + link + "//" + captain2 + '//' + captain1)),
                        ]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text('And the coin tosses mid in the air. It shows <b>Tails</b>!\n<b>' + captain1 + "</b> you lost the toss.\n<b>" + captain2 + "</b>, you can now choose <i>Bat</i> or <i>Bowl</i>", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:
            if userlist[get_user_ID(update)] == captain2:
                info_msg(captain1 + ' is choosen for the toss',update)
            else:
                info_msg('You cannot click. You should be the Captain of your team',update)

    elif 'hc_tail' in data:
        link = getlink(data)
        captain1 = data.split('//')[2]
        captain2 = data.split('//')[3]
        if userlist[get_user_ID(update)] == captain1:
            x = random.randint(0,1)
            if x == 1:
                keyboard = [
                    [
                        InlineKeyboardButton("Bat", callback_data=("hc_bat//" + link + "//" + captain1 + '//' + captain2)),
                        InlineKeyboardButton("Bowl", callback_data=("hc_ball//" + link + "//" + captain1 + '//' + captain2)),
                ]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text('And the coin tosses mid in the air. It shows <b>Tails</b>!\n<b>' + captain1 + "</b> you won the toss.\n<b>" + captain1 + "</b>, you can now choose <i>Bat</i> or <i>Bowl</i>", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
            else :
                if captain2 == 'AI Bot':
                        y = random.randint(0,1)
                        if y == 0:
                                # Bot chooses to Bat
                                query.edit_message_text('And the coin tosses mid in the air. It shows <b>Tails</b>!\n<b>' + captain1 + "</b> you lost the toss.\n<b>" + captain2 + "</b> chooses to <i>Bat</i>", parse_mode=telegram.ParseMode.HTML)
                                hc_game_list[link] = [hc_game_list[link][0],hc_game_list[link][1],hc_game_list[link][2],hc_game_list[link][4],hc_game_list[link][3],hc_game_list[link][5],hc_game_list[link][6],hc_game_list[link][7],hc_game_list[link][8],hc_game_list[link][9]]
                                # InterChange is Required
                        elif y == 1:
                                # Bot chooses to Ball
                                query.edit_message_text('And the coin tosses mid in the air. It shows <b>Tails</b>!\n<b>' + captain1 + "</b> you lost the toss.\n<b>" + captain2 + "</b> chooses to <i>Ball</i>", parse_mode=telegram.ParseMode.HTML)
                                hc_game_list[link] = [hc_game_list[link][0],hc_game_list[link][1],hc_game_list[link][2],hc_game_list[link][3],hc_game_list[link][4],hc_game_list[link][5],hc_game_list[link][6],hc_game_list[link][7],hc_game_list[link][8],hc_game_list[link][9]]
                                # No interchange is Required
                        time.sleep(5)
                        keyboard = []
                        for i in hc_game_list[link][3]:
                                keyboard.append([InlineKeyboardButton(i,callback_data = ('hc_first_player_to_bat//' + link + '//' + str(i)))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text('<b>' + hc_game_list[link][3][0] + '</b> choose your first Batsman', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                else:
                        keyboard = [
                            [
                                InlineKeyboardButton("Bat", callback_data=("hc_bat//" + link + "//" + captain2 + '//' + captain1)),
                                InlineKeyboardButton("Bowl", callback_data=("hc_ball//" + link + "//" + captain2 + '//' + captain1)),
                        ]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text('And the coin tosses mid in the air. It shows <b>Heads</b>!\n<b>' + captain1 + " you lost the toss.\n<b>" + captain2 + "</b>, you can now choose <i>Bat</i> or <i>Bowl</i>", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:
            if userlist[get_user_ID(update)] == captain2:
                info_msg(captain1 + ' is choosen for the toss',update)
            else:
                info_msg('You cannot click. You should be the Captain of your team',update)

    elif 'hc_bat' in data:
        link = getlink(data)
        captain1 = data.split('//')[2]
        captain2 = data.split('//')[3]
        if userlist[get_user_ID(update)] == captain1:
            # now decide which team will be teamA and which will be teamB
            hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets'])
            if hc_game_list[link][3][0] != captain1:
                # teamB would be teamA
                hc_game_list[link] = [hc_game_list[link][0],hc_game_list[link][1],hc_game_list[link][2],hc_game_list[link][4],hc_game_list[link][3],hc_game_list[link][5],hc_game_list[link][6],hc_game_list[link][7],hc_game_list[link][8],hc_game_list[link][9]]
            else:
                hc_game_list[link] = [hc_game_list[link][0],hc_game_list[link][1],hc_game_list[link][2],hc_game_list[link][3],hc_game_list[link][4],hc_game_list[link][5],hc_game_list[link][6],hc_game_list[link][7],hc_game_list[link][8],hc_game_list[link][9]]
            keyboard = []
            for i in hc_game_list[link][3]:
                keyboard.append([InlineKeyboardButton(i,callback_data = ('hc_first_player_to_bat//' + link + '//' + str(i)))])
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text('<b>' + hc_game_list[link][3][0] + '</b> choose your first Batsman', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:
            if userlist[get_user_ID(update)] == captain2:
                info_msg('You lost the Toss. Now only ' + captain1 + ' will decide',update)
            else:
                info_msg('You cannot click. You should be the Captain of your team',update)
            
    elif 'hc_ball' in data:
        link = getlink(data)
        captain1 = data.split('//')[2]
        captain2 = data.split('//')[3]
        if userlist[get_user_ID(update)] == captain1:
            # now decide which team will be teamA and which will be teamB
            hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets'])
            if hc_game_list[link][3][0] != captain1:
                # teamB would be teamA
                hc_game_list[link] = [hc_game_list[link][0],hc_game_list[link][1],hc_game_list[link][2],hc_game_list[link][3],hc_game_list[link][4],hc_game_list[link][5],hc_game_list[link][6],hc_game_list[link][7],hc_game_list[link][8],hc_game_list[link][9]]
            else:
                hc_game_list[link] = [hc_game_list[link][0],hc_game_list[link][1],hc_game_list[link][2],hc_game_list[link][4],hc_game_list[link][3],hc_game_list[link][5],hc_game_list[link][6],hc_game_list[link][7],hc_game_list[link][8],hc_game_list[link][9]]                    
            keyboard = []
            for i in hc_game_list[link][3]:
                keyboard.append([InlineKeyboardButton(i,callback_data = ('hc_first_player_to_bat//' + link + '//' + str(i)))])
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text('<b>' + hc_game_list[link][3][0] + '</b> choose your first Batsman', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:
            if userlist[get_user_ID(update)] == captain2:
                info_msg('You lost the Toss. Now only ' + captain1 + ' will decide',update)
            else:
                info_msg('You cannot click. You should be the Captain of your team',update)

    elif 'hc_first_player_to_bat' in data:
        link = getlink(data)
        if hc_game_list[link][3][0] == 'AI Bot':
                hc_game_list[link][5] = ['AI Bot']
                keyboard = []
                for i in hc_game_list[link][4]:
                        keyboard.append([InlineKeyboardButton(i,callback_data = ('hc_first_player_to_ball//' + link + '//' + str(i)))])
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text('<b>' + hc_game_list[link][4][0] + '</b> choose your first Bowler', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:                
                if userlist[get_user_ID(update)] == hc_game_list[link][3][0]:
                    batsman = data.split('//')[2]
                    hc_game_list[link][5] = [batsman]
                    keyboard = []
                    for i in hc_game_list[link][4]:
                        keyboard.append([InlineKeyboardButton(i,callback_data = ('hc_first_player_to_ball//' + link + '//' + str(i)))])
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    query.edit_message_text('<b>' + hc_game_list[link][4][0] + '</b> choose your first Bowler', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                else:
                    info_msg('Only ' + hc_game_list[link][3][0] + ' is allowed to choose',update)

    elif 'hc_first_player_to_ball' in data:
        link = getlink(data)
        hc_game_list[link][7] = 'teamA'
        if hc_game_list[link][4][0] == 'AI Bot':
                hc_game_list[link][6] = ['AI Bot']
                no_display = [
                    [
                        InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                        InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                    InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                ],[
                        InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                        InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                    InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                ],]
                reply_markup = InlineKeyboardMarkup(no_display)
                query.edit_message_text('<i>Here we go.....</i>\n' + hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Selected)</b>', reply_markup=reply_markup,parse_mode=telegram.ParseMode.HTML)
                hc_game_list[link][6].append(random.randint(1,6))
        else:
                if hc_game_list[link][3][0] == 'AI Bot':
                        hc_game_list[link][6] = hc_game_list[link][2][0]
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text('<i>Here we go.....</i>\n' + hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Selected)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup,parse_mode=telegram.ParseMode.HTML)
                        hc_game_list[link][5].append(random.randint(1,6))
                else:
                        if userlist[get_user_ID(update)] == hc_game_list[link][4][0]:
                            bowler = data.split('//')[2]
                            hc_game_list[link][6] = [bowler]
                            # now we are ready to begin the game!!!!!!
                            no_display = [
                                [
                                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                            ],[
                                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                            ],]
                            reply_markup = InlineKeyboardMarkup(no_display)
                            query.edit_message_text('<i>Here we go.....</i>\n' + hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup,parse_mode=telegram.ParseMode.HTML)
                        else:
                            info_msg('Only ' + hc_game_list[link][4][0] + ' is allowed to choose',update)
            
    elif 'hc_new_batsman_bowler' in data:
        link = getlink(data)
        player = data.split('//')[2]
        keyboard = []
        list_bowler = get_bowler_list(link)
        if hc_game_list[link][7] == 'teamA':
                if  userlist[get_user_ID(update)] == hc_game_list[link][3][0]:
                        hc_game_list[link][5] = [player]
                        for i in list_bowler:
                                keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                else:
                        info_msg('Only ' + hc_game_list[link][3][0] + ' is allowed to choose',update)
        else:
                if  userlist[get_user_ID(update)] == hc_game_list[link][4][0]:
                        hc_game_list[link][5] = [player]
                        for i in list_bowler:
                                keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                else:
                        info_msg('Only ' + hc_game_list[link][4][0] + ' is allowed to choose',update)

    elif 'hc_new_innings_batsman_bowler' in data:
        link = getlink(data)
        player = data.split('//')[2]
        keyboard = []
        list_bowler = get_bowler_list(link)
        if userlist[get_user_ID(update)] == hc_game_list[link][4][0]:
            hc_game_list[link][5] = [player]
            for i in list_bowler:
                    keyboard.append([InlineKeyboardButton(i, callback_data="hc_new_innings_batsman_select_bowler//" + link + "//" + i)])
                    
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a opening bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:
            info_msg('Only ' + hc_game_list[link][4][0] + ' is allowed to choose',update)

    elif 'hc_new_innings_batsman_select_bowler' in data:
        link = getlink(data)
        player = data.split('//')[2]
        if userlist[get_user_ID(update)] == hc_game_list[link][3][0]:
                hc_game_list[link][6] = [player]
                no_display = [
                    [                        InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                        InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                    InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                ],[
                        InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                        InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                    InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                ],]
                reply_markup = InlineKeyboardMarkup(no_display)
                query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:
            info_msg('Only ' + hc_game_list[link][3][0] + ' is allowed to choose',update)
        

        
    elif 'hc_new_bowler' in data:
        link = getlink(data)
        player = data.split('//')[2]
        keyboard = []
        if hc_game_list[link][7] == 'teamA':
            if  userlist[get_user_ID(update)] == hc_game_list[link][4][0]:
                hc_game_list[link][6] = [player]
                no_display = [
                    [
                        InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                        InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                    InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                ],[
                        InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                        InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                    InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                ],]
                reply_markup = InlineKeyboardMarkup(no_display)
                query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            else:
                info_msg('Only ' + hc_game_list[link][4][0] + ' is allowed to choose',update)
        else:
            if userlist[get_user_ID(update)] == hc_game_list[link][3][0]:
                hc_game_list[link][6] = [player]
                no_display = [
                    [
                        InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                        InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                    InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                ],[
                        InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                        InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                    InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                ],]
                reply_markup = InlineKeyboardMarkup(no_display)
                query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            else:
                info_msg('Only ' + hc_game_list[link][3][0] + ' is allowed to choose',update)

    elif 'hc_new_batsman' in data:
        link = getlink(data)
        player = data.split('//')[2]
        keyboard = []
        if hc_game_list[link][7] == 'teamA':
            if  userlist[get_user_ID(update)] == hc_game_list[link][3][0]:
                hc_game_list[link][5] = [player]
                no_display = [
                    [
                        InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                        InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                    InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                ],[
                        InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                        InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                    InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                ],]
                reply_markup = InlineKeyboardMarkup(no_display)
                query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            else:
                info_msg('Only ' + hc_game_list[link][3][0] + ' is allowed to choose',update)
        else:
            if userlist[get_user_ID(update)] == hc_game_list[link][4][0]:
                hc_game_list[link][5] = [player]
                no_display = [
                    [
                        InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                        InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                    InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                ],[
                        InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                        InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                    InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                ],]
                reply_markup = InlineKeyboardMarkup(no_display)
                query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            else:
                info_msg('Only ' + hc_game_list[link][4][0] + ' is allowed to choose',update)
                
    elif 'hc_n1' in data:
        keyboard = []
        link = getlink(data)
        if userlist[get_user_ID(update)] == hc_game_list[link][5][0]:
            hc_game_list[link][5] = [hc_game_list[link][5][0],1]
        elif userlist[get_user_ID(update)] == hc_game_list[link][6][0]:
            hc_game_list[link][6] = [hc_game_list[link][6][0],1]
        else:
            info_msg('why are you clicking',update)
        if len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) == 2 :
            # now going for the handcricket file
            res = hand_cricket.init(game_detail = hc_game_list[link][1], batsman_no = hc_game_list[link][5][1], baller_no = hc_game_list[link][6][1], current_batsman = hc_game_list[link][5][0], current_bowler = hc_game_list[link][6][0], teamA_players = hc_game_list[link][3], teamB_players = hc_game_list[link][4])
            hc_game_list[link][1] = res['game_detail']
            if res['result'] == 'score increase':
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                        
            elif res['result'] == "new batsman":
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == "end of innings":
                display = 'With that it leads us to the <i>End of the First Innings......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b>Needs <b>' + str(res['scoreA']+1) + '</b> runs to WIN\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(7)
                hc_game_list[link][7] = 'teamB'
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                keyboard = []
                hc_game_list[link][9] = res['available_bowler']
                for i in res['available_batsman']:
                    keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_innings_batsman_bowler//" + link + "//" + i))])
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose opening Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == 'game_end':
                display = 'With that it leads us to the <i>End of the Game......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b><b>' + str(res['scoreA']+1) + '</b>\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(8)
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                if res['winner_by_team'] == 'teamA':
                    hc_game_list[link][8] = 'teamA//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamA</b> won the match by <b>" + str(res['win_by']) + '</b> runs!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    
                elif res['winner_by_team'] == 'teamB':
                    hc_game_list[link][8] = 'teamB//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamB</b> won the match by <b>" + str(res['win_by']) + '</b> wickets!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                
                else:
                    hc_game_list[link][8] = 'draw//' + str(0)
                    display = "With that it's the end of the Game!\n<b>It's a Draw. That was a close game!</b>\nTo view ScoreBoard of teams click on the button below....\n" + generate_sb(link,'teamA')


        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) == 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Selected)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    

        elif len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Selected)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    
         
        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    


    elif 'hc_n2' in data:
        keyboard = []
        link = getlink(data)
        if userlist[get_user_ID(update)] == hc_game_list[link][5][0]:
            hc_game_list[link][5] = [hc_game_list[link][5][0],2]
        elif userlist[get_user_ID(update)] == hc_game_list[link][6][0]:
            hc_game_list[link][6] = [hc_game_list[link][6][0],2]
        else:
            info_msg('why are you clicking',update)
        if len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) == 2 :
            res = hand_cricket.init(game_detail = hc_game_list[link][1], batsman_no = hc_game_list[link][5][1], baller_no = hc_game_list[link][6][1], current_batsman = hc_game_list[link][5][0], current_bowler = hc_game_list[link][6][0], teamA_players = hc_game_list[link][3], teamB_players = hc_game_list[link][4])
            hc_game_list[link][1] = res['game_detail']
            if res['result'] == 'score increase':
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                        
            elif res['result'] == "new batsman":
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == "end of innings":
                display = 'With that it leads us to the <i>End of the First Innings......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b>Needs <b>' + str(res['scoreA']+1) + '</b> runs to WIN\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(7)
                hc_game_list[link][7] = 'teamB'
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                keyboard = []
                hc_game_list[link][9] = res['available_bowler']
                for i in res['available_batsman']:
                    keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_innings_batsman_bowler//" + link + "//" + i))])
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose opening Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == 'game_end':
                display = 'With that it leads us to the <i>End of the Game......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b><b>' + str(res['scoreA']+1) + '</b>\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(8)
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                if res['winner_by_team'] == 'teamA':
                    hc_game_list[link][8] = 'teamA//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamA</b> won the match by <b>" + str(res['win_by']) + '</b> runs!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    
                elif res['winner_by_team'] == 'teamB':
                    hc_game_list[link][8] = 'teamB//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamB</b> won the match by <b>" + str(res['win_by']) + '</b> wickets!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                
                else:
                    hc_game_list[link][8] = 'draw//' + str(0)
                    display = "With that it's the end of the Game!\n<b>It's a Draw. That was a close game!</b>\nTo view ScoreBoard of teams click on the button below....\n" + generate_sb(link,'teamA')


        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) == 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Selected)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    

        elif len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Selected)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    
         
        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    

    elif 'hc_n3' in data:
        keyboard = []
        link = getlink(data)
        if userlist[get_user_ID(update)] == hc_game_list[link][5][0]:
            hc_game_list[link][5] = [hc_game_list[link][5][0],3]
        elif userlist[get_user_ID(update)] == hc_game_list[link][6][0]:
            hc_game_list[link][6] = [hc_game_list[link][6][0],3]
        else:
            info_msg('why are you clicking',update)
        if len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) == 2 :
            # now going for the handcricket file
            res = hand_cricket.init(game_detail = hc_game_list[link][1], batsman_no = hc_game_list[link][5][1], baller_no = hc_game_list[link][6][1], current_batsman = hc_game_list[link][5][0], current_bowler = hc_game_list[link][6][0], teamA_players = hc_game_list[link][3], teamB_players = hc_game_list[link][4])
            hc_game_list[link][1] = res['game_detail']
            if res['result'] == 'score increase':
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                        
            elif res['result'] == "new batsman":
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == "end of innings":
                display = 'With that it leads us to the <i>End of the First Innings......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b>Needs <b>' + str(res['scoreA']+1) + '</b> runs to WIN\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(7)
                hc_game_list[link][7] = 'teamB'
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                keyboard = []
                hc_game_list[link][9] = res['available_bowler']
                for i in res['available_batsman']:
                    keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_innings_batsman_bowler//" + link + "//" + i))])
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose opening Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == 'game_end':
                display = 'With that it leads us to the <i>End of the Game......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b><b>' + str(res['scoreA']+1) + '</b>\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(8)
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                if res['winner_by_team'] == 'teamA':
                    hc_game_list[link][8] = 'teamA//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamA</b> won the match by <b>" + str(res['win_by']) + '</b> runs!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    
                elif res['winner_by_team'] == 'teamB':
                    hc_game_list[link][8] = 'teamB//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamB</b> won the match by <b>" + str(res['win_by']) + '</b> wickets!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                
                else:
                    hc_game_list[link][8] = 'draw//' + str(0)
                    display = "With that it's the end of the Game!\n<b>It's a Draw. That was a close game!</b>\nTo view ScoreBoard of teams click on the button below....\n" + generate_sb(link,'teamA')


        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) == 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Selected)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    

        elif len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Selected)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    
         
        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    



    elif 'hc_n4' in data:
        keyboard = []
        link = getlink(data)
        if userlist[get_user_ID(update)] == hc_game_list[link][5][0]:
            hc_game_list[link][5] = [hc_game_list[link][5][0],4]
        elif userlist[get_user_ID(update)] == hc_game_list[link][6][0]:
            hc_game_list[link][6] = [hc_game_list[link][6][0],4]
        else:
            info_msg('why are you clicking',update)
        if len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) == 2 :
            # now going for the handcricket file
            res = hand_cricket.init(game_detail = hc_game_list[link][1], batsman_no = hc_game_list[link][5][1], baller_no = hc_game_list[link][6][1], current_batsman = hc_game_list[link][5][0], current_bowler = hc_game_list[link][6][0], teamA_players = hc_game_list[link][3], teamB_players = hc_game_list[link][4])
            hc_game_list[link][1] = res['game_detail']
            if res['result'] == 'score increase':
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                        
            elif res['result'] == "new batsman":
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup()
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == "end of innings":
                display = 'With that it leads us to the <i>End of the First Innings......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b>Needs <b>' + str(res['scoreA']+1) + '</b> runs to WIN\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(7)
                hc_game_list[link][7] = 'teamB'
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                keyboard = []
                hc_game_list[link][9] = res['available_bowler']
                for i in res['available_batsman']:
                    keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_innings_batsman_bowler//" + link + "//" + i))])
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose opening Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == 'game_end':
                display = 'With that it leads us to the <i>End of the Game......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b><b>' + str(res['scoreA']+1) + '</b>\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(8)
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                if res['winner_by_team'] == 'teamA':
                    hc_game_list[link][8] = 'teamA//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamA</b> won the match by <b>" + str(res['win_by']) + '</b> runs!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    
                elif res['winner_by_team'] == 'teamB':
                    hc_game_list[link][8] = 'teamB//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamB</b> won the match by <b>" + str(res['win_by']) + '</b> wickets!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                
                else:
                    hc_game_list[link][8] = 'draw//' + str(0)
                    display = "With that it's the end of the Game!\n<b>It's a Draw. That was a close game!</b>\nTo view ScoreBoard of teams click on the button below....\n" + generate_sb(link,'teamA')


        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) == 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Selected)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    

        elif len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Selected)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    
         
        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    


    elif 'hc_n5' in data:
        keyboard = []
        link = getlink(data)
        if userlist[get_user_ID(update)] == hc_game_list[link][5][0]:
            hc_game_list[link][5] = [hc_game_list[link][5][0],5]
        elif userlist[get_user_ID(update)] == hc_game_list[link][6][0]:
            hc_game_list[link][6] = [hc_game_list[link][6][0],5]
        else:
            info_msg('why are you clicking',update)
        if len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) == 2 :
            # now going for the handcricket file
            res = hand_cricket.init(game_detail = hc_game_list[link][1], batsman_no = hc_game_list[link][5][1], baller_no = hc_game_list[link][6][1], current_batsman = hc_game_list[link][5][0], current_bowler = hc_game_list[link][6][0], teamA_players = hc_game_list[link][3], teamB_players = hc_game_list[link][4])
            hc_game_list[link][1] = res['game_detail']
            if res['result'] == 'score increase':
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                        
            elif res['result'] == "new batsman":
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == "end of innings":
                display = 'With that it leads us to the <i>End of the First Innings......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b>Needs <b>' + str(res['scoreA']+1) + '</b> runs to WIN\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(7)
                hc_game_list[link][7] = 'teamB'
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                keyboard = []
                hc_game_list[link][9] = res['available_bowler']
                for i in res['available_batsman']:
                    keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_innings_batsman_bowler//" + link + "//" + i))])
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose opening Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == 'game_end':
                display = 'With that it leads us to the <i>End of the Game......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b><b>' + str(res['scoreA']+1) + '</b>\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(8)
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                if res['winner_by_team'] == 'teamA':
                    hc_game_list[link][8] = 'teamA//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamA</b> won the match by <b>" + str(res['win_by']) + '</b> runs!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    
                elif res['winner_by_team'] == 'teamB':
                    hc_game_list[link][8] = 'teamB//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamB</b> won the match by <b>" + str(res['win_by']) + '</b> wickets!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                
                else:
                    hc_game_list[link][8] = 'draw//' + str(0)
                    display = "With that it's the end of the Game!\n<b>It's a Draw. That was a close game!</b>\nTo view ScoreBoard of teams click on the button below....\n" + generate_sb(link,'teamA')

        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) == 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Selected)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    

        elif len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Selected)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    
         
        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    


    elif 'hc_n6' in data:
        keyboard = []
        link = getlink(data)
        if userlist[get_user_ID(update)] == hc_game_list[link][5][0]:
            hc_game_list[link][5] = [hc_game_list[link][5][0],6]
        elif userlist[get_user_ID(update)] == hc_game_list[link][6][0]:
            hc_game_list[link][6] = [hc_game_list[link][6][0],6]
        else:
            info_msg('why are you clicking',update)
        if len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) == 2 :
            # now going for the handcricket file
            res = hand_cricket.init(game_detail = hc_game_list[link][1], batsman_no = hc_game_list[link][5][1], baller_no = hc_game_list[link][6][1], current_batsman = hc_game_list[link][5][0], current_bowler = hc_game_list[link][6][0], teamA_players = hc_game_list[link][3], teamB_players = hc_game_list[link][4])
            hc_game_list[link][1] = res['game_detail']
            if res['result'] == 'score increase':
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        no_display = [
                            [
                                InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                                InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                            InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
                        ],[
                                InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                                InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                            InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
                        ],]
                        reply_markup = InlineKeyboardMarkup(no_display)
                        query.edit_message_text(hc_text[link] + '\n' + hc_game_list[link][5][0] + '<b>[Batting](Waiting)</b>\n' + hc_game_list[link][6][0] + '<b>[Balling](Waiting)</b>\n', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        for i in res['available_bowler']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][6][0] + "</b> choose a new Bowler", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                        
            elif res['result'] == "new batsman":
                if res['innings'] == 'teamA':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> Yet to Bat\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamA'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][3][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                elif res['innings'] == 'teamB':
                    display = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                    hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                    query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                    time.sleep(5)
                    hc_game_list[link][5].pop(1)
                    hc_game_list[link][6].pop(1)
                    hc_game_list[link][7] = 'teamB'
                    if res['over_change'] == False:
                        keyboard = []
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        keyboard = []
                        hc_game_list[link][9] = res['available_bowler']
                        for i in res['available_batsman']:
                            keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_batsman_bowler//" + link + "//" + i))])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose a new Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == "end of innings":
                display = 'With that it leads us to the <i>End of the First Innings......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b>Needs <b>' + str(res['scoreA']+1) + '</b> runs to WIN\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(7)
                hc_game_list[link][7] = 'teamB'
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                keyboard = []
                hc_game_list[link][9] = res['available_bowler']
                for i in res['available_batsman']:
                    keyboard.append([InlineKeyboardButton(i, callback_data=("hc_new_innings_batsman_bowler//" + link + "//" + i))])
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(hc_text[link] + '\n<b>' + hc_game_list[link][4][0] + "</b> choose opening Batsman", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

            elif res['result'] == 'game_end':
                display = 'With that it leads us to the <i>End of the Game......</i>\n<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB : </b><b>' + str(res['scoreA']+1) + '</b>\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate']) + '\n<b>' + hc_game_list[link][5][0] + "</b>'s number was : " + str(hc_game_list[link][5][1]) + "\n<b>" + hc_game_list[link][6][0] + "</b>'s number was : " + str(hc_game_list[link][6][1])
                hc_text[link] = '<b>TeamA :</b> ' + hc_game_list[link][1]['teamA'] + '\n<b>TeamB :</b> ' + hc_game_list[link][1]['teamB'] + '\n<b>No of Overs :</b> ' + str(hc_game_list[link][1]['no_of_overs']) + '\n<b>No of Wickets :</b> ' + str(hc_game_list[link][1]['no_of_wickets']) + '\n<b>Current Run Rate : </b>' + str(res['run_rateA']) + "\n<b>Required Run Rate :</b> " + str(res['req_run_rate'])
                query.edit_message_text(display, parse_mode=telegram.ParseMode.HTML)
                time.sleep(8)
                hc_game_list[link][5].pop(1)
                hc_game_list[link][6].pop(1)
                if res['winner_by_team'] == 'teamA':
                    hc_game_list[link][8] = 'teamA//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamA</b> won the match by <b>" + str(res['win_by']) + '</b> runs!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    
                elif res['winner_by_team'] == 'teamB':
                    hc_game_list[link][8] = 'teamB//' + str(res['win_by'])
                    display = "With that it's the end of the Game!\n<b>TeamB</b> won the match by <b>" + str(res['win_by']) + '</b> wickets!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
                    no_display = [
                        [
                            InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                            InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
                    ]]
                    reply_markup = InlineKeyboardMarkup(no_display)
                    query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                
                else:
                    hc_game_list[link][8] = 'draw//' + str(0)
                    display = "With that it's the end of the Game!\n<b>It's a Draw. That was a close game!</b>\nTo view ScoreBoard of teams click on the button below....\n" + generate_sb(link,'teamA')

                        
        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) == 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Selected)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    

        elif len(hc_game_list[link][5]) == 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Selected)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    
         
        elif len(hc_game_list[link][5]) != 2 and len(hc_game_list[link][6]) != 2:
            no_display = [
                [
                    InlineKeyboardButton("1", callback_data=("hc_n1//" + link)),
                    InlineKeyboardButton("2", callback_data=("hc_n2//" + link)),
                InlineKeyboardButton("3", callback_data=("hc_n3//" + link)),
            ],[
                    InlineKeyboardButton("4", callback_data=("hc_n4//" + link)),
                    InlineKeyboardButton("5", callback_data=("hc_n5//" + link)),
                InlineKeyboardButton("6", callback_data=("hc_n6//" + link)),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text(hc_text[link] + '\n<b>Batting :</b> <i>' + hc_game_list[link][5][0] + '</i> <b>(Waiting)</b>\n<b>Balling :</b> <i>' + hc_game_list[link][6][0] + '</i> <b>(Waiting)</b>', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)    

    elif 'sb_teamA' in data:
        link = getlink(data)
        x = hc_game_list[link][8]
        y = x.split('//')
        if y[0] == 'teamA':
            display = "With that it's the end of the Game!\n<b>TeamA</b> won the match by <b>" + y[1] + '</b> runs!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
        elif y[0] == 'teamB':
            display = "With that it's the end of the Game!\n<b>TeamB</b> won the match by <b>" + y[1] + '</b> wickets!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamA')
        else:
            display = "With that it's the end of the Game!\n<b>It's a Draw. That was a close game!</b>\nTo view ScoreBoard of teams click on the button below....\n" + generate_sb(link,'teamA')

        no_display = [
            [
                InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
        ]]
        reply_markup = InlineKeyboardMarkup(no_display)
        query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

    elif 'sb_teamB' in data:
        link = getlink(data)
        x = hc_game_list[link][8]
        y = x.split('//')
        if y[0] == 'teamA':
            display = "With that it's the end of the Game!\n<b>TeamA</b> won the match by <b>" + y[1] + '</b> runs!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamB')
        elif y[0] == 'teamB':
            display = "With that it's the end of the Game!\n<b>TeamB</b> won the match by <b>" + y[1] + '</b> wickets!' + '\nTo view ScoreBoard of teams click on the button below....\n' + generate_sb(link,'teamB')
        else:
            display = "With that it's the end of the Game!\n<b>It's a Draw. That was a close game!</b>\nTo view ScoreBoard of teams click on the button below....\n" + generate_sb(link,'teamB')

        no_display = [
            [
                InlineKeyboardButton("TeamA", callback_data=("sb_teamA//" + link )),
                InlineKeyboardButton("TeamB", callback_data=("sb_teamB//" + link )),
        ]]
        reply_markup = InlineKeyboardMarkup(no_display)
        query.edit_message_text(display, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)     

            
        '''
        #display all the handcricket tools
        no_display = [
            [
                InlineKeyboardButton("Head", callback_data="hc_head"),
                InlineKeyboardButton("Tail", callback_data="hc_tail"),
        ]]
        reply_markup = InlineKeyboardMarkup(no_display)
        query.edit_message_text("Ok now make your call for head or tail....", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

    elif data == 'hc_head':
        x = random.randint(1,2)
        if x == 1:
            no_display = [
                [
                    InlineKeyboardButton("Bat", callback_data="hc_bat"),
                    InlineKeyboardButton("Bowl", callback_data="hc_ball"),
            ]]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text("And that's head... You won the toss now choose batting or bowling", reply_markup = reply_markup)
        else:
            y = random.randint(1,2)
            if y == 1:
                query.edit_message_text("And that's tail... You lost the toss.\nComputer chooses to bat first")
                hc_list.append('Computer')
                hc_list.append('Human')
            else:
                query.edit_message_text("And that's tail... You lost the toss.\nComputer chooses to bowl first")
                hc_list.append('Human')
                hc_list.append('Computer')
            time.sleep(3)
            countdowntimer(query)

    elif data == 'hc_tail':
        x = random.randint(1,2)
        if x == 2:
            no_display = [
                [
                    InlineKeyboardButton("Bat", callback_data="hc_bat"),
                    InlineKeyboardButton("Bowl", callback_data="hc_ball"),
            ]]
            reply_markup = InlineKeyboardMarkup(no_display)
            query.edit_message_text("And that's tail... You won the toss now choose batting or bowling", reply_markup = reply_markup)
        else:
            y = random.randint(1,2)
            if y == 1:
                query.edit_message_text("And that's head... You lost the toss.\nComputer chooses to bat first\nMatch will begin shortly")
                hc_list.append('Computer')
                hc_list.append('Human')
            else:
                query.edit_message_text("And that's head... You lost the toss.\nComputer chooses to bowl first\nMatch will begin shortly")
                hc_list.append('Human')
                hc_list.append('Computer')
            time.sleep(3)
            countdowntimer(query)

    elif data == 'hc_bat':
        query.edit_message_text("You have choosen to bat first...\nMatch will begin shortly")
        hc_list.append('Human')
        hc_list.append('Computer')
        time.sleep(3)
        countdowntimer(query)

    elif data == 'hc_bowl':
        query.edit_message_text("You have choosen to bowl first...\nMatch will begin shortly")
        hc_list.append('Computer')
        hc_list.append('Human')
        time.sleep(3)
        countdowntimer(query)
        
    elif data=='hc_n1':
        if hc_list[0] == "Computer":
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,y,1,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        else:
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,1,y,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
            
    elif data=='hc_n2':
        if hc_list[0] == "Computer":
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,y,2,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        else:
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,2,y,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        
    elif data=='hc_n3':
        if hc_list[0] == "Computer":
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,y,3,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        else:
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,3,y,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        
    elif data=='hc_n4':
        if hc_list[0] == "Computer":
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,y,4,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        else:
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,4,y,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        
    elif data=='hc_n5':
        if hc_list[0] == "Computer":
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,y,5,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        else:
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,5,y,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        
    elif data=='hc_n6':
        if hc_list[0] == "Computer":
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,y,6,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        else:
            y = random.randint(1,6)
            res = hand_cricket.init(game_detail,6,y,hc_list[0],hc_list[1])
            if res['game_end']==True:
                game_end=True
            game_detail = res['game_detail']
        
    if game == 'hc':
        
        try:
            if game_end == False:
                print(game_detail)
                string = ""
                if res['innings'] == 'teamA':
                    string = hc_list[0] + " is batting ....." + '\n' + hc_list[0] + " : " + game_detail['teamA'] + '\n' + hc_list[1] + " : " + game_detail['teamB'] + '\n' + 'Current Run Rate : ' + str(res['run_rateA']) + '\n' + hc_list[0] + " number : " + str(res['numberA']) + '\n' + hc_list[1] + ' number : ' + str(res['numberB'])
                else:
                    string = hc_list[1] + " is batting ....." + '\n' + hc_list[1] + " : " + game_detail['teamB'] + '\n' + hc_list[0] + " : " + game_detail['teamA'] + '\n' + 'Current Run Rate : ' + str(res['run_rateB']) + '\n' + 'Required Run Rate : ' + str(res['req_run_rate']) + '\n' + hc_list[1] + " number : " + str(res['numberB']) + '\n' + hc_list[0] + ' number : ' + str(res['numberA'])     
                query.edit_message_text(text=string, reply_markup = reply_markup)
            else:
                if res['winner_by_team'] == 'teamA':
                    string = res['winner'] + " won the match by " + str(res['win_by']) + " runs"
                else:
                    string = res['winner'] + " won the match by " + str(res['win_by']) + " runs"
                query.edit_message_text(text=string, reply_markup = reply_markup)
                
        except Exception as e:
            print(str(e))
            # It will give error when res is not defined means that after count down it will come here and show up a error so now here we will just display blank scores

            no_display = [
                [
                    InlineKeyboardButton("1", callback_data="hc_n1"),
                    InlineKeyboardButton("2", callback_data="hc_n2"),
                InlineKeyboardButton("3", callback_data="hc_n3"),
            ],[
                    InlineKeyboardButton("4", callback_data="hc_n4"),
                    InlineKeyboardButton("5", callback_data="hc_n5"),
                InlineKeyboardButton("6", callback_data="hc_n6"),
            ],]
            reply_markup = InlineKeyboardMarkup(no_display)

            if hc_list[0] == 'Computer':
                query.edit_message_text("You are bowling please choose a number.......", reply_markup = reply_markup)
            else:
                query.edit_message_text("You are batting please choose a number.......", reply_markup = reply_markup)
                '''
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''Telegram Bot Launching'''

updater = Updater(API, use_context=True)
bot = telegram.Bot(token=API)
APPID = API
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''Adding Commands to the Bot'''
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('register', register))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
updater.dispatcher.add_handler(CommandHandler('play', display_all_game))
updater.dispatcher.add_handler(CallbackQueryHandler(game_handler))
updater.start_polling()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''Finally Printing Bot Ready to take Requests'''
print("Started Accepting Requests...")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
