# -*- coding: utf-8 -*-

import os
from time import sleep
from sgfmill import ascii_boards
from sgfmill import sgf
from sgfmill import sgf_moves

move_number = 500

#星位
starPoint = [(r,c) for r in [3,15] for c in [3,15]]
#小目
komokuPoint = [(r,c) for r in [3,15] for c in [2,16]]
komokuPoint += [(r,c) for r in [2,16] for c in [3,15]]
#高目
t54Point = [(r,c) for r in [3,15] for c in [4,14]]
t54Point += [(r,c) for r in [4,14] for c in [3,15]]
#三三
sansanPoint = [(r,c) for r in [2,16] for c in [2,16]]
#星位小飞挂
flyPoint = [(r,c) for r in [2,16] for c in [5,13]]
flyPoint += [(r,c) for r in [5,13] for c in [2,16]]
#小目低挂
kflyPoint = [(r,c) for r in [2,16] for c in [4,14]]
kflyPoint += [(r,c) for r in [4,14] for c in [2,16]]
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
#星三三
openning_S33 = [starPoint,sansanPoint]
#三三星
openning_33S = [sansanPoint,starPoint]
#小目三三
openning_K33 = [komokuPoint,sansanPoint]
#三三小目
openning_33K = [sansanPoint,komokuPoint]
#星高目
openning_S54 = [starPoint,t54Point]
#2个星位后点三三
openning_2S33 = [starPoint,starPoint,sansanPoint]
#小目星位后点三三
openning_KS33 = [komokuPoint,starPoint,sansanPoint]
#星位小目后低挂
openning_SKFly = [starPoint,komokuPoint,kflyPoint]

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

#判断是否为双小目
def is_KK(steps):
    is_openning_KK = True
    for eachStep in range(2):
        row, col = steps[eachStep]
        #print('  is_KK:',row,col)
        if (row,col) not in openning_KK[eachStep]:
            is_openning_KK = False
    if is_openning_KK:
        return True
    return False

#判断是否为星高目
def is_S54(steps):
    is_openning_S54 = True
    for eachStep in range(2):
        row, col = steps[eachStep]
        #print('  is_K54:',row,col)
        if (row,col) not in openning_S54[eachStep]:
            is_openning_S54 = False
    if is_openning_S54:
        return True
    return False

#判断是否为星三三
def is_S33(steps):
    is_openning_S33 = True
    for eachStep in range(2):
        row, col = steps[eachStep]
        #print('  is_S33:',row,col)
        if (row,col) not in openning_S33[eachStep]:
            is_openning_S33 = False
    if is_openning_S33:
        return True
    return False

#判断是否为三三星
def is_33S(steps):
    is_openning_33S = True
    for eachStep in range(2):
        row, col = steps[eachStep]
        #print('  is_33S:',row,col)
        if (row,col) not in openning_33S[eachStep]:
            is_openning_33S = False
    if is_openning_33S:
        return True
    return False

#判断是否为小目三三
def is_K33(steps):
    is_openning_K33 = True
    for eachStep in range(2):
        row, col = steps[eachStep]
        #print('  is_K33:',row,col
        if (row,col) not in openning_K33[eachStep]:
            is_openning_K33 = False
    if is_openning_K33:
        return True
    return False

#判断是否为三三小目
def is_33K(steps):
    is_openning_33K = True
    for eachStep in range(2):
        row, col = steps[eachStep]
        #print('  is_33K:',row,col
        if (row,col) not in openning_33K[eachStep]:
            is_openning_33K = False
    if is_openning_33K:
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

#判断是否是黑星位白小目后黑低挂白小目
def is_SKFly(steps):
    is_openning_SKFly = True
    for eachStep in range(3):
        row, col = steps[eachStep]
        if (row,col) not in openning_SKFly[eachStep]:
            is_openning_SKFly = False
    if is_openning_SKFly:
        return True
    return False

result=[]
for root,dirs,files in os.walk("."):
    for eachfile in files:
        if os.path.splitext(eachfile)[1] == '.sgf':
            result.append(os.path.join(root, eachfile))
            #print(eachfile)
bwin = wwin = num = 0

dsds33=dsdsfly=dssk=dss33=dskk=0
ssssss33=ssssssfly=ssssk=ssskk=0
sksk=sksss=skds=skkk=0
s33sk=s33sss=s33ds=s33kk=0
kksk=kksss=kkds=kkkk=kk33k=kkk33=0
s54sk=s54sss=s54ds=s54s33=0
twoStar33=ks33=skfly=0

have_dsds33=have_dsdsfly=have_dssk=have_dss33=have_dskk=False
have_ssssss33=have_ssssssfly=have_ssssk=have_ssskk=False
have_sksk=have_sksss=have_skds=have_skkk=False
have_s33sk=have_s33sss=have_s33ds=have_s33kk=False
have_kksk=have_kksss=have_kkds=have_kkkk=have_kk33k=have_kkk33=False
have_s54sk=have_s54sss=have_s54ds=have_s54s33=False
have_twoStar33=have_ks33=have_skfly=False

bwin_dsds33=bwin_dsdsfly=bwin_dssk=bwin_dss33=bwin_dskk=0
bwin_ssssss33=bwin_ssssssfly=bwin_ssssk=bwin_ssskk=0
bwin_sksk=bwin_sksss=bwin_skds=bwin_skkk=0
bwin_s33sk=bwin_s33sss=bwin_s33ds=bwin_s33kk=0
bwin_kksk=bwin_kksss=bwin_kkds=bwin_kkkk=bwin_kk33k=bwin_kkk33=0
bwin_s54sk=bwin_s54sss=bwin_s54ds=bwin_s54s33=0
bwin_twoStar33=bwin_ks33=bwin_skfly=0

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

    whowins = fname[fname.find('+')-1]
    if whowins == 'b':
        bwin += 1
        num += 1
    elif whowins == 'w':
        wwin += 1
        num += 1
    
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
            #print('对角星vs对角星',row5,col5
            if (row5,col5) in sansanPoint:
                #print(fname,"对角星点三三开局")
                have_dsds33 = True
                dsds33 += 1
                if whowins == 'b':
                    bwin_dsds33 += 1
                continue
            elif (row5,col5) in flyPoint:
                #print(fname,"对角星小飞挂开局")
                have_dsdsfly = True
                dsdsfly += 1
                if whowins == 'b':
                    bwin_dsdsfly += 1
                continue
        elif is_starKomoku([step2,step4]) or is_komokuStar([step2,step4]):  #白星对角小目或者小目星开局
            #print(fname,"对角星对星对角小目开局")
            have_dssk = True
            dssk += 1
            if whowins == 'b':
                bwin_dssk += 1
            continue
        elif is_S33([step2,step4]):  #白星33开局
            #print(fname,"对角星对星三三开局")
            have_dss33 = True
            dss33 += 1
            if whowins == 'b':
                bwin_dss33 += 1
            continue
        elif is_33S([step2,step4]):  #白33星开局
            #print(fname,"对角星对三三星开局")
            have_dss33 = True
            dss33 += 1
            if whowins == 'b':
                bwin_dss33 += 1
            continue
        if is_KK([step2,step4]):    #白双小目开局
            #print(fname,"对角星对双小目开局")
            have_dskk = True
            dskk += 1
            if whowins == 'b':
                bwin_dskk += 1
            continue
    elif is_sameSideStar([step1,step3]):    #黑二连星开局
        #print('黑二连星开局')
        if is_sameSideStar([step2,step4]):  #白也是二连星开局
            (color5,stepmove5) = mainSequence[5].get_move()
            row5, col5 = stepmove5
            #print('二连星vs二连星',row5,col5)
            if (row5,col5) in sansanPoint:
                #print(fname,"二连星点三三开局")
                have_ssssss33 = True
                ssssss33 += 1
                if whowins == 'b':
                    bwin_ssssss33 += 1
                continue
            elif (row5,col5) in flyPoint:
                #print(fname,"二连星小飞挂开局")
                have_ssssssfly = True
                ssssssfly += 1
                if whowins == 'b':
                    bwin_ssssssfly += 1
                continue
        elif is_starKomoku([step2,step4]) or is_komokuStar([step2,step4]):  #白星小目或小目星开局
            #print(fname,"二连星对星小目开局")
            have_ssssk = True
            ssssk += 1
            if whowins == 'b':
                bwin_ssssk += 1
            continue
        if is_KK([step2,step4]):    #白双小目开局
            #print(fname,"二连星对双小目开局")
            have_ssskk = True
            ssskk += 1
            if whowins == 'b':
                bwin_ssskk += 1
            continue
    elif is_starKomoku([step1,step3]) or is_komokuStar([step1,step3]):  #黑星小目或小目星开局
        #print('黑星小目开局')
        if is_starKomoku([step2,step4]) or is_komokuStar([step2,step4]):    #白星小目或小目星开局
            #print(fname,"星小目对星小目开局")
            have_sksk = True
            sksk += 1
            if whowins == 'b':
                bwin_sksk += 1
            continue
        if is_sameSideStar([step2,step4]):  #白二连星开局
            #print(fname,"星小目对二连星开局")
            have_sksss = True
            sksss += 1
            if whowins == 'b':
                bwin_sksss += 1
            continue
        if is_diagonalStar([step2,step4]):   #白对角星
            #print(fname,"星小目对对角星开局")
            have_skds = True
            skds += 1
            if whowins == 'b':
                bwin_skds += 1
            continue
        if is_KK([step2,step4]):    #白双小目开局
            #print(fname,"星小目对双小目开局")
            have_skkk = True
            skkk += 1
            if whowins == 'b':
                bwin_skkk += 1
            continue
    elif is_KK([step1,step3]):  #黑双小目开局
        #print('黑双小目开局')
        if is_starKomoku([step2,step4]) or is_komokuStar([step2,step4]):    #白星小目或小目星开局
            #print(fname,"双小目对星小目开局")
            have_kksk = True
            kksk += 1
            if whowins == 'b':
                bwin_kksk += 1
            continue
        if is_sameSideStar([step2,step4]):  #白二连星开局
            #print(fname,"双小目对二连星开局")
            have_kksss = True
            kksss += 1
            if whowins == 'b':
                bwin_kksss += 1
            continue
        if is_diagonalStar([step2,step4]):   #白对角星
            #print(fname,"双小目对对角星开局")
            have_kkds = True
            kkds += 1
            if whowins == 'b':
                bwin_kkds += 1
            continue
        if is_KK([step2,step4]):    #白双小目开局
            #print(fname,"双小目对双小目开局")
            have_kkkk = True
            kkkk += 1
            if whowins == 'b':
                bwin_kkkk += 1
            continue
        if is_33K([step2,step4]):    #白三三小目开局
            #print(fname,"双小目对三三小目开局")
            have_kk33k = True
            kk33k += 1
            if whowins == 'b':
                bwin_kk33k += 1
            continue
        if is_K33([step2,step4]):    #白小目三三开局
            #print(fname,"双小目对小目三三开局")
            have_kkk33 = True
            kkk33 += 1
            if whowins == 'b':
                bwin_kkk33 += 1
            continue
    elif is_S33([step1,step3]):  #黑星三三开局
        #print('黑星三三开局')
        if is_starKomoku([step2,step4]) or is_komokuStar([step2,step4]):    #白星小目或小目星开局
            #print(fname,"星三三对星小目开局")
            have_s33sk = True
            s33sk += 1
            if whowins == 'b':
                bwin_s33sk += 1
            continue
        if is_sameSideStar([step2,step4]):  #白二连星开局
            #print(fname,"星三三对二连星开局")
            have_s33sss = True
            s33sss += 1
            if whowins == 'b':
                bwin_s33sss += 1
            continue
        if is_diagonalStar([step2,step4]):   #白对角星
            #print(fname,"星三三对对角星开局")
            have_s33ds = True
            s33ds += 1
            if whowins == 'b':
                bwin_s33ds += 1
            continue
        if is_KK([step2,step4]):    #白双小目开局
            #print(fname,"星三三对双小目开局")
            have_s33kk = True
            s33kk += 1
            if whowins == 'b':
                bwin_s33kk += 1
            continue
    elif is_S54([step1,step3]):  #黑星高目开局
        #print('黑星高目开局')
        if is_starKomoku([step2,step4]) or is_komokuStar([step2,step4]):    #白星小目或小目星开局
            #print(fname,"星高目对星小目开局")
            have_s54sk = True
            s54sk += 1
            if whowins == 'b':
                bwin_s54sk += 1
            continue
        if is_sameSideStar([step2,step4]):  #白二连星开局
            #print(fname,"星高目对二连星开局")
            have_s54sss = True
            s54sss += 1
            if whowins == 'b':
                bwin_s54sss += 1
            continue
        if is_diagonalStar([step2,step4]):   #白对角星
            #print(fname,"星高目对对角星开局")
            have_s54ds = True
            s54ds += 1
            if whowins == 'b':
                bwin_s54ds += 1
            continue
        elif is_S33([step2,step4]):  #白星33开局
            #print(fname,"星高目对星三三开局")
            have_s54s33 = True
            s54s33 += 1
            if whowins == 'b':
                bwin_s54s33 += 1
            continue
    elif is_2starSansan([step1,step2,step3]):
        #print(fname,"星位后点三三开局")
        have_twoStar33 = True
        twoStar33 += 1
        if whowins == 'b':
            bwin_twoStar33 += 1
        continue
    elif is_KS33([step1,step2,step3]):
        #print(fname,"小目星位后点三三开局")
        have_ks33 = True
        ks33 += 1
        if whowins == 'b':
            bwin_ks33 += 1
        continue
    elif is_SKFly([step1,step2,step3]):
        #print(fname,"星位小目后黑低挂开局")
        have_skfly = True
        skfly += 1
        if whowins == 'b':
            bwin_skfly += 1
        continue
    print(fname,"未知开局")

if have_dsds33: print('对角星点三三',bwin_dsds33,dsds33,"黑胜率{:.2f}%".format(bwin_dsds33*1.0/dsds33*100))
if have_dsdsfly: print('对角星小飞挂',bwin_dsdsfly,dsdsfly,"黑胜率{:.2f}%".format(bwin_dsdsfly*1.0/dsdsfly*100))
if have_dssk: print('对角星对星对角小目',bwin_dssk,dssk,"黑胜率{:.2f}%".format(bwin_dssk*1.0/dssk*100))
if have_dss33: print('对角星对星三三',bwin_dss33,dss33,"黑胜率{:.2f}%".format(bwin_dss33*1.0/dss33*100))
if have_dskk: print('对角星对双小目',bwin_dskk,dskk,"黑胜率{:.2f}%".format(bwin_dskk*1.0/dskk*100))

if have_ssssss33: print(u'二连星点三三',bwin_ssssss33,ssssss33,"黑胜率{:.2f}%".format(bwin_ssssss33*1.0/ssssss33*100))
if have_ssssssfly: print(u'二连星小飞挂',bwin_ssssssfly,ssssssfly,"黑胜率{:.2f}%".format(bwin_ssssssfly*1.0/ssssssfly*100))
if have_ssssk: print(u'二连星对星小目',bwin_ssssk,ssssk,"黑胜率{:.2f}%".format(bwin_ssssk*1.0/ssssk*100))
if have_ssskk: print(u'二连星对双小目',bwin_ssskk,ssskk,"黑胜率{:.2f}%".format(bwin_ssskk*1.0/ssskk*100))

if have_sksk: print('星小目对星小目',bwin_sksk,sksk,"黑胜率{:.2f}%".format(bwin_sksk*1.0/sksk*100))
if have_sksss: print('星小目对二连星',bwin_sksss,sksss,"黑胜率{:.2f}%".format(bwin_sksss*1.0/sksss*100))
if have_skds: print('星小目对对角星',bwin_skds,skds,"黑胜率{:.2f}%".format(bwin_skds*1.0/skds*100))
if have_skkk: print('星小目对双小目',bwin_skkk,skkk,"黑胜率{:.2f}%".format(bwin_skkk*1.0/skkk*100))

if have_s33sk: print('星三三对星小目',bwin_s33sk,s33sk,"黑胜率{:.2f}%".format(bwin_s33sk*1.0/s33sk*100))
if have_s33sss: print('星三三对二连星',bwin_s33sss,s33sss,"黑胜率{:.2f}%".format(bwin_s33sss*1.0/s33sss*100))
if have_s33ds: print('星三三对对角星',bwin_s33ds,s33ds,"黑胜率{:.2f}%".format(bwin_s33ds*1.0/s33ds*100))
if have_s33kk: print('星三三对双小目',bwin_s33kk,s33kk,"黑胜率{:.2f}%".format(bwin_s33kk*1.0/s33kk*100))

if have_kksk: print('双小目对星小目',bwin_kksk,kksk,"黑胜率{:.2f}%".format(bwin_kksk*1.0/kksk*100))
if have_kksss: print('双小目对二连星',bwin_kksss,kksss,"黑胜率{:.2f}%".format(bwin_kksss*1.0/kksss*100))
if have_kkds: print('双小目对对角星',bwin_kkds,kkds,"黑胜率{:.2f}%".format(bwin_kkds*1.0/kkds*100))
if have_kkkk: print('双小目对双小目',bwin_kkkk,kkkk,"黑胜率{:.2f}%".format(bwin_kkkk*1.0/kkkk*100))
if have_kk33k: print('双小目对三三小目',bwin_kk33k,kk33k,"黑胜率{:.2f}%".format(bwin_kk33k*1.0/kk33k*100))
if have_kkk33: print('双小目对小目三三',bwin_kkk33,kkk33,"黑胜率{:.2f}%".format(bwin_kkk33*1.0/kkk33*100))

if have_s54sk: print('星高目对星小目',bwin_s54sk,s54sk,"黑胜率{:.2f}%".format(bwin_s54sk*1.0/s54sk*100))
if have_s54sss: print('星高目对二连星',bwin_s54sss,s54sss,"黑胜率{:.2f}%".format(bwin_s54sss*1.0/s54sss*100))
if have_s54ds: print('星高目对对角星',bwin_s54ds,s54ds,"黑胜率{:.2f}%".format(bwin_s54ds*1.0/s54ds*100))
if have_s54s33: print('星高目对星三三',bwin_s54s33,s54s33,"黑胜率{:.2f}%".format(bwin_s54s33*1.0/s54s33*100))

if have_twoStar33: print(u'星位后点三三',bwin_twoStar33,twoStar33,"黑胜率{:.2f}%".format(bwin_twoStar33*1.0/twoStar33*100))
if have_ks33: print(u'小目星位后点三三',bwin_ks33,ks33,"黑胜率{:.2f}%".format(bwin_ks33*1.0/ks33*100))
if have_skfly: print(u'星位小目后黑低挂',bwin_skfly,skfly,"黑胜率{:.2f}%".format(bwin_skfly*1.0/skfly*100))

if num>0:   print("黑胜局数",bwin,"总局数",num,"黑胜率{:.2f}%".format(bwin*1.0/num*100))
