# AutoPK
Try to draw the elo-playouts curve of those leelazero networks.这个程序的目标是画leelaZero权重的棋力曲线(elo-playouts)，以ELFV0为基础，使用逐步增长的playouts自动对战，根据胜率计算出对应playouts的elo值，进一步画出棋力曲线来。

# Advantage
    自动保存对战棋谱，并且保存每一步的胜率情况
    保存对战比分、对战时长，同时间对战保存平均playouts数据
    参数调整自由，引擎也可以自由调整
    会python编程的话，还可以变形出各种测试花样来

# To do list
    图形配置界面，动态显示下棋对战进展
    对战断点保存以及恢复

# Requirements
    本程序需要python2.x环境，感谢Matthew Woodcraft的gomill模块。

# How to use
    修改程序，主要是最后一段，已做详细的说明。需要特别注意的是引擎以及权重的路径需要改成你自己的另外，程序在第一次跑时，会因为LeelaZero在新的路径下会生成新的显卡运行参数（leelaz_opencl_tuning），会比较慢或者调参失败中断退出（如20xx系最新显卡），重新运行程序就好。
    生成的对战结果会自动保存在PKResult.txt文件中

    同playouts的对战程序为：goEngin-SamePoPK.py
    同时间的对战程序为：goEngin-SameTimePK.py

参见“#”注释的可修改部分说明：
if __name__ == "__main__":

    同playouts的对战程序：
    playoutb = 100 #可修改：执黑权重的初始po值
    playoutw = 100 #可修改：执白权重的初始po值    
    weightb='200.gz' #可修改：执黑权重    
    weightw='ELFV0.gz' #可修改：执白权重    
    while playoutb <= 12800: #可修改：测试po的上限    
        t0 = datetime.datetime.now()        
        blackW = 0        
        whiteW = 0        
        for i in range(100): #可修改：第39盘中断了的话，可以改为，如：range(39,100)继续测试        
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
        playoutb = playoutb *2 #可修改：执黑权重测试完毕100局后，下一轮100局的po值增加量        
        playoutw = playoutw *2 #可修改：一般改成和上一行一样        
        #引擎及引擎参数的修改要到201行和242行，注意行数可能随着程序被修改而变化，搜索pbscmd、pwscmd变量比较准确

    同时间的对战程序：
    spendTime = 3 #可修改：设定pk时间
    weightb='197.gz' #可修改：执黑权重
    weightw='LeelaMaster_GX5B.gz' #可修改：执白权重
    while spendTime <= 3: #可修改：设定pk上限时间
        t0 = datetime.datetime.now()
        blackW = 0
        whiteW = 0
        for i in range(100): #可修改：每一轮测试的对局数
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
        spendTime = spendTime*2 #可修改：设定每一轮pk时间的增量
        #引擎及引擎参数的修改要到201行和242行，注意行数可能随着程序被修改而变化，搜索pbscmd、pwscmd变量比较准确
