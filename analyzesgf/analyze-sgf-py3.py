# -*- coding: utf-8 -*-

import os
from sgfmill import ascii_boards
from sgfmill import sgf
from sgfmill import sgf_moves

move_number = 500

#星位
starPoint = [(r,c) for r in [3,15] for c in [3,15]]
#小目
komokuPoint = [(r,c) for r in [3,15] for c in [2,16]]
komokuPoint += [(r,c) for r in [2,16] for c in [3,15]]
#三三
sansanPoint = [(r,c) for r in [2,16] for c in [2,16]]
#星位小飞挂
flyPoint = [(r,c) for r in [2,16] for c in [5,13]]
flyPoint += [(r,c) for r in [5,13] for c in [2,16]]
#天元
tengenPoint = [9,9]

#2星位（对角星或者二连星）
openning_2S = [starPoint,starPoint]
#星小目
openning_SK = [starPoint,komokuPoint]
#小目星
openning_KS = [komokuPoint,starPoint]
#双小目
openning_KK = [komokuPoint,komokuPoint]
#2个星位后点三三
openning_2S33 = [starPoint,starPoint,sansanPoint]
#小目星位后点三三
openning_KS33 = [komokuPoint,starPoint,sansanPoint]

#判断是否为对角星
def is_diagonalStar(steps):
    is_openning_2S = True
    is_openning_diagonalStar = False  #对角星
    #基础判断
    for eachStep in range(2):
        row, col = steps[eachStep]
        #print('  is_diagonalStar:',row,col)
        if (row,col) not in openning_2S[eachStep]:
            is_openning_2S = False

    #黑1、3两手棋坐标全不相同则为对角星
    if is_openning_2S:
        row1, col1 = steps[0]
        row2, col2 = steps[1]
        #print(row1, col1,row2, col2)
        if row1 != row2 and col1 != col2:
            return True
    return False

#判断是否为二连星
def is_sameSideStar(steps):
    is_openning_2S = True
    #基础判断
    for eachStep in range(2):
        row, col = steps[eachStep]
        #print('  is_sameSideStar:',row,col,eachStep)
        if (row,col) not in openning_2S[eachStep]:
            is_openning_2S = False

    #黑1、3两手棋坐标全不相同则为对角星
    if is_openning_2S:
        row1, col1 = steps[0]
        row2, col2 = steps[1]
        #print(row1, col1,row2, col2)
        if row1 != row2 and col1 != col2:
            return False
        else:
            return True
    return False

#判断是否为星小目
def is_starKomoku(steps):
    is_openning_SK = True
    for eachStep in range(2):
        row, col = steps[eachStep]
        #print('  is_starKomoku:',row,col)
        if (row,col) not in openning_SK[eachStep]:
            is_openning_SK = False
    if is_openning_SK:
        return True
    return False

#判断是否为小目星
def is_komokuStar(steps):
    is_openning_KS = True
    for eachStep in range(2):
        row, col = steps[eachStep]
        #print('  is_komokuStar:',row,col)
        if (row,col) not in openning_KS[eachStep]:
            is_openning_KS = False
    if is_openning_KS:
        return True
    return False

#判断是否是两个星位后点三三
def is_2starSansan(steps):
    is_openning_2S33 = True
    for eachStep in range(3):
        row, col = steps[eachStep]
        if (row,col) not in openning_2S33[eachStep]:
            is_openning_2S33 = False
    if is_openning_2S33:
        #需要补测一下三三是否点在第二手的三三位置
        row2, col2 = steps[1]
        row3, col3 = steps[2]
        #print('  is_2starSansan',row2,col2,row3,col3)
        if row2 < 9 and col2 < 9:    #左下角
            if row3 == 2 and col3 == 2:
                return True
        elif row2 < 9 and col2 > 9:    #右下角
            if row3 == 2 and col3 == 16:
                return True
        elif row2 > 9 and col2 < 9:    #左上角
            if row3 == 16 and col3 == 2:
                return True
        elif row2 > 9 and col2 > 9:    #右上角
            if row3 == 16 and col3 == 16:
                return True
    return False

#判断是否是黑小目白星位后黑点三三
def is_KS33(steps):
    is_openning_KS33 = True
    for eachStep in range(3):
        row, col = steps[eachStep]
        if (row,col) not in openning_KS33[eachStep]:
            is_openning_KS33 = False
    if is_openning_KS33:
        #需要补测一下三三是否点在第二手的三三位置
        row2, col2 = steps[1]
        row3, col3 = steps[2]
        #print('  is_KS33',row2,col2,row3,col3)
        if row2 < 9 and col2 < 9:    #左下角
            if row3 == 2 and col3 == 2:
                return True
        elif row2 < 9 and col2 > 9:    #右下角
            if row3 == 2 and col3 == 16:
                return True
        elif row2 > 9 and col2 < 9:    #左上角
            if row3 == 16 and col3 == 2:
                return True
        elif row2 > 9 and col2 > 9:    #右上角
            if row3 == 16 and col3 == 16:
                return True
    return False

result=[]
for root,dirs,files in os.walk("."):
    for eachfile in files:
        if os.path.splitext(eachfile)[1] == '.sgf':
            result.append(os.path.join(root, eachfile))
            #print(eachfile)
for fname in result:
    sgffile=open(fname,'rb')
    sgf_src = sgffile.read()
    sgffile.close()
    try:
        sgf_game = sgf.Sgf_game.from_bytes(sgf_src)
    except ValueError:
        raise Exception("bad sgf file")

    #print(sgf_game.get_player_name('b'),'vs',sgf_game.get_player_name('w'), \
    #      'komi',sgf_game.get_komi(),'Result:',sgf_game.get_winner(),'wins')

    mainSequence = sgf_game.get_main_sequence()

    #基础判断,取黑棋1、3步以及白棋2、4步
    (color,step1) = mainSequence[1].get_move()
    (color,step3) = mainSequence[3].get_move()
    (color,step2) = mainSequence[2].get_move()
    (color,step4) = mainSequence[4].get_move()
    #print(step1,step2,step3,step4)
    if step1 != None:
        row, col = step1
    else:
        print("读取棋谱信息出错")
        break

    if is_diagonalStar([step1,step3]):  #黑对角星开局
        #print('黑对角星开局')
        if is_diagonalStar([step2,step4]):   #白也是对角星
            (color5,stepmove5) = mainSequence[5].get_move()
            row5, col5 = stepmove5
            #print('对角星vs对角星',row5,col5)
            if (row5,col5) in sansanPoint:
                #print(fname,"对角星点三三开局")
                continue
            elif (row5,col5) in flyPoint:
                #print(fname,"对角星小飞挂开局")
                continue
        elif is_starKomoku([step2,step4]):  #白星对角小目开局
            #print(fname,"对角星对星对角小目开局")
            continue
        elif is_komokuStar([step2,step4]):  #白小目星开局
            #print(fname,"对角星对小目星开局")
            continue
    elif is_sameSideStar([step1,step3]):    #黑二连星开局
        #print('黑二连星开局')
        if is_sameSideStar([step2,step4]):  #白也是二连星开局
            (color5,stepmove5) = mainSequence[5].get_move()
            row5, col5 = stepmove5
            #print('二连星vs二连星',row5,col5)
            if (row5,col5) in sansanPoint:
                #print(fname,"二连星点三三开局")
                continue
            elif (row5,col5) in flyPoint:
                #print(fname,"二连星小飞挂开局")
                continue
        elif is_starKomoku([step2,step4]):  #白星小目开局
            #print(fname,"二连星对星小目开局")
            continue
        elif is_komokuStar([step2,step4]):  #白小目星开局
            #print(fname,"二连星对小目星开局")
            continue
    elif is_komokuStar([step1,step3]):  #黑小目星开局
        #print('黑小目星开局')
        if is_starKomoku([step2,step4]):    #白星小目开局
            #print(fname,"小目星对星小目开局")
            continue
        if is_sameSideStar([step2,step4]):  #白二连星开局
            #print(fname,"小目星对二连星开局")
            continue
        if is_komokuStar([step2,step4]):    #白小目星开局
            #print(fname,"小目星对小目星开局")
            continue
    elif is_starKomoku([step1,step3]):  #黑星小目开局
        #print('黑星小目开局')
        if is_starKomoku([step2,step4]):    #白星小目开局
            #print(fname,"星小目对星小目开局")
            continue
        if is_sameSideStar([step2,step4]):  #白二连星开局
            #print(fname,"星小目对二连星开局")
            continue
    elif is_2starSansan([step1,step2,step3]):
        #print(fname,"星位后点三三开局")
        continue
    elif is_KS33([step1,step2,step3]):
        #print(fname,"小目星位后点三三开局")
        continue
    print(fname,"未知开局")
