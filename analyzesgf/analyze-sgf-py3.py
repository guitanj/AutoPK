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
#天元
tengenPoint = [9,9]

#全星位点三三开局（对角星或者二连星）
openning_4S33 = [[],starPoint,starPoint,starPoint,starPoint,sansanPoint]
#二连星对星小目
openning_2SSK = [[],starPoint,starPoint,starPoint,komokuPoint]

result=[]
for root,dirs,files in os.walk("."):
    for eachfile in files:
        if os.path.splitext(eachfile)[1] == '.sgf':
            result.append(os.path.join(root, eachfile))
            print(eachfile)
for fname in result:
    sgffile=open(fname,'rb')
    sgf_src = sgffile.read()
    sgffile.close()
    try:
        sgf_game = sgf.Sgf_game.from_bytes(sgf_src)
    except ValueError:
        raise Exception("bad sgf file")

    print(sgf_game.get_player_name('b'),'vs',sgf_game.get_player_name('w'), \
          'komi',sgf_game.get_komi(),'Result:',sgf_game.get_winner(),'wins')

    mainSequence = sgf_game.get_main_sequence()

    is_openning_4S33 = True
    is_openning_diagonalStar33 = False  #对角星
    is_openning_sameSideStar33 = False  #二连星
    #基础判断
    for eachStep in range(1,len(openning_4S33)):
        (color,stepmove) = mainSequence[eachStep].get_move()
        if stepmove != None:
            row, col = stepmove
        else:
            is_openning_4Star33 = False
            print("读取棋谱信息出错")
            break
        if (row,col) not in openning_4S33[eachStep]:
            is_openning_4S33 = False


    #还需要判断是二连星还是对角星，黑1、3两手棋坐标全不相同则为对角星，否则一定是二连星
    if is_openning_4S33:
        (color1,stepmove1) = mainSequence[1].get_move()
        row1, col1 = stepmove1
        (color3,stepmove3) = mainSequence[3].get_move()
        row3, col3 = stepmove3
        print(row1, col1,row3, col3)
        if row1 != row3 and col1 != col3:
            is_openning_diagonalStar33 = True
        else:
            is_openning_sameSideStar33 = True
    if is_openning_diagonalStar33:
        print(fname,"对角星点三三开局")
        continue
    if is_openning_sameSideStar33:
        print(fname,"二连星点三三开局")
        continue
    if not is_openning_diagonalStar33 and not is_openning_sameSideStar33:
        is_openning_2SSK = True
        #判断是否是二连星对星小目开局
        for eachStep in range(1,len(openning_2SSK)):
            (color,stepmove) = mainSequence[eachStep].get_move()
            if stepmove != None:
                row, col = stepmove
            if (row,col) not in openning_2SSK[eachStep]:
                is_openning_2SSK = False
        if is_openning_2SSK:
            print(fname,"二连星对星小目开局")
            continue
        else:
            print(fname,"未知开局")
