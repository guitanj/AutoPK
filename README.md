# AutoPK
Try to draw the elo-playouts curve of those leelazero networks.

Based on the elfv0, auto self-fight with the gradual growth of playouts(100 games per fight), 10 vs 2,50 vs 10,100 vs 50 and so on...now max 25600 vs 12800, Define elfv0 2 playouts with 2000 elo, generate baseline elo data.

then use other weights to fight with elfv0 with same playouts(100 games per fight),use the winning percentage to calculate Elo values of the corresponding playouts, Eventually draw the elo-playouts curve.

这个程序的目标是画leelaZero权重的棋力曲线(elo-playouts)。

以ELFV0为基础，使用其逐步增长的playouts自动自我对战（每轮对战100局），根据胜率计算出对应playouts的elo值，进一步画出棋力曲线来。

然后用其他权重同po对战ELFV0（每轮对战100局），用胜率计算出对应的elo值，画出测试权重的棋力曲线。以ELFV0权重2po为2000elo值。

# Advantage
Automatically save versus, and to save every step of the situation.

Same playouts pk:save score, time spending.

Same time pk:save the average playouts.

Parameter adjustment of freedom, the engine can also be freely adjusted.

Going to Python programming, you can change the program whatever you like.

自动保存对战棋谱，并且保存每一步的胜率情况

保存对战比分、对战时长，同时间对战保存平均playouts数据

参数调整自由，引擎也可以自由调整

会python编程的话，还可以变形出各种测试花样来

# To do list
GUI interface, animate the progress while fighting

Versus breakpoints saved and restored

图形配置界面，动态显示下棋对战进展

对战断点保存以及恢复
    
# Curves
![权重playouts值对应elo分对照表-基于各自100局对战测试（设定ELFV0 2po为2000）](https://github.com/guitanj/AutoPK/blob/master/updateto204.jpg "playouts vs elo list")
![Screen-shot of elo-playouts Curves](https://github.com/guitanj/AutoPK/blob/master/Curves.jpg "Screen-shot of elo-playouts Curves")

# Requirements
This program requires python2.X or python3.X environment, thanks to Matthew woodcraft's gomill & sgfmill module.

本程序需要python2.x or python3.X环境，感谢Matthew Woodcraft的gomill & sgfmill模块。

# How to use
Modify the program, mainly the last paragraph.I noted some detailed description. 

Attention:Path to the engine and weights needs to be modified.

Results are automatically saved in PKResult.txt file.

Program with same playouts:goEngin-SamePoPK.py

Program with same time:goEngin-SameTimePK.py

修改程序，主要是最后一段，已做详细的说明。需要特别注意的是引擎以及权重的路径需要改成你自己的

另外，程序在第一次跑时，会因为LeelaZero在新的路径下会生成新的显卡运行参数（leelaz_opencl_tuning），会比较慢或者调参失败中断退出（如20xx系最新显卡），重新运行程序就好。

生成的对战结果会自动保存在PKResult.txt文件中

同playouts的对战程序为：goEngin-SamePoPK.py or goEngin-SamePoPK-PY3.py for python 3.X

同时间的对战程序为：goEngin-SameTimePK.py or goEngin-SameTimePK-PY3.py for python 3.X

See " # " note to modify the part of the description :

参见“#”注释的可修改部分说明：

if __name__ == "__main__":

    Program with same playouts:
    同playouts的对战程序：
    playoutb = 100 #You can modify : initial playouts with black weight 可修改：执黑权重的初始po值
    playoutw = 100 #You can modify : initial playouts with white weight 可修改：执白权重的初始po值    
    weightb='200.gz' #You can modify : black weight 可修改：执黑权重    
    weightw='ELFV0.gz' #You can modify : white weight 可修改：执白权重    
    while playoutb <= 12800: #You can modify : max playouts to test 可修改：测试po的上限    
        t0 = datetime.datetime.now()        
        blackW = 0        
        whiteW = 0        
        for i in range(100): #You can modify : break at 39th game, change to range(39,100) 可修改：第39盘中断了的话，可以改为，如：range(39,100)继续测试        
            whoWin = startPK(i,playoutb,playoutw,weightb,weightw)            
            if whoWin == 'b':            
                blackW += 1                
            elif whoWin == 'w':            
                whiteW += 1                
            elif whoWin == 'x':            
                print 'Too many moves Found:', whoWin                
            else:            
                print 'Error Found:', whoWin                
            print weightb+' B-'+str(playoutb)+'po vs '+weightw+' W-'+str(playoutw)+'po', blackW,':', whiteW            
        t1 = datetime.datetime.now()        
        resfile = open('PKResult.txt','a')        
        resfile.write('From:'+t0.strftime('%b-%d-%y %H:%M:%S')+' to '+ \        
                      t1.strftime('%b-%d-%y %H:%M:%S')+ \                      
                      '. Spend '+str((t1-t0).total_seconds())+'s\n')                      
        resfile.write(weightb+' B-'+str(playoutb)+'po vs '+weightw+' W-'+str(playoutw)+'po '+str(blackW)+":"+str(whiteW)+'\n')     
        resfile.close()        
        playoutb = playoutb *2 #You can modify : next playouts to be tested 可修改：执黑权重测试完毕100局后，下一轮100局的po值增加量        
        playoutw = playoutw *2 #You can modify : same with the upper line 可修改：一般改成和上一行一样
        #modifications to the engine and its parameters & working directory, you may goto line 204 and 246, note the number of rows may change as the program is modified, search "pbscmd" "pwscmd" variables.
        #引擎及引擎参数、引擎的工作路径的修改要到204行和246行附近，注意行数可能随着程序被修改而变化，搜索pbscmd、pwscmd变量比较准确

    Program with same time:
    同时间的对战程序：
    spendTime = 3 #You can modify : set pk time 可修改：设定pk时间
    weightb='197.gz' #You can modify : black weight 可修改：执黑权重
    weightw='LeelaMaster_GX5B.gz' #You can modify : white weight 可修改：执白权重
    while spendTime <= 3: #You can modify : max of time 可修改：设定pk上限时间
        t0 = datetime.datetime.now()
        blackW = 0
        whiteW = 0
        for i in range(100): #You can modify : amount of each round 可修改：每一轮测试的对局数
            whoWin = startPK(i,weightb,weightw,spendTime)
            if whoWin == 'b':
                blackW += 1
            elif whoWin == 'w':
                whiteW += 1
            elif whoWin == 'x':
                print 'Too many moves Found:', whoWin
            else:
                print 'Error Found:', whoWin
            print weightb+' B vs '+weightw+' W'+str(spendTime)+'s', blackW,':', whiteW
        t1 = datetime.datetime.now()
        resfile = open('PKResult.txt','a')
        resfile.write('From:'+t0.strftime('%b-%d-%y %H:%M:%S')+' to '+ \
                      t1.strftime('%b-%d-%y %H:%M:%S')+ \
                      '. Spend '+str((t1-t0).total_seconds())+'s\n')
        resfile.write(weightb+' B vs '+weightw+' W'+str(spendTime)+'s '+str(blackW)+":"+str(whiteW)+'\n')
        #resfile.write(weightb+' B-t2 vs '+weightw+' W-t4 '+str(blackW)+":"+str(whiteW)+'\n')
        resfile.close()
        spendTime = spendTime*2 #You can modify : set increment of time with each round 可修改：设定每一轮pk时间的增量
        #modifications to the engine and its parameters & working directory, you may goto line 204 and 246, note the number of rows may change as the program is modified, search "pbscmd" "pwscmd" variables.
        #引擎及引擎参数、引擎的工作路径的修改要到204行和246行，注意行数可能随着程序被修改而变化，搜索pbscmd、pwscmd变量比较准确
