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
#高目
t54Point = [(r,c) for r in [3,15] for c in [4,14]]
t54Point += [(r,c) for r in [4,14] for c in [3,15]]
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
#星三三
openning_S33 = [starPoint,sansanPoint]
#三三星
openning_33S = [sansanPoint,starPoint]
#星高目
openning_S54 = [starPoint,t54Point]
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
bwin = wwin = num = 0

dsds33=dsdsfly=dssk=dsks=dss33=ds33s=0
ssssss33=ssssssfly=ssssk=sssks=ssskk=0
kssk=kssss=ksks=kskk=0
sksk=sksss=skds=skkk=skks=0
kksk=kksss=kkds=kkkk=0
s54sk=s54sss=s54ds=s54ks=0
twoStar33=ks33=0

have_dsds33=have_dsdsfly=have_dssk=have_dsks=have_dss33=have_ds33s=False
have_ssssss33=have_ssssssfly=have_ssssk=have_sssks=have_ssskk=False
have_kssk=have_kssss=have_ksks=have_kskk=False
have_sksk=have_sksss=have_skds=have_skkk=have_skks=False
have_kksk=have_kksss=have_kkds=have_kkkk=False
have_s54sk=have_s54sss=have_s54ds=have_s54ks=False
have_twoStar33=have_ks33=False

bwin_dsds33=bwin_dsdsfly=bwin_dssk=bwin_dsks=bwin_dss33=bwin_ds33s=0
bwin_ssssss33=bwin_ssssssfly=bwin_ssssk=bwin_sssks=bwin_ssskk=0
bwin_kssk=bwin_kssss=bwin_ksks=bwin_kskk=0
bwin_sksk=bwin_sksss=bwin_skds=bwin_skkk=bwin_skks=0
bwin_kksk=bwin_kksss=bwin_kkds=bwin_kkkk=0
bwin_s54sk=bwin_s54sss=bwin_s54ds=bwin_s54ks=0
bwin_twoStar33=bwin_ks33=0

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

    whowins = fname[-6]
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
            #print('对角星vs对角星',row5,col5)
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
        elif is_starKomoku([step2,step4]):  #白星对角小目开局
            #print(fname,"对角星对星对角小目开局")
            have_dssk = True
            dssk += 1
            if whowins == 'b':
                bwin_dssk += 1
            continue
        elif is_komokuStar([step2,step4]):  #白小目星开局
            #print(fname,"对角星对小目星开局")
            have_dsks = True
            dsks += 1
            if whowins == 'b':
                bwin_dsks += 1
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
            have_ds33s = True
            ds33s += 1
            if whowins == 'b':
                bwin_ds33s += 1
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
        elif is_starKomoku([step2,step4]):  #白星小目开局
            #print(fname,"二连星对星小目开局")
            have_ssssk = True
            ssssk += 1
            if whowins == 'b':
                bwin_ssssk += 1
            continue
        elif is_komokuStar([step2,step4]):  #白小目星开局
            #print(fname,"二连星对小目星开局")
            have_sssks = True
            sssks += 1
            if whowins == 'b':
                bwin_sssks += 1
            continue
        if is_KK([step2,step4]):    #白双小目开局
            #print(fname,"二连星对双小目开局")
            have_ssskk = True
            ssskk += 1
            if whowins == 'b':
                bwin_ssskk += 1
            continue
    elif is_komokuStar([step1,step3]):  #黑小目星开局
        #print('黑小目星开局')
        if is_starKomoku([step2,step4]):    #白星小目开局
            #print(fname,"小目星对星小目开局")
            have_kssk = True
            kssk += 1
            if whowins == 'b':
                bwin_kssk += 1
            continue
        if is_sameSideStar([step2,step4]):  #白二连星开局
            #print(fname,"小目星对二连星开局")
            have_kssss = True
            kssss += 1
            if whowins == 'b':
                bwin_kssss += 1
            continue
        if is_komokuStar([step2,step4]):    #白小目星开局
            #print(fname,"小目星对小目星开局")
            have_ksks = True
            ksks += 1
            if whowins == 'b':
                bwin_ksks += 1
            continue
        if is_KK([step2,step4]):    #白双小目开局
            #print(fname,"小目星对双小目开局")
            have_kskk = True
            kskk += 1
            if whowins == 'b':
                bwin_kskk += 1
            continue
    elif is_starKomoku([step1,step3]):  #黑星小目开局
        #print('黑星小目开局')
        if is_starKomoku([step2,step4]):    #白星小目开局
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
        if is_komokuStar([step2,step4]):   #白小目星
            #print(fname,"星小目对小目星开局")
            have_skks = True
            skks += 1
            if whowins == 'b':
                bwin_skks += 1
            continue
    elif is_KK([step1,step3]):  #黑双小目开局
        #print('黑双小目开局')
        if is_starKomoku([step2,step4]):    #白星小目开局
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
    elif is_S54([step1,step3]):  #黑星高目开局
        #print('黑星高目开局')
        if is_starKomoku([step2,step4]):    #白星小目开局
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
        if is_komokuStar([step2,step4]):   #白小目星
            #print(fname,"星高目对小目星开局")
            have_s54ks = True
            s54ks += 1
            if whowins == 'b':
                bwin_s54ks += 1
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
    print(fname,"未知开局")

if have_dsds33: print('对角星点三三',dsds33,"黑胜率{:.2f}%".format(bwin_dsds33/dsds33*100))
if have_dsdsfly: print('对角星小飞挂',dsdsfly,"黑胜率{:.2f}%".format(bwin_dsdsfly/dsdsfly*100))
if have_dssk: print('对角星对星对角小目',dssk,"黑胜率{:.2f}%".format(bwin_dssk/dssk*100))
if have_dsks: print('对角星对小目星',dsks,"黑胜率{:.2f}%".format(bwin_dsks/dsks*100))
if have_dss33: print('对角星对星三三',dss33,"黑胜率{:.2f}%".format(bwin_dss33/dss33*100))
if have_ds33s: print('对角星对三三星',ds33s,"黑胜率{:.2f}%".format(bwin_ds33s/ds33s*100))
print()

if have_ssssss33: print('二连星点三三',ssssss33,"黑胜率{:.2f}%".format(bwin_ssssss33/ssssss33*100))
if have_ssssssfly: print('二连星小飞挂',ssssssfly,"黑胜率{:.2f}%".format(bwin_ssssssfly/ssssssfly*100))
if have_ssssk: print('二连星对星小目',ssssk,"黑胜率{:.2f}%".format(bwin_ssssk/ssssk*100))
if have_sssks: print('二连星对小目星',sssks,"黑胜率{:.2f}%".format(bwin_sssks/sssks*100))
if have_ssskk: print('二连星对双小目',ssskk,"黑胜率{:.2f}%".format(bwin_ssskk/ssskk*100))
print()

if have_kssk: print('小目星对星小目',kssk,"黑胜率{:.2f}%".format(bwin_kssk/kssk*100))
if have_kssss: print('小目星对二连星',kssss,"黑胜率{:.2f}%".format(bwin_kssss/kssss*100))
if have_ksks: print('小目星对小目星',ksks,"黑胜率{:.2f}%".format(bwin_ksks/ksks*100))
if have_kskk: print('小目星对双小目',kskk,"黑胜率{:.2f}%".format(bwin_kskk/kskk*100))
print()

if have_sksk: print('星小目对星小目',sksk,"黑胜率{:.2f}%".format(bwin_sksk/sksk*100))
if have_sksss: print('星小目对二连星',sksss,"黑胜率{:.2f}%".format(bwin_sksss/sksss*100))
if have_skds: print('星小目对对角星',skds,"黑胜率{:.2f}%".format(bwin_skds/skds*100))
if have_skkk: print('星小目对双小目',skkk,"黑胜率{:.2f}%".format(bwin_skkk/skkk*100))
if have_skks: print('星小目对小目星',skks,"黑胜率{:.2f}%".format(bwin_skks/skks*100))
print()

if have_kksk: print('双小目对星小目',kksk,"黑胜率{:.2f}%".format(bwin_kksk/kksk*100))
if have_kksss: print('双小目对二连星',kksss,"黑胜率{:.2f}%".format(bwin_kksss/kksss*100))
if have_kkds: print('双小目对对角星',kkds,"黑胜率{:.2f}%".format(bwin_kkds/kkds*100))
if have_kkkk: print('双小目对双小目',kkkk,"黑胜率{:.2f}%".format(bwin_kkkk/kkkk*100))
print()

if have_s54sk: print('星高目对星小目',s54sk,"黑胜率{:.2f}%".format(bwin_s54sk/s54sk*100))
if have_s54sss: print('星高目对二连星',s54sss,"黑胜率{:.2f}%".format(bwin_s54sss/s54sss*100))
if have_s54ds: print('星高目对对角星',s54ds,"黑胜率{:.2f}%".format(bwin_s54ds/s54ds*100))
if have_s54ks: print('星高目对小目星',s54ks,"黑胜率{:.2f}%".format(bwin_s54ks/s54ks*100))
print()

if have_twoStar33: print('星位后点三三',twoStar33,"黑胜率{:.2f}%".format(bwin_twoStar33/twoStar33*100))
if have_ks33: print('小目星位后点三三',ks33,"黑胜率{:.2f}%".format(bwin_ks33/ks33*100))
print()

#print('',)

print("黑胜率{:.2f}%".format(bwin/num*100))
