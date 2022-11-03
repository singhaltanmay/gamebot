from telegram import InlineKeyboardButton

alpha_to_num = {
        'a' : 1,
        'b' : 2,
        'c' : 3,
        'd' : 4,
        'e' : 5,
        'f' : 6,
        'g' : 7,
        'h' : 8
        }

num_to_alpha = {
            0 : 'None',
            1 : 'a',
            2 : 'b',
            3 : 'c',
            4 : 'd',
            5 : 'e',
            6 : 'f',
            7 : 'g',
            8 : 'h',
            9 : 'None'
            }

piece_to_emoji = {
    'k':'♚',
    'q':'♛',
    'n':'♞',
    'b':'♝',
    'p':'♟',
    'r':'♜',
    'K':'♔',
    'Q':'♕',
    'N':'♘',
    'B':'♗',
    'P':'♙',
    'R':'♖',
    '.':' '
    }

def is_upper(string):
    if string == string.upper():
        return True
    else:
        return False

def is_lower(string):
    if string == string.lower():
        return True
    else:
        return False

def in_board(c1,c2):
    if c1 < 9 and c2 < 9 and c1 >0 and c2 > 0:
        return True
    else:
        return False

def count(list):
    m = {}
    for i in list:
        if i in m:
            m[i] = m[i] + 1
        else:
            m[i] = 1
    return m
        
def same_element(list):
    l = []
    for i in list:
        for j in i:
            l.append(j)
    m = []
    d = count(l)
    for i in d:
        if d[i] > 1:
            m.append(i)
    return m

def remove(lists,element):
    l = []
    if isinstance(element, list):
        for i in lists:
            if i not in element:
                l.append(i)
    else:
        for i in lists:
            if i!= element:
                l.append(i)
    return l

def replace(list,to_replace,replace_with):
    l = []
    for i in list:
        if i == to_replace:
            l.append(replace_with)
        else:
            l.append(i)
    return l

def diff_squares(list):
    l = []
    for i in list:
        l.append(i[0:1])
    to_stop = True
    x = count(l)
    for i in x:
        if x[i] > 1:
            to_stop = False
    if to_stop == True:
        return l
    else:
        l = []
        for i in list:
            l.append(i[-1:])
        to_stop = True
        x = count(l)
        for i in x:
            if x[i] > 1:
                to_stop = False
        if to_stop == True:
            return l
        else:
            return list

def board_to_fen(ranks):
    fen=''
    for rank in ranks:
        string=''
        i=0
        while i<8:
            piece=rank[i]
            if piece in 'RNBQKPrnbqkp':
                string+=piece
                i+=1
            
            elif piece=='.':
                nex=None
                for x in range(i+1,len(rank)):
                    if rank[x] in 'RNBQKPrnbqkp':
                        nex=x
                        break
                    else:
                        continue
                    
                if nex==None and i==0:
                    string+='8'
                    i=9
                elif nex==None and i!=0:
                    string+=str(8-i)
                    i=9
                else:
                    
                    string+=str(nex-i)
                    i=nex
        fen+=string+'/'
        continue
    fen=fen.rstrip(fen[-1])
    return fen

def fen_to_board(fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
    game_fen=fen.split(' ')[0]
    for i in game_fen:
        if i in '1 2 3 4 5 6 7 8':
            game_fen=game_fen.replace(i, '.'*int(i))
        else:
            i=i
            
    ranks=game_fen.split('/')
    rank8=list(ranks[0])
    rank7=list(ranks[1])
    rank6=list(ranks[2])
    rank5=list(ranks[3])
    rank4=list(ranks[4])
    rank3=list(ranks[5])
    rank2=list(ranks[6])
    rank1=list(ranks[7])
    ranks=[rank8, rank7, rank6, rank5, rank4, rank3, rank2, rank1]
    
    return ranks # 1,2,3... wale order mein hai (matlab bottom to top board)

def board_to_keyboard(ranks, link):
    global num_to_alpha
    global piece_to_emoji
    for x in range(len(ranks)):
        row=ranks[x]
        rank=str(8-x)
        for i in range(len(row)):
            file=num_to_alpha[i+1]
            row[i]=InlineKeyboardButton(piece_to_emoji[row[i]], callback_data='coords//'+row[i]+'//'+file+rank+'//'+link)
    return ranks

def FEN_to_List(board_FEN):
    # FEN has different rows seperated by ' '
    # First row : 4k2r/6r1/8/8/8/8/3R4/R3K3 (Indicating the pieces on the board)
    # Second row : w (Indicating whom to move as here white)
    # Third row : Qk (The "Qk" in the third field indicates that White may castle queenside and Black may castle kingside)
    # Fourth row : e3 (Means that pawn on e3 square can be captured by en passant)
    # If fourth row has '-' that means no pawn can be captured by en passant
    # Fifth row : 99 ( 'Halfmove Clock', Informs how many moves both players have made since the last pawn advance or piece capture)
    # If Halfmove Clock >= 100 game ends in a draw
    # Sixth row : 50 ( 'FullMove Number', The sixth and last field of the FEN code shows the number of completed turns in the game. This number is incremented by one every time Black moves)
    global num_to_alpha
    try :
        d = {
            'black_king' : '',
            'black_queen' : [],
            'black_bishop' : [],
            'black_knight' : [],
            'black_rook' : [],
            'black_pawn' : [],
            'white_king' : '',
            'white_queen' : [],
            'white_bishop' : [],
            'white_knight' : [],
            'white_rook' : [],
            'white_pawn' : [],
            'side_to_move' : '',
            'white_castle' : [],
            'black_castle' : [],
            'en_passant' : '',
            'halfmove' : '0',
            'fullmove' : '0'
            }
        
        
            
        row = board_FEN.split(' ')
        if (row[1]).strip().lower() == 'w':
            d['side_to_move'] = 'white'
        elif (row[1]).strip().lower() == 'b':
            d['side_to_move'] = 'black'
        else:
            return 'Invalid FEN'

        castle = (row[2]).strip()
        if 'Q' in castle:
            d['white_castle'].append('Q')
        if 'K' in castle:
            d['white_castle'].append('K')
        if 'q' in castle:
            d['black_castle'].append('q')
        if 'k' in castle:
            d['black_castle'].append('k')

        en = (row[3]).strip()
        if en == '-' or en == '--':
            d['en_passant'] = '-'
        else:
            d['en_passant'] = en

        half = int(row[4])
        full = int(row[5])
        d['halfmove'] = str(half)
        d['fullmove'] = str(full)
        s = (row[0]).split('/')
        for i in range(0,len(s)):
            if s[i].strip() != '8': # Do nothing if having 8
                x = list(s[i]) # Spliting every terms
                # Like 4k2r to '4','k','2','r'
                int_list = [] # list of index having integers
                
                for y in range(0,len(x)):
                    try:
                        x[y] = int(x[y])
                        int_list.append(y)
                    except:
                        pass
                vertical = i   
                for y in range(0,len(x)):
                    if y not in int_list:
                        horizontal = 0
                        for m in range(0,y+1):
                            if m in int_list:
                                horizontal += int(x[m])
                            else:
                                horizontal += 1
                        if x[y] == 'k':
                            d['black_king'] = num_to_alpha[horizontal] + str(8 - vertical)
                        elif x[y] == 'q':
                            (d['black_queen']).append(num_to_alpha[horizontal] + str(8 - vertical))
                        elif x[y] == 'b':
                            (d['black_bishop']).append(num_to_alpha[horizontal] + str(8 - vertical))
                        elif x[y] == 'n':
                            (d['black_knight']).append(num_to_alpha[horizontal] + str(8 - vertical))
                        elif x[y] == 'r':
                            (d['black_rook']).append(num_to_alpha[horizontal] + str(8 - vertical))
                        elif x[y] == 'p':
                            (d['black_pawn']).append(num_to_alpha[horizontal] + str(8 - vertical))
                            
                        elif x[y] == 'K':
                            d['white_king'] = num_to_alpha[horizontal] + str(8 - vertical)
                        elif x[y] == 'Q':
                            (d['white_queen']).append(num_to_alpha[horizontal] + str(8 - vertical))
                        elif x[y] == 'B':
                            (d['white_bishop']).append(num_to_alpha[horizontal] + str(8 - vertical))
                        elif x[y] == 'N':
                            (d['white_knight']).append(num_to_alpha[horizontal] + str(8 - vertical))
                        elif x[y] == 'R':
                            (d['white_rook']).append(num_to_alpha[horizontal] + str(8 - vertical))
                        elif x[y] == 'P':
                            (d['white_pawn']).append(num_to_alpha[horizontal] + str(8 - vertical))

                        else:
                            return 'Invalid FEN'
    except Exception as e:
        return 'Invalid FEN! Error : ' + str(e).upper()
    return d

def List_to_FEN(List):
    global num_to_alpha
    global alpha_to_num
    FEN = ''
    li = {
        8 : [],
        7 : [],
        6 : [],
        5 : [],
        4 : [],
        3 : [],
        2 : [],
        1 : []
        }
    
    li[int(list(List['black_king'])[1])].append(List['black_king'][0:1] + 'k')
    for i in List['black_queen']:
        li[int(list(i)[1])].append(i[0:1] + 'q')
    for i in List['black_bishop']:
        li[int(list(i)[1])].append(i[0:1] + 'b')
    for i in List['black_knight']:
        li[int(list(i)[1])].append(i[0:1] + 'n')
    for i in List['black_rook']:
        li[int(list(i)[1])].append(i[0:1] + 'r')
    for i in List['black_pawn']:
        li[int(list(i)[1])].append(i[0:1] + 'p')

    li[int(list(List['white_king'])[1])].append(List['white_king'][0:1] + 'K')
    for i in List['white_queen']:
        li[int(list(i)[1])].append(i[0:1] + 'Q')
    for i in List['white_bishop']:
        li[int(list(i)[1])].append(i[0:1] + 'B')
    for i in List['white_knight']:
        li[int(list(i)[1])].append(i[0:1] + 'N')
    for i in List['white_rook']:
        li[int(list(i)[1])].append(i[0:1] + 'R')
    for i in List['white_pawn']:
        li[int(list(i)[1])].append(i[0:1] + 'P')

    for i in li:
        if li[i] == []:
            FEN = FEN + '8/'
        else:
            l = li[i]
            l.sort()
            if len(l) == 1:
                num1 = (alpha_to_num[l[0][0:1]] - 1)
                num2 = (8 - alpha_to_num[l[0][0:1]])
                if num1 == 0:
                    if num2 == 0:
                        FEN = FEN + l[0][1:2] + '/'
                    else:
                        FEN = FEN + l[0][1:2] + str(num2) + '/'
                else:
                    if num2 == 0:
                        FEN = FEN + str(num1) + l[0][1:2] + '/'
                    else:
                        FEN = FEN + str(num1) + l[0][1:2] + str(num2) + '/'
            else:
                for j in range(0,len(l)):
                    if j == 0:
                        num = (alpha_to_num[l[j][0:1]] - 1)
                        if num == 0:
                            FEN = FEN + l[j][1:2]
                        else:
                            FEN = FEN + str(num) + l[j][1:2]
                    elif j == len(l) - 1:
                        num = (8 - alpha_to_num[l[j][0:1]])
                        if num == 0 :
                            FEN = FEN + l[j][1:2] + '/'
                        else:
                            FEN = FEN + l[j][1:2] + str(num) + '/'
                    else:
                        num = (alpha_to_num[l[j+1][0:1]] - alpha_to_num[l[j][0:1]] - 1)
                        if num == 0:
                            FEN = FEN + l[j][1:2]
                        else:
                            FEN = FEN + l[j][1:2] + str(num)
                            
    FEN = FEN[0:-1] # Removing last character as it has '/' in it

    if List['side_to_move'] == 'white':
        FEN = FEN + ' w'
    elif List['side_to_move'] == 'black':
        FEN = FEN + ' b'
    else:
        return "Invalid 'side_to_move'"

    string = ""

    for i in List['white_castle']:
        string = string + i.strip()
    for i in List['black_castle']:
        string = string + i.strip()

    FEN = FEN + ' ' + string.strip()

    FEN = FEN + ' ' + List['en_passant'].strip()
    FEN = FEN + ' ' + List['halfmove'].strip()
    FEN = FEN + ' ' + List['fullmove'].strip()

    return FEN
     
def piece_on_pos(board_List,position):
    for i in board_List:
        if i != 'halfmove' and i != 'fullmove':
            if position in board_List[i]:
                return i
    return None


def material_sq(board_List):
    x = board_List
    
    b = []
    
    b.append(x['black_king'])
    for i in x['black_queen']:
        if not i =="":
            b.append(i)
    for i in x['black_bishop']:
        if not i == "":
            b.append(i)
    for i in x['black_knight']:
        if not i == "":
            b.append(i)
    for i in x['black_rook']:
        if not i == "":
            b.append(i)
    for i in x['black_pawn']:
        if not i == "":
            b.append(i)

    w = []    
    w.append(x['white_king'])
    for i in x['white_queen']:
        if not i =="":
            w.append(i)
    for i in x['white_bishop']:
        if not i == "":
            w.append(i)
    for i in x['white_knight']:
        if not i == "":
            w.append(i)
    for i in x['white_rook']:
        if not i == "":
            w.append(i)
    for i in x['white_pawn']:
        if not i == "":
            w.append(i)

    return [w,b]





def board_after_move(board_List,move):
    global num_to_alpha
    global alpha_to_num
    move = (move.replace('e.p.','')).strip()
    move_sq = move[-2:]
    piece = move[0:1]
    if board_List['side_to_move'] == 'white':
        if piece != "K" and piece != "Q" and piece != "B" and piece != "N" and piece != "R":
            # It is a pawn move
            if "x" in move:
                #Here piece is representing file from which pawn departed
                pawn_depart_sq = ''
                capture_piece = piece_on_pos(board_List, position = move_sq)
                if move_sq == board_List['en_passant']:
                    board_List['white_pawn'] = replace(board_List['white_pawn'], to_replace = (move[0:1] + str(5)), replace_with = move_sq)
                    board_List['black_pawn'] = remove(board_List['black_pawn'], element = (move_sq[0:1] + str(5)))
                elif '=' in move:
                    promote_piece = move[-1:]
                    file = move[0:1]
                    move_sq = move[2:4]
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    if promote_piece.lower() == 'q':
                        board_List[capture_piece] = remove(board_List[capture_piece], element = move_sq)
                        board_List['white_pawn'] = remove(board_List['white_pawn'], element = (move[0:1] + str(7)))
                        board_List['white_queen'].append(move_sq)
                    elif promote_piece.lower() == 'r':
                        board_List[capture_piece] = remove(board_List[capture_piece], element = move_sq)
                        board_List['white_pawn'] = remove(board_List['white_pawn'], element = (move[0:1] + str(7)))
                        board_List['white_rook'].append(move_sq)
                    elif promote_piece.lower() == 'b':
                        board_List[capture_piece] = remove(board_List[capture_piece], element = move_sq)
                        board_List['white_pawn'] = remove(board_List['white_pawn'], element = (move[0:1] + str(7)))
                        board_List['white_bishop'].append(move_sq)
                    elif promote_piece.lower() == 'n':
                        board_List[capture_piece] = remove(board_List[capture_piece], element = move_sq)
                        board_List['white_pawn'] = remove(board_List['white_pawn'], element = (move[0:1] + str(7)))
                        board_List['white_knight'].append(move_sq)
                else:
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        
                        if i == 'white_pawn':
                            for j in board_List[i]:
                                if piece in j:
                                    if move_sq in pawn_sq(board_List,j):
                                        pawn_depart_sq = j
                                        break
                            board_List[i] = replace(board_List[i], to_replace = pawn_depart_sq, replace_with = move_sq)
                board_List['en_passant'] = '-'
                board_List['halfmove'] = '0'
                
            else:
                pawn_depart_sq = ''
                if '=' in move:
                    # This move is promoting a pawn to a piece
                    promote_piece = move[-1:]
                    move_sq = move[0:2]
                    if promote_piece.lower() == 'q':
                        board_List['white_pawn'] = remove(board_List['white_pawn'], element = (move[0:1] + str(7)))
                        board_List['white_queen'].append(move_sq)
                    elif promote_piece.lower() == 'r':
                        board_List['white_pawn'] = replace(board_List['white_pawn'], to_replace = (move[0:1] + str(7)))
                        board_List['white_rook'].append(move_sq)
                    elif promote_piece.lower() == 'n':
                        board_List['white_pawn'] = replace(board_List['white_pawn'], to_replace = (move[0:1] + str(7)))
                        board_List['white_knight'].append(move_sq)
                    if promote_piece.lower() == 'b':
                        board_List['white_pawn'] = replace(board_List['white_pawn'], to_replace = (move[0:1] + str(7)))
                        board_List['white_bishop'].append(move_sq)
                else:
                    for i in board_List:
                        if i == 'white_pawn':
                            for j in board_List[i]:
                                if piece in j:
                                    if move_sq in pawn_sq(board_List,j):
                                        pawn_depart_sq = j
                                        break
                            board_List[i] = replace(board_List[i], to_replace = pawn_depart_sq, replace_with = move_sq)

                    x = alpha_to_num[list(pawn_depart_sq)[0]]
                    if int(list(pawn_depart_sq)[1]) == 2:
                        if piece_on_pos(board_List,(str((num_to_alpha[x-1]) + str(4)))) == 'black_pawn' or piece_on_pos(board_List,(str((num_to_alpha[x+1]) + str(4)))) == 'black_pawn':
                            board_List['en_passant'] = str(num_to_alpha[x] + str(3))
                        else:
                            board_List['en_passant'] = '-'
                    else:
                        board_List['en_passant'] = '-'
                    board_List['halfmove'] = str(int(board_List['halfmove']) + 1)

            board_List['side_to_move'] = 'black'
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)
                    
        elif piece == 'K':
            if 'O-O-O' in move:
                board_List['white_king'] = 'c1'
                board_List['white_rook'] = replace(board_List['white_rook'], to_replace = 'a1', replace_with = 'd1')
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
            elif 'O-O' in move:
                board_List['white_king'] = 'g1'
                board_List['white_rook'] = replace(board_List['white_rook'], to_replace = 'h1', replace_with = 'f1')
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
            else:
                if "x" in move:
                    #Here piece is representing file from which King departed
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        king_depart_sq = ''
                        if i == 'white_king':
                            for j in board_List[i]:
                                    if move_sq in king_sq_without_castle(board_List, side = 'white'):
                                        king_depart_sq = j
                                        break
                            board_List[i] = move_sq
                    board_List['halfmove'] = '0'
                else:
                    king_depart_sq = ''
                    for i in board_List:
                        if i == 'white_king':
                            for j in board_List[i]:
                                    if move_sq in king_sq_without_castle(board_List, side = 'white'):
                                        king_depart_sq = j
                                        break
                            board_List[i] = move_sq
                    board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
                        
            board_List['en_passant'] = '-'
            board_List['side_to_move'] = 'black'
            board_List['white_castle'] = []
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)

        elif piece == 'B':
            
            if 'x' in move:
                if len(move) == 4:
                    bishop_depart_sq = ''
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['white_bishop']:
                            if move_sq in bishop_sq(board_List,j):
                                bishop_depart_sq = j
                    
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'white_bishop':
                            board_List[i] = replace(board_List[i], to_replace = bishop_depart_sq , replace_with = move_sq)

                elif len(move) == 5:
                    bishop_depart_sq = move[1:2]
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['white_bishop']:
                            if bishop_depart_sq in j:
                                if move_sq in bishop_sq(board_List,j):
                                    bishop_depart_sq = j

                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'white_bishop':
                            board_List[i] = replace(board_List[i], to_replace = bishop_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = '0'
                            
            else:
                
                if len(move) == 3:
                    bishop_depart_sq = ''
                    for j in board_List['white_bishop']:
                            if move_sq in bishop_sq(board_List,j):
                                bishop_depart_sq = j
                    
                    for i in board_List:
                        if i == 'white_bishop':
                            board_List[i] = replace(board_List[i], to_replace = bishop_depart_sq , replace_with = move_sq)

                elif len(move) == 4:
                    bishop_depart_sq = move[1:2]
                    for j in board_List['white_bishop']:
                            if bishop_depart_sq in j:
                                if move_sq in bishop_sq(board_List,j):
                                    bishop_depart_sq = j

                    for i in board_List:
                        if i == 'white_bishop':
                            board_List[i] = replace(board_List[i], to_replace = bishop_depart_sq , replace_with = move_sq)
                    
                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
                        
            board_List['en_passant'] = '-'
            board_List['side_to_move'] = 'black'
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)

                
        elif piece == 'Q':
            
            if 'x' in move:
                if len(move) == 4:
                    queen_depart_sq = ''
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['white_queen']:
                            if move_sq in queen_sq(board_List,j):
                                queen_depart_sq = j
                    
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'white_queen':
                            board_List[i] = replace(board_List[i], to_replace = queen_depart_sq , replace_with = move_sq)
                elif len(move) == 5:
                    queen_depart_sq = move[1:2]
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['white_queen']:
                            if queen_depart_sq in j:
                                if move_sq in queen_sq(board_List,j):
                                    queen_depart_sq = j

                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'white_queen':
                            board_List[i] = replace(board_List[i], to_replace = queen_depart_sq , replace_with = move_sq)
        
                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = '0'
                            
            else:
                
                if len(move) == 3:
                    queen_depart_sq = ''
                    for j in board_List['white_queen']:
                            if move_sq in queen_sq(board_List,j):
                                queen_depart_sq = j
                    
                    for i in board_List:
                        if i == 'white_queen':
                            board_List[i] = replace(board_List[i], to_replace = queen_depart_sq , replace_with = move_sq)

                elif len(move) == 4:
                    queen_depart_sq = move[1:2]
                    for j in board_List['white_queen']:
                            if queen_depart_sq in j:
                                if move_sq in queen_sq(board_List,j):
                                    queen_depart_sq = j

                    for i in board_List:
                        if i == 'white_queen':
                            board_List[i] = replace(board_List[i], to_replace = queen_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
                        
            board_List['en_passant'] = '-'
            board_List['side_to_move'] = 'black'
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)


        elif piece == 'N':
            
            if 'x' in move:
                if len(move) == 4:
                    knight_depart_sq = ''
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['white_knight']:
                            if move_sq in knight_sq(board_List,j):
                                knight_depart_sq = j
                    
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'white_knight':
                            board_List[i] = replace(board_List[i], to_replace = knight_depart_sq , replace_with = move_sq)

                elif len(move) == 5:
                    knight_depart_sq = move[1:2]
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['white_knight']:
                            if knight_depart_sq in j:
                                if move_sq in knight_sq(board_List,j):
                                    knight_depart_sq = j

                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'white_knight':
                            board_List[i] = replace(board_List[i], to_replace = knight_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = '0'
                            
            else:
                
                if len(move) == 3:
                    knight_depart_sq = ''
                    for j in board_List['white_knight']:
                            if move_sq in knight_sq(board_List,j):
                                knight_depart_sq = j
                    
                    for i in board_List:
                        if i == 'white_knight':
                            board_List[i] = replace(board_List[i], to_replace = knight_depart_sq , replace_with = move_sq)

                elif len(move) == 4:
                    knight_depart_sq = move[1:2]
                    for j in board_List['white_knight']:
                            if knight_depart_sq in j:
                                if move_sq in knight_sq(board_List,j):
                                    knight_depart_sq = j

                    for i in board_List:
                        if i == 'white_knight':
                            board_List[i] = replace(board_List[i], to_replace = knight_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
                        
            board_List['en_passant'] = '-'
            board_List['side_to_move'] = 'black'
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)


        elif piece == 'R':

            if 'x' in move:
                if len(move) == 4:
                    rook_depart_sq = ''
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['white_rook']:
                            if move_sq in rook_sq(board_List,j):
                                rook_depart_sq = j
                    
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'white_rook':
                            board_List[i] = replace(board_List[i], to_replace = rook_depart_sq , replace_with = move_sq)

                elif len(move) == 5:
                    rook_depart_sq = move[1:2]
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['white_rook']:
                            if rook_depart_sq in j:
                                if move_sq in rook_sq(board_List,j):
                                    rook_depart_sq = j

                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'white_rook':
                            board_List[i] = replace(board_List[i], to_replace = rook_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = '0'
                            
            else:
                
                if len(move) == 3:
                    rook_depart_sq = ''
                    for j in board_List['white_rook']:
                            if move_sq in rook_sq(board_List,j):
                                rook_depart_sq = j
                    
                    for i in board_List:
                        if i == 'white_rook':
                            board_List[i] = replace(board_List[i], to_replace = rook_depart_sq , replace_with = move_sq)

                elif len(move) == 4:
                    rook_depart_sq = move[1:2]
                    for j in board_List['white_rook']:
                        for j in i:
                            if rook_depart_sq in j:
                                if move_sq in rook_sq(board_List,j):
                                    rook_depart_sq = j

                    for i in board_List:
                        if i == 'white_rook':
                            board_List[i] = replace(board_List[i], to_replace = rook_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
                        
            board_List['en_passant'] = '-'
            board_List['side_to_move'] = 'black'
            white_castle = board_List['white_castle']
            if rook_depart_sq == 'a1':
                white_castle = remove(white_castle, element = 'Q')
            if rook_depart_sq == 'h1':
                white_castle = remove(white_castle, element = 'K')
            board_List['white_castle'] = white_castle
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)


    elif board_List['side_to_move'] == 'black':
        if piece != "K" and piece != "Q" and piece != "B" and piece != "N" and piece != "R":
            # It is a pawn move
            if "x" in move:
                #Here piece is representing file from which pawn departed
                pawn_depart_sq = ''
                capture_piece = piece_on_pos(board_List, position = move_sq)
                if move_sq == board_List['en_passant']:
                    board_List['black_pawn'] = replace(board_List['black_pawn'], to_replace = (move[0:1] + str(5)), replace_with = move_sq)
                    board_List['white_pawn'] = remove(board_List['white_pawn'], element = (move_sq[0:1] + str(5)))
                elif '=' in move:
                    promote_piece = move[-1:]
                    file = move[0:1]
                    move_sq = move[2:4]
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    if promote_piece.lower() == 'q':
                        board_List[capture_piece] = remove(board_List[capture_piece], element = move_sq)
                        board_List['black_pawn'] = remove(board_List['black_pawn'], element = (move[0:1] + str(2)))
                        board_List['black_queen'].append(move_sq)
                    elif promote_piece.lower() == 'r':
                        board_List[capture_piece] = remove(board_List[capture_piece], element = move_sq)
                        board_List['black_pawn'] = remove(board_List['black_pawn'], element = (move[0:1] + str(2)))
                        board_List['black_rook'].append(move_sq)
                    elif promote_piece.lower() == 'b':
                        board_List[capture_piece] = remove(board_List[capture_piece], element = move_sq)
                        board_List['black_pawn'] = remove(board_List['black_pawn'], element = (move[0:1] + str(2)))
                        board_List['black_bishop'].append(move_sq)
                    elif promote_piece.lower() == 'n':
                        board_List[capture_piece] = remove(board_List[capture_piece], element = move_sq)
                        board_List['black_pawn'] = remove(board_List['black_pawn'], element = (move[0:1] + str(2)))
                        board_List['black_knight'].append(move_sq)
                    
                else:
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        
                        if i == 'black_pawn':
                            for j in board_List[i]:
                                if piece in j:
                                    if move_sq in pawn_sq(board_List,j):
                                        pawn_depart_sq = j
                                        break
                            board_List[i] = replace(board_List[i], to_replace = pawn_depart_sq, replace_with = move_sq)
                
                board_List['en_passant'] = '-'
                board_List['halfmove'] = '0'
                
            else:
                pawn_depart_sq = ''
                if '=' in move:
                    # This move is promoting a pawn to a piece
                    promote_piece = move[-2:]
                    move_sq = move[0:2]
                    if promote_piece.lower() == 'q':
                        board_List['black_pawn'] = remove(board_List['black_pawn'], element = (move[0:1] + str(2)))
                        board_List['black_queen'].append(move_sq)
                    elif promote_piece.lower() == 'r':
                        board_List['black_pawn'] = remove(board_List['black_pawn'], element = (move[0:1] + str(2)))
                        board_List['black_rook'].append(move_sq)
                    elif promote_piece.lower() == 'n':
                        board_List['black_pawn'] = remove(board_List['black_pawn'], element = (move[0:1] + str(2)))
                        board_List['black_knight'].append(move_sq)
                    if promote_piece.lower() == 'b':
                        board_List['black_pawn'] = remove(board_List['black_pawn'], element = (move[0:1] + str(2)))
                        board_List['black_bishop'].append(move_sq)
                else:
                    for i in board_List:
                        if i == 'black_pawn':
                            for j in board_List[i]:
                                if piece in j:
                                    if move_sq in pawn_sq(board_List,j):
                                        pawn_depart_sq = j
                                        break
                            board_List[i] = replace(board_List[i], to_replace = pawn_depart_sq, replace_with = move_sq)
                    x = alpha_to_num[list(pawn_depart_sq)[0]]
                    if int(list(pawn_depart_sq)[1]) == 7:
                        if piece_on_pos(board_List,(str((num_to_alpha[x-1]) + str(5)))) == 'white_pawn' or piece_on_pos(board_List,(str((num_to_alpha[x+1]) + str(5)))) == 'white_pawn':
                            board_List['en_passant'] = str(num_to_alpha[x] + str(6))
                        else:
                            board_List['en_passant'] = '-'
                    else:
                        board_List['en_passant'] = '-'
                    board_List['halfmove'] = str(int(board_List['halfmove']) + 1)

            board_List['side_to_move'] = 'white'
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)
                    
        elif piece == 'K':
            
            if 'O-O-O' in move:
                board_List['white_king'] = 'c8'
                board_List['white_rook'] = replace(board_List['white_rook'], to_replace = 'a8', replace_with = 'd8')
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
            elif 'O-O' in move:
                board_List['white_king'] = 'g8'
                board_List['white_rook'] = replace(board_List['white_rook'], to_replace = 'h8', replace_with = 'f8')
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
            else:
                if "x" in move:
                    #Here piece is representing file from which King departed
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        kinb_depart_sq = ''
                        if i == 'black_king':
                            for j in board_List[i]:
                                    if move_sq in king_sq_without_castle(board_List, side = 'black'):
                                        kinb_depart_sq = j
                                        break
                            board_List[i] = move_sq
                    board_List['halfmove'] = '0'
                    
                else:
                    king_depart_sq = ''
                    for i in board_List:
                        if i == 'black_king':
                            for j in board_List[i]:
                                    if move_sq in king_sq_without_castle(board_List, side = 'black'):
                                        king_depart_sq = j
                                        break
                            board_List[i] = move_sq
                    board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
                        
            board_List['en_passant'] = '-'
            board_List['side_to_move'] = 'white'
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)

        elif piece == 'B':
            
            if 'x' in move:
                if len(move) == 4:
                    bishop_depart_sq = ''
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['black_bishop']:
                            if move_sq in bishop_sq(board_List,j):
                                bishop_depart_sq = j
                    
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'black_bishop':
                            board_List[i] = replace(board_List[i], to_replace = bishop_depart_sq , replace_with = move_sq)

                elif len(move) == 5:
                    bishop_depart_sq = move[1:2]
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['black_bishop']:
                            if bishop_depart_sq in j:
                                if move_sq in bishop_sq(board_List,j):
                                    bishop_depart_sq = j

                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'black_bishop':
                            board_List[i] = replace(board_List[i], to_replace = bishop_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = '0'
                            
            else:
                
                if len(move) == 3:
                    bishop_depart_sq = ''
                    for j in board_List['black_bishop']:
                            if move_sq in bishop_sq(board_List,j):
                                bishop_depart_sq = j
                    
                    for i in board_List:
                        if i == 'black_bishop':
                            board_List[i] = replace(board_List[i], to_replace = bishop_depart_sq , replace_with = move_sq)

                elif len(move) == 4:
                    bishop_depart_sq = move[1:2]
                    for j in board_List['black_bishop']:
                            if bishop_depart_sq in j:
                                if move_sq in bishop_sq(board_List,j):
                                    bishop_depart_sq = j

                    for i in board_List:
                        if i == 'black_bishop':
                            board_List[i] = replace(board_List[i], to_replace = bishop_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
                        
            board_List['en_passant'] = '-'
            board_List['side_to_move'] = 'white'
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)
                
        elif piece == 'Q':
            
            if 'x' in move:
                if len(move) == 4:
                    queen_depart_sq = ''
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['black_queen']:
                            if move_sq in queen_sq(board_List,j):
                                queen_depart_sq = j
                    
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'black_queen':
                            board_List[i] = replace(board_List[i], to_replace = queen_depart_sq , replace_with = move_sq)

                elif len(move) == 5:
                    queen_depart_sq = move[1:2]
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['black_queen']:
                            if queen_depart_sq in j:
                                if move_sq in queen_sq(board_List,j):
                                    queen_depart_sq = j

                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'black_queen':
                            board_List[i] = replace(board_List[i], to_replace = queen_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = '0'
                            
            else:
                
                if len(move) == 3:
                    queen_depart_sq = ''
                    for j in board_List['black_queen']:
                            if move_sq in queen_sq(board_List,j):
                                queen_depart_sq = j
                    
                    for i in board_List:
                        if i == 'black_queen':
                            board_List[i] = replace(board_List[i], to_replace = queen_depart_sq , replace_with = move_sq)

                elif len(move) == 4:
                    queen_depart_sq = move[1:2]
                    for j in board_List['black_queen']:
                            if queen_depart_sq in j:
                                if move_sq in queen_sq(board_List,j):
                                    queen_depart_sq = j

                    for i in board_List:
                        if i == 'black_queen':
                            board_List[i] = replace(board_List[i], to_replace = queen_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
                        
            board_List['en_passant'] = '-'
            board_List['side_to_move'] = 'white'
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)

        elif piece == 'N':
            
            if 'x' in move:
                if len(move) == 4:
                    knight_depart_sq = ''
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['black_knight']:
                            if move_sq in knight_sq(board_List,j):
                                knight_depart_sq = j
                    
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'black_knight':
                            board_List[i] = replace(board_List[i], to_replace = knight_depart_sq , replace_with = move_sq)

                elif len(move) == 5:
                    knight_depart_sq = move[1:2]
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['black_knight']:
                            if knight_depart_sq in j:
                                if move_sq in knight_sq(board_List,j):
                                    knight_depart_sq = j

                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'black_knight':
                            board_List[i] = replace(board_List[i], to_replace = knight_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = '0'
                            
            else:
                
                if len(move) == 3:
                    knight_depart_sq = ''
                    for j in board_List['black_knight']:
                            if move_sq in knight_sq(board_List,j):
                                knight_depart_sq = j
                    
                    for i in board_List:
                        if i == 'black_knight':
                            board_List[i] = replace(board_List[i], to_replace = knight_depart_sq , replace_with = move_sq)

                elif len(move) == 4:
                    knight_depart_sq = move[1:2]
                    for j in board_List['black_knight']:
                            if knight_depart_sq in j:
                                if move_sq in knight_sq(board_List,j):
                                    knight_depart_sq = j

                    for i in board_List:
                        if i == 'black_knight':
                            board_List[i] = replace(board_List[i], to_replace = knight_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
                        
            board_List['en_passant'] = '-'
            board_List['side_to_move'] = 'white'
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)

        elif piece == 'R':

            if 'x' in move:
                if len(move) == 4:
                    rook_depart_sq = ''
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['black_rook']:
                            if move_sq in rook_sq(board_List,j):
                                rook_depart_sq = j
                    
                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'black_rook':
                            board_List[i] = replace(board_List[i], to_replace = rook_depart_sq , replace_with = move_sq)

                elif len(move) == 5:
                    rook_depart_sq = move[1:2]
                    capture_piece = piece_on_pos(board_List, position = move_sq)
                    for j in board_List['black_rook']:
                            if rook_depart_sq in j:
                                if move_sq in rook_sq(board_List,j):
                                    rook_depart_sq = j

                    for i in board_List:
                        if i == capture_piece:
                            board_List[i] = remove(board_List[i], element = move_sq)
                        if i == 'black_rook':
                            board_List[i] = replace(board_List[i], to_replace = rook_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = '0'
                            
            else:
                
                if len(move) == 3:
                    rook_depart_sq = ''
                    for j in board_List['black_rook']:
                            if move_sq in rook_sq(board_List,j):
                                rook_depart_sq = j
                    
                    for i in board_List:
                        if i == 'black_rook':
                            board_List[i] = replace(board_List[i], to_replace = rook_depart_sq , replace_with = move_sq)

                elif len(move) == 4:
                    rook_depart_sq = move[1:2]
                    for j in board_List['black_rook']:
                            if rook_depart_sq in j:
                                if move_sq in rook_sq(board_List,j):
                                    rook_depart_sq = j

                    for i in board_List:
                        if i == 'black_rook':
                            board_List[i] = replace(board_List[i], to_replace = rook_depart_sq , replace_with = move_sq)

                else:
                    return "Can't Recognise Move"
                board_List['halfmove'] = str(int(board_List['halfmove']) + 1)
                
            board_List['en_passant'] = '-'
            board_List['side_to_move'] = 'black'
            black_castle = board_List['black_castle']
            if rook_depart_sq == 'a8':
                black_castle = remove(white_castle, element = 'q')
            if rook_depart_sq == 'h8':
                black_castle = remove(white_castle, element = 'k')
            board_List['white_castle'] = black_castle
            board_List['fullmove'] = str(int(board_List['fullmove']) + 1)
                                                    
    return board_List


            
def bishop_sq(board_List, position): # position of the bishop
    global alpha_to_num
    global num_to_alpha
    sq = material_sq(board_List)
    l = list(position.lower())
    square = []
    c1 = alpha_to_num[l[0]]
    c2 = int(l[1])
    if (num_to_alpha[c1] + str(c2)) in sq[0]:
        # The bishop is of WHITE
        
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1+1,c2+1):
            c1 = c1 + 1
            c2 = c2 + 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Bx" + p)
                break
            elif p in sq[0]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("B" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1-1,c2+1):
            c1 = c1 - 1
            c2 = c2 + 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Bx" + p)
                break
            elif p in sq[0]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("B" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1+1,c2-1):
            c1 = c1 + 1
            c2 = c2 - 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Bx" + p)
                break
            elif p in sq[0]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("B" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1-1,c2-1):
            c1 = c1 - 1
            c2 = c2 - 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Bx" + p)
                break
            elif p in sq[0]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("B" + p)

    elif (num_to_alpha[c1] + str(c2)) in sq[1]:
        # The bishop is of BLACK
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1+1,c2+1):
            c1 = c1 + 1
            c2 = c2 + 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Bx" + p)
                break
            elif p in sq[1]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("B" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1-1,c2+1):
            c1 = c1 - 1
            c2 = c2 + 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Bx" + p)
                break
            elif p in sq[1]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("B" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1+1,c2-1):
            c1 = c1 + 1
            c2 = c2 - 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Bx" + p)
                break
            elif p in sq[1]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("B" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1-1,c2-1):
            c1 = c1 - 1
            c2 = c2 - 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Bx" + p)
                break
            elif p in sq[1]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("B" + p)

    else:
        return "Invalid 'position'"
    return square
        
def rook_sq(board_List, position): # position of the rook
    global alpha_to_num
    global num_to_alpha
    sq = material_sq(board_List)
    l = list(position.lower())
    square = []
    c1 = alpha_to_num[l[0]]
    c2 = int(l[1])
    if (num_to_alpha[c1] + str(c2)) in sq[0]:
        # Rook is of WHITE
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1,c2+1):
            c2 = c2 + 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Rx" + p)
                break
            elif p in sq[0]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("R" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1,c2-1):
            c2 = c2 - 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Rx" + p)
                break
            elif p in sq[0]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("R" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1+1,c2):
            c1 = c1 + 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Rx" + p)
                break
            elif p in sq[0]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("R" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1-1,c2):
            c1 = c1 - 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Rx" + p)
                break
            elif p in sq[0]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("R" + p)
        
    elif (num_to_alpha[c1] + str(c2)) in sq[1]:
        # Rook is of BLACK
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1,c2+1):
            c2 = c2 + 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Rx" + p)
                break
            elif p in sq[1]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("R" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1,c2-1):
            c2 = c2 - 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Rx" + p)
                break
            elif p in sq[1]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("R" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1+1,c2):
            c1 = c1 + 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Rx" + p)
                break
            elif p in sq[1]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("R" + p)

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        while in_board(c1-1,c2):
            c1 = c1 - 1
            p = (num_to_alpha[c1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Rx" + p)
                break
            elif p in sq[1]:
                # That piece can't be captured
                break
            else:
                # Empty square
                square.append("R" + p)

    else:
        return "Invalid 'position'"
    return square
        
def queen_sq(board_List, position):  # position of the queen
    # Queen can move like rook and bishop at the same time so adding bishop and rook lines directly to queen squares
    diagonal = bishop_sq(board_List, position)
    line = rook_sq(board_List, position)
    square = []
    if diagonal != "Invalid 'position'" and line != "Invalid 'position'":
        for i in diagonal:
            square.append("Q" + i[1:])
        for i in line:
            square.append("Q" + i[1:])
        return square
    else:
        return "Invalid 'position'"

def knight_sq(board_List, position): #position of the knight
    # Bishop can move on max 8 squares only
    global alpha_to_num
    global num_to_alpha
    sq = material_sq(board_List)
    l = list(position.lower())
    square = []
    c1 = alpha_to_num[l[0]]
    c2 = int(l[1])
    if (num_to_alpha[c1] + str(c2)) in sq[0]:
        # The knight is of WHITE
        
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        if in_board(c1-1,c2+2):
            p = (num_to_alpha[c1-1] + str(c2+2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1-1,c2-2):
            p = (num_to_alpha[c1-1] + str(c2-2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1+1,c2+2):
            p = (num_to_alpha[c1+1] + str(c2+2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1+1,c2-2):
            p = (num_to_alpha[c1+1] + str(c2-2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1+2,c2+1):
            p = (num_to_alpha[c1+2] + str(c2+1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1+2,c2-1):
            p = (num_to_alpha[c1+2] + str(c2-1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1-2,c2+1):
            p = (num_to_alpha[c1-2] + str(c2+1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1-2,c2-1):
            p = (num_to_alpha[c1-2] + str(c2-1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)
            
        
    elif (num_to_alpha[c1] + str(c2)) in sq[1]:
        # Rook is of BLACK
        
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        if in_board(c1-1,c2+2):
            p = (num_to_alpha[c1-1] + str(c2+2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1-1,c2-2):
            p = (num_to_alpha[c1-1] + str(c2-2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1+1,c2+2):
            p = (num_to_alpha[c1+1] + str(c2+2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1+1,c2-2):
            p = (num_to_alpha[c1+1] + str(c2-2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1+2,c2+1):
            p = (num_to_alpha[c1+2] + str(c2+1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1+2,c2-1):
            p = (num_to_alpha[c1+2] + str(c2-1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1-2,c2+1):
            p = (num_to_alpha[c1-2] + str(c2+1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)

        if in_board(c1-2,c2-1):
            p = (num_to_alpha[c1-2] + str(c2-1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Nx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("N" + p)
        
    else:
        return "Invalid 'position'"
    return square


def pawn_sq(board_List, position): # position of pawn
    global alpha_to_num
    global num_to_alpha
    sq = material_sq(board_List)
    l = list(position.lower())
    square = []
    c1 = alpha_to_num[l[0]]
    c2 = int(l[1])
    if (num_to_alpha[c1] + str(c2)) in sq[0]:
        # The bishop is of WHITE
        
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        if c2==2:
            # Pawn can cover two squares at a time
            p = (num_to_alpha[c1]) + str(c2+1)
            p2 = (num_to_alpha[c1]) + str(c2+2)
            if p not in sq[0] and p not in sq[1]:
                if p2 not in sq[0] and p2 not in sq[1]:
                    square.append(p)
                    square.append(p2)
                else:
                    square.append(p)
            else:
                pass
                #Pawn can't move in forward or backward direction
            
            if c2 < 7 :
                if board_List['en_passant'] == "-":
                    if in_board(c1-1,c2+1):
                        p = (num_to_alpha[c1-1]) + str(c2+1)
                        if p in sq[1]:
                            #Pawn can be captured
                            square.append(num_to_alpha[c1] + "x" + num_to_alpha[c1-1] + str(c2+1))
                        else:
                            #No material or same side material hence pawn can't make to this square
                            pass
                        
                    elif in_board(c1+1,c2+1):
                        p = (num_to_alpha[c1+1]) + str(c2+1)
                        if p in sq[1]:
                            #Pawn can be captured
                            square.append(num_to_alpha[c1] + "x" + num_to_alpha[c1-1] + str(c2+1))
                        else:
                            #No material or same side material hence pawn can't make to this square
                            pass

                    elif in_board(c1,c2+1):
                        p = (num_to_alpha[c1]) + str(c2+1)
                        if p not in sq[0] and p not in sq[1]:
                            square.append(p)

                else:
                    position_en = list(board_List['en_passant'].lower())
                    en_c1 = alpha_to_num[position_en[0]]
                    en_c2 = int(position_en[1])
                    if (en_c1-1) == c1 and (en_c2-1) == c2:
                        square.append(num_to_alpha[c1] + "x" + num_to_alpha[en_c1] + str(en_c2) + " e.p.")
                    elif (en_c1+1) == c1 and (en_c2-1) == c2:
                        square.append(num_to_alpha[c1] + "x" + num_to_alpha[en_c1] + str(en_c2) + " e.p.")
            else:
                if in_board(c1,c2+1):
                    p = (num_to_alpha[c1]) + str(c2+1)
                    if p not in sq[0] and p not in sq[1]:
                        square.append(p + '=' + 'Q')
                        square.append(p + '=' + 'R')
                        square.append(p + '=' + 'B')
                        square.append(p + '=' + 'N')

                if in_board(c1-1,c2+1):
                    p = (num_to_alpha[c1-1]) + str(c2+1)
                    if p in sq[1]:
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')

                if in_board(c1+1,c2+1):
                    p = (num_to_alpha[c1+1]) + str(c2+1)
                    if p in sq[1]:
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                
                
        
    elif (num_to_alpha[c1] + str(c2)) in sq[1]:
        # Rook is of BLACK

        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
        if c2==7:
            # Pawn can cover two squares at a time
            p = (num_to_alpha[c1]) + str(c2-1)
            p2 = (num_to_alpha[c1]) + str(c2-2)
            if p not in sq[0] and p not in sq[1]:
                if p2 not in sq[0] and p2 not in sq[1]:
                    square.append(p)
                    square.append(p2)
                else:
                    square.append(p)
            else:
                pass
                #Pawn can't move in forward or backward direction
            
            if c2 > 2 :
                if board_List['en_passant'] == "-":
                    if in_board(c1-1,c2-1):
                        p = (num_to_alpha[c1-1]) + str(c2-1)
                        if p in sq[1]:
                            #Pawn can be captured
                            square.append(num_to_alpha[c1] + "x" + num_to_alpha[c1-1] + str(c2-1))
                        else:
                            #No material or same side material hence pawn can't make to this square
                            pass
                        
                    elif in_board(c1+1,c2-1):
                        p = (num_to_alpha[c1+1]) + str(c2-1)
                        if p in sq[1]:
                            #Pawn can be captured
                            square.append(num_to_alpha[c1] + "x" + num_to_alpha[c1-1] + str(c2-1))
                        else:
                            #No material or same side material hence pawn can't make to this square
                            pass

                    elif in_board(c1,c2-1):
                        p = (num_to_alpha[c1]) + str(c2-1)
                        if p not in sq[0] and p not in sq[1]:
                            square.append(p)

                else:
                    position_en = list(board_List['en_passant'].lower())
                    en_c1 = alpha_to_num[position_en[0]]
                    en_c2 = int(position_en[1])
                    if (en_c1-1) == c1 and (en_c2+1) == c2:
                        square.append(num_to_alpha[c1] + "x" + num_to_alpha[en_c1] + str(en_c2) + " e.p.")
                    elif (en_c1+1) == c1 and (en_c2+1) == c2:
                        square.append(num_to_alpha[c1] + "x" + num_to_alpha[en_c1] + str(en_c2) + " e.p.")
            else:
                if in_board(c1,c2-1):
                    p = (num_to_alpha[c1]) + str(c2-1)
                    if p not in sq[0] and p not in sq[1]:
                        square.append(p + '=' + 'Q')
                        square.append(p + '=' + 'R')
                        square.append(p + '=' + 'B')
                        square.append(p + '=' + 'N')

                if in_board(c1-1,c2-1):
                    p = (num_to_alpha[c1-1]) + str(c2-1)
                    if p in sq[0]:
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')

                if in_board(c1+1,c2+1):
                    p = (num_to_alpha[c1+1]) + str(c2-1)
                    if p in sq[0]:
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')
                        square.append((num_to_alpha[c1]) + 'x' + p + '=' + 'Q')

        
    else:
        return "Invalid 'position'"
    return square        

def king_sq_without_castle(board_List, side):
    global alpha_to_num
    global num_to_alpha
    sq = material_sq(board_List)
    if side == 'white':
        l = list(board_List['white_king'])
    elif side == 'black':
        l = list(board_List['black_king'])
    else:
        return "Invalid 'side'"
    square = []
    c1 = alpha_to_num[l[0]]
    c2 = int(l[1])
    if (num_to_alpha[c1] + str(c2)) in sq[0]:
        # The King is of WHITE
        
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
            
        if in_board(c1,c2-1):
            p = (num_to_alpha[c1] + str(c2-1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1,c2+1):
            p = (num_to_alpha[c1] + str(c2+1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2-1):
            p = (num_to_alpha[c1+1] + str(c2-1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2):
            p = (num_to_alpha[c1+1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2+1):
            p = (num_to_alpha[c1+1] + str(c2+1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2-1):
            p = (num_to_alpha[c1-1] + str(c2-1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2+1):
            p = (num_to_alpha[c1-1] + str(c2+1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2):
            p = (num_to_alpha[c1-1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)
        
            
        
    elif (num_to_alpha[c1] + str(c2)) in sq[1]:
        # The King is of BLACK
        
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])
                
        if in_board(c1,c2-1):
            p = (num_to_alpha[c1] + str(c2-1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1,c2+1):
            p = (num_to_alpha[c1] + str(c2+1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2-1):
            p = (num_to_alpha[c1+1] + str(c2-1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2):
            p = (num_to_alpha[c1+1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2+1):
            p = (num_to_alpha[c1+1] + str(c2+1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2-1):
            p = (num_to_alpha[c1-1] + str(c2-1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2+1):
            p = (num_to_alpha[c1-1] + str(c2+1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2):
            p = (num_to_alpha[c1-1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)
        
    else:
        return "Invalid 'position'"
    return square

def check_without_king_castle(board_List, side):
    
    l = board_List
    if side.lower() == 'white':
        wk_pos = l['white_king']
        for i in l['black_queen']:
            x = (queen_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True
                
        for i in l['black_bishop']:
            x = (bishop_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        for i in l['black_knight']:
            x = (knight_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        for i in l['black_rook']:
            x = (rook_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        for i in l['black_pawn']:
            x = (pawn_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        x = (king_sq_without_castle(board_List, side = 'black'))
        for j in x:
            if wk_pos in j:
                return True

    elif side.lower() == 'black':
        wk_pos = l['black_king']
        for i in l['white_queen']:
            x = (queen_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        for i in l['white_bishop']:
            x = (bishop_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True
                
        for i in l['white_knight']:
            x = (knight_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        for i in l['white_rook']:
            x = (rook_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True
                
        for i in l['white_pawn']:
            x = (pawn_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        x = (king_sq_without_castle(board_List, side = 'white'))
        for j in x:
            if wk_pos in j:
                return True

    else:
        return "Invalid 'side'"
    return False

def king_sq(board_List, side):
    global alpha_to_num
    global num_to_alpha
    sq = material_sq(board_List)
    if side == 'white':
        l = list(board_List['white_king'])
    elif side == 'black':
        l = list(board_List['black_king'])
    else:
        return "Invalid 'side'"
    square = []
    c1 = alpha_to_num[l[0]]
    c2 = int(l[1])
    if (num_to_alpha[c1] + str(c2)) in sq[0]:
        # The King is of WHITE
        
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])

        wc = board_List['white_castle']
        if 'Q' in wc :
            if 'd1' not in sq[0] and 'c1'not in sq[0] and 'b1' not in sq[0] and 'd1' not in sq[1] and 'c1'not in sq[1] and 'b1' not in sq[1] and check_without_king_castle(board_List, side = 'white') == False and check_without_king_castle(board_after_move(board_List, move = 'Kd1'), side = 'white') == False and check_without_king_castle(board_after_move(board_List, move = 'Kc1'), side = 'white') == False: 
                sq.append('O-O-O')
        if 'K' in wc :
            if 'f1' not in sq[0] and 'g1' not in sq[0] and 'f1' not in sq[1] and 'g1' not in sq[1] and check_without_king_castle(board_List, side = 'white') == False and check_without_king_castle(board_after_move(board_List, move = 'Kf1'), side = 'white') == False and check_without_king_castle(board_after_move(board_List, move = 'Kg1'), side = 'white') == False:
                sq.append('O-O')
            
        if in_board(c1,c2-1):
            p = (num_to_alpha[c1] + str(c2-1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1,c2+1):
            p = (num_to_alpha[c1] + str(c2+1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2-1):
            p = (num_to_alpha[c1+1] + str(c2-1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2):
            p = (num_to_alpha[c1+1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2+1):
            p = (num_to_alpha[c1+1] + str(c2+1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2-1):
            p = (num_to_alpha[c1-1] + str(c2-1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2+1):
            p = (num_to_alpha[c1-1] + str(c2+1))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2):
            p = (num_to_alpha[c1-1] + str(c2))
            if p in sq[1]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[0]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)
        
            
        
    elif (num_to_alpha[c1] + str(c2)) in sq[1]:
        # The King is of BLACK
        
        c1 = alpha_to_num[l[0]]
        c2 = int(l[1])

        wc = board_List['black_castle']
        if 'Q' in wc :
            if 'd8' not in sq[0] and 'c8'not in sq[0] and 'b8' not in sq[0] and 'd8' not in sq[1] and 'c8'not in sq[1] and 'b8' not in sq[1] and check_without_king_castle(board_List, side = 'black') == False and check_without_king_castle(board_after_move(board_List, move = 'Kd8'), side = 'black') == False and check_without_king_castle(board_after_move(board_List, move = 'Kc8'), side = 'black') == False: 
                sq.append('O-O-O')
        if 'K' in wc :
            if 'f8' not in sq[0] and 'g8' not in sq[0] and 'f8' not in sq[1] and 'g8' not in sq[1] and check_without_king_castle(board_List, side = 'black') == False and check_without_king_castle(board_after_move(board_List, move = 'Kf8'), side = 'black') == False and check_without_king_castle(board_after_move(board_List, move = 'Kg8'), side = 'black') == False:
                sq.append('O-O')
                
        if in_board(c1,c2-1):
            p = (num_to_alpha[c1] + str(c2-1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1,c2+1):
            p = (num_to_alpha[c1] + str(c2+1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2-1):
            p = (num_to_alpha[c1+1] + str(c2-1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2):
            p = (num_to_alpha[c1+1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1+1,c2+1):
            p = (num_to_alpha[c1+1] + str(c2+1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2-1):
            p = (num_to_alpha[c1-1] + str(c2-1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2+1):
            p = (num_to_alpha[c1-1] + str(c2+1))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)

        if in_board(c1-1,c2):
            p = (num_to_alpha[c1-1] + str(c2))
            if p in sq[0]:
                # That piece can be captured
                square.append("Kx" + p)
            elif p in sq[1]:
                # That piece can't be captured
                pass
            else:
                # Empty square
                square.append("K" + p)
        
    else:
        return "Invalid 'position'"
    return square
    
    
       
def check(board_List, side):
    
    l = board_List
    if side.lower() == 'white':
        wk_pos = l['white_king']
        for i in l['black_queen']:
            x = (queen_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True
                
        for i in l['black_bishop']:
            x = (bishop_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        for i in l['black_knight']:
            x = (knight_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        for i in l['black_rook']:
            x = (rook_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        for i in l['black_pawn']:
            x = (pawn_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        x = (king_sq(board_List, side = 'black'))
        for j in x:
            if wk_pos in j:
                return True

    elif side.lower() == 'black':
        wk_pos = l['black_king']
        for i in l['white_queen']:
            x = (queen_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        for i in l['white_bishop']:
            x = (bishop_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True
                
        for i in l['white_knight']:
            x = (knight_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        for i in l['white_rook']:
            x = (rook_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True
                
        for i in l['white_pawn']:
            x = (pawn_sq(board_List, i))
            for j in x:
                if wk_pos in j:
                    return True

        x = (king_sq(board_List, side = 'white'))
        for j in x:
            if wk_pos in j:
                return True

    else:
        return "Invalid 'side'"
    return False

def legal_move(board_FEN):
    # It will generate all the possible legal moves
    
    d = FEN_to_List(board_FEN)
    board_List = d
    if d['side_to_move'] == 'white':
        moves = []
        
        m  = {}
        for i in d['white_queen']:
            x = (queen_sq(d, i))
            for item in x:
                moves.append(item)
            m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in m[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            li = diff_squares(x[i])
            for item in li:
                moves.append(i[0:1] + item + i[1:])

        m  = {}
        for i in d['white_bishop']:
            x = (bishop_sq(d, i))
            for item in x:
                moves.append(item)
            m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in m[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            li = diff_squares(x[i])
            for item in li:
                moves.append(i[0:1] + item + i[1:])

        m  = {}
        for i in d['white_knight']:
            x = (knight_sq(d, i))
            for item in x:
                moves.append(item)
            m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in m[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            li = diff_squares(x[i])
            for item in li:
                moves.append(i[0:1] + item + i[1:])

        m  = {}
        for i in d['white_rook']:
            x = (rook_sq(d, i))
            for item in x:
                moves.append(item)
            m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in m[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            li = diff_squares(x[i])
            for item in li:
                moves.append(i[0:1] + item + i[1:])

        m  = {}
        for i in d['white_pawn']:
            x = (pawn_sq(d, i))
            for item in x:
                moves.append(item)
            m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in m[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            li = diff_squares(x[i])
            for item in li:
                moves.append(i[0:1] + item + i[1:])

        m  = {}
        x = (king_sq(d,side = 'white'))
        for item in x:
            moves.append(item)
        m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in i:
                if j in common:
                    x[j].append(i)
        for i in x:
            li = diff_squares(i)
            for item in li:
                moves.append(i[0:1] + item + i[1:])

        # Now checking whether the moves are legal or not due to check
        m = []
        for i in moves:
            if i == 'Qc1':
                print(board_after_move(board_List, move = i))
            if check(board_after_move(board_List, move = i), side = 'white') == False:
                m.append(i)
                print(i + " :ACCEPTED")
            else:
                print(i + " :REJECTED")
            board_List = FEN_to_List(board_FEN)
        moves = m
                
    elif d['side_to_move'] == 'black':
        moves = []
        m  = {}
        for i in d['black_queen']:
            x = (queen_sq(d, i))
            for item in x:
                moves.append(item)
            m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in m[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            li = diff_squares(x[i])
            for item in li:
                moves.append(i[0:1] + item + i[1:])

        m  = {}
        for i in d['black_bishop']:
            x = (bishop_sq(d, i))
            for item in x:
                moves.append(item)
            m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in m[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            li = diff_squares(x[i])
            for item in li:
                moves.append(i[0:1] + item + i[1:])

        m  = {}
        for i in d['black_knight']:
            x = (knight_sq(d, i))
            for item in x:
                moves.append(item)
            m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in m[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            li = diff_squares(x[i])
            for item in li:
                moves.append(i[0:1] + item + i[1:])
        m  = {}
        for i in d['black_rook']:
            x = (rook_sq(d, i))
            for item in x:
                moves.append(item)
            m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in m[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            li = diff_squares(x[i])
            for item in li:
                moves.append(i[0:1] + item + i[1:])
        m  = {}
        for i in d['black_pawn']:
            x = (pawn_sq(d, i))
            for item in x:
                moves.append(item)
            m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in m[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            li = diff_squares(x[i])
            for item in li:
                moves.append(i[0:1] + item + i[1:])

        m  = {}
        x = (king_sq(d,side = 'black'))
        for item in x:
            moves.append(item)
        m[i] = x
        l = []
        for i in m:
            l.append(m[i])
        common = same_element(l)
        x = {}
        moves = remove(moves, common)
        for i in m:
            for j in i:
                if j in common:
                    x[j].append(i)
        for i in x:
            li = diff_squares(i)
            for item in li:
                moves.append(i[0:1] + item + i[1:])

        # Now checking whether the moves are legal or not due to check
        m = []

        for i in moves:
            if check(board_after_move(board_List, move = i), side = 'black') == False:
                m.append(i)
            board_List = FEN_to_List(board_FEN)
        moves = m

    else:
        return "Invalid 'side'"

    if len(moves) == 0:
        return "Checkmate"
    return moves
            

def moves_with_position(board_FEN, position):
    # Generate Moves by a given co ordinate
    board_List = FEN_to_List(board_FEN)
    d = board_List
    piece = piece_on_pos(board_List,position)
    moves = []
    if piece == 'white_king':
        m  = {}
        x = (king_sq(d,side = 'black'))
        for item in x:
            moves.append(item)
            
    elif piece == 'white_queen':
        m  = {}
        moves = {}
        for i in d['white_queen']:
            x = (queen_sq(d, i))
            moves[i] = x
            if i == position:
                m[i] = x
        l = []
        for i in moves:
            l.append(moves[i])
        common = same_element(l)
        x = {}
        m[position] = remove(m[position], common)
        for i in moves:
            for j in moves[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            location = None
            for var in range(0,len(x[i])):
                if x[i][var] == position:
                    location = var
            li = diff_squares(x[i])
            if location != None:
                for item in range(0,len(li)):
                    if item == location:
                        m[position].append(i[0:1] + li[item] + i[1:])
        moves = m[position]
        
    elif piece == 'white_bishop':
        m  = {}
        moves = {}
        for i in d['white_bishop']:
            x = (bishop_sq(d, i))
            moves[i] = x
            if i == position:
                m[i] = x
        l = []
        for i in moves:
            l.append(moves[i])
        common = same_element(l)
        x = {}
        m[position] = remove(m[position], common)
        for i in moves:
            for j in moves[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            location = None
            for var in range(0,len(x[i])):
                if x[i][var] == position:
                    location = var
            li = diff_squares(x[i])
            if location != None:
                for item in range(0,len(li)):
                    if item == location:
                        m[position].append(i[0:1] + li[item] + i[1:])
        moves = m[position]

    elif piece == 'white_knight':
        m  = {}
        moves = {}
        for i in d['white_knight']:
            x = (knight_sq(d, i))
            moves[i] = x
            if i == position:
                m[i] = x
        l = []
        for i in moves:
            l.append(moves[i])
        common = same_element(l)
        x = {}
        m[position] = remove(m[position], common)
        for i in moves:
            for j in moves[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            location = None
            for var in range(0,len(x[i])):
                if x[i][var] == position:
                    location = var
            li = diff_squares(x[i])
            if location != None:
                for item in range(0,len(li)):
                    if item == location:
                        m[position].append(i[0:1] + li[item] + i[1:])
        moves = m[position]

    elif piece == 'white_rook':
        m  = {}
        moves = {}
        for i in d['white_rook']:
            x = (rook_sq(d, i))
            moves[i] = x
            if i == position:
                m[i] = x
        l = []
        for i in moves:
            l.append(moves[i])
        common = same_element(l)
        x = {}
        m[position] = remove(m[position], common)
        for i in moves:
            for j in moves[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            location = None
            for var in range(0,len(x[i])):
                if x[i][var] == position:
                    location = var
            li = diff_squares(x[i])
            if location != None:
                for item in range(0,len(li)):
                    if item == location:
                        m[position].append(i[0:1] + li[item] + i[1:])
        moves = m[position]

    elif piece == 'white_pawn':
        m  = {}
        moves = {}
        for i in d['white_pawn']:
            x = (pawn_sq(d, i))
            moves[i] = x
            if i == position:
                m[i] = x
        l = []
        for i in moves:
            l.append(moves[i])
        common = same_element(l)
        x = {}
        m[position] = remove(m[position], common)
        for i in moves:
            for j in moves[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            location = None
            for var in range(0,len(x[i])):
                if x[i][var] == position:
                    location = var
            li = diff_squares(x[i])
            if location != None:
                for item in range(0,len(li)):
                    if item == location:
                        m[position].append(i[0:1] + li[item] + i[1:])
        moves = m[position]


    elif piece == 'black_king':
        m  = {}
        x = (king_sq(d,side = 'black'))
        for item in x:
            moves.append(item)
            
    elif piece == 'black_queen':
        m  = {}
        moves = {}
        for i in d['black_queen']:
            x = (queen_sq(d, i))
            moves[i] = x
            if i == position:
                m[i] = x
        l = []
        for i in moves:
            l.append(moves[i])
        common = same_element(l)
        x = {}
        m[position] = remove(m[position], common)
        for i in moves:
            for j in moves[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            location = None
            for var in range(0,len(x[i])):
                if x[i][var] == position:
                    location = var
            li = diff_squares(x[i])
            if location != None:
                for item in range(0,len(li)):
                    if item == location:
                        m[position].append(i[0:1] + li[item] + i[1:])
        moves = m[position]

    elif piece == 'black_bishop':
        m  = {}
        moves = {}
        for i in d['black_bishop']:
            x = (bishop_sq(d, i))
            moves[i] = x
            if i == position:
                m[i] = x
        l = []
        for i in moves:
            l.append(moves[i])
        common = same_element(l)
        x = {}
        m[position] = remove(m[position], common)
        for i in moves:
            for j in moves[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            location = None
            for var in range(0,len(x[i])):
                if x[i][var] == position:
                    location = var
            li = diff_squares(x[i])
            if location != None:
                for item in range(0,len(li)):
                    if item == location:
                        m[position].append(i[0:1] + li[item] + i[1:])
        moves = m[position]

    elif piece == 'black_knight':
        m  = {}
        moves = {}
        for i in d['black_knight']:
            x = (knight_sq(d, i))
            moves[i] = x
            if i == position:
                m[i] = x
        l = []
        for i in moves:
            l.append(moves[i])
        common = same_element(l)
        x = {}
        m[position] = remove(m[position], common)
        for i in moves:
            for j in moves[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            location = None
            for var in range(0,len(x[i])):
                if x[i][var] == position:
                    location = var
            li = diff_squares(x[i])
            if location != None:
                for item in range(0,len(li)):
                    if item == location:
                        m[position].append(i[0:1] + li[item] + i[1:])
        moves = m[position]
        
    elif piece == 'black_rook':
        m  = {}
        moves = {}
        for i in d['black_rook']:
            x = (rook_sq(d, i))
            moves[i] = x          
            if i == position:
                m[i] = x
        l = []
        for i in moves:
            l.append(moves[i])
        common = same_element(l)
        x = {}
        m[position] = remove(m[position], common)
        for i in moves:
            for j in moves[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            location = None
            for var in range(0,len(x[i])):
                if x[i][var] == position:
                    location = var
            li = diff_squares(x[i])
            if location != None:
                for item in range(0,len(li)):
                    if item == location:
                        m[position].append(i[0:1] + li[item] + i[1:])
        moves = m[position]
        
    elif piece == 'black_pawn':
        m  = {}
        moves = {}
        for i in d['black_pawn']:
            x = (pawn_sq(d, i))
            moves[i] = x
            if i == position:
                m[i] = x
        l = []
        for i in moves:
            l.append(moves[i])
        common = same_element(l)
        x = {}
        m[position] = remove(m[position], common)
        for i in moves:
            for j in moves[i]:
                if j in common:
                    try:
                        x[j].append(i)
                    except:
                        x[j] = [i]
        for i in x:
            location = None
            for var in range(0,len(x[i])):
                if x[i][var] == position:
                    location = var
            li = diff_squares(x[i])
            if location != None:
                for item in range(0,len(li)):
                    if item == location:
                        m[position].append(i[0:1] + li[item] + i[1:])
        moves = m[position]

    # Now checking whether the moves are legal or not due to check
    m = []
    if 'white' in piece:
        for i in moves:
            if check(board_after_move(board_List, move = i), side = 'white') == False:
                m.append(i)
            board_List = FEN_to_List(board_FEN)
        moves = m
    elif 'black' in piece:
        for i in moves:
            if check(board_after_move(board_List, move = i), side = 'black') == False:
                m.append(i)
            board_List = FEN_to_List(board_FEN)
        moves = m
    else:
        return "Can't Recognise the piece"

    return moves
    

    
        
        
        
        
        
        
        
        
    
        
                    
            
            
        
    
        
        
            
#print(FEN_to_List('rbq3r/pppp1pbp/2nnp1/4p3/4P3/2NPB3/PPPQ1PPP/RkK1BNR b qk - 7 9') )                
#print(legal_move('rnbqk2r/pppp1pbp/5np1/4p3/4P3/2NPB3/PPPQ1PPP/R3KBNR b KQkq - 3 5'))
#print(legal_move('r1bqk2r/pppp1pbp/2n2np1/4p3/4P3/2NPB3/PPPQ1PPP/R3KBNR w KQkq - 4 6'))
#print(moves_with_position('r1bqk2r/pppp1pbp/2n2np1/4p3/4P3/2NPB3/PPPQ1PPP/R3KBNR w KQkq - 4 6','h2'))
#ranks=fen_to_board('r1bqk2r/pppp1pbp/2n2np1/4p3/4P3/2NPB3/PPPQ1PPP/R3KBNR w KQkq - 4 6')
#keyboard=board_to_keyboard(ranks, 'link')
        
    
