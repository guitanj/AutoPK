# -*- coding: utf-8 -*-
# AutoPK version 1.0 20181122 by Alan@NJ
# version 2.3 20190203 upload to github

import os,sys
import subprocess
from subprocess import Popen, PIPE
from threading import Thread
from Queue import Queue, Empty
from time import sleep
from gomill import sgf
from Tkinter import *
import tkMessageBox as messagebox
import datetime

a2n = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'J':8,'K':9,'L':10,'M':11,'N':12,'O':13,'P':14,'Q':15,'R':16,'S':17,'T':18}

class goEngin():
    def __init__(self, command, cwdstr):
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.CREATE_NEW_CONSOLE \
                     | subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        self.process = Popen(command, bufsize=1,stdin=PIPE, stdout=PIPE, \
                        stderr=PIPE,startupinfo=si,cwd=cwdstr)
        print('leelaz threading is started...',self.process.pid,'poll:',self.process.poll())

        #gtp辅助的运算信息，比如genmove中的过程，胜率，其他选点等都在stderr中输出
        self.stderr_queue = Queue()
        Thread(target=self.consume_stderr).start()
        #print('get stderr threading is started...',self.process.poll())
        
        #程序调用一开始就出错的话，比如命令行用错了，报错信息在stdout中输出
        #运行起来，正常的gtp输出信息在stdout中
        self.stdout_queue = Queue()
        Thread(target=self.consume_stdout).start()
        #print('get stdout threading is started...',self.process.poll())

    #读取stderr信息流，写入stderrQ
    def consume_stderr(self):
        while 1:
            try:
                err_line=self.process.stderr.readline().decode("utf-8")
                if err_line:
                    #print('errout:[[[',err_line,']]]]')
                    self.stderr_queue.put(err_line)
                else:
                    #print("leaving consume_stderr thread")
                    return
            except (Exception) as e:
                print("leaving consume_stderr thread due to exception",e)
                return

    #读取stdout信息流，写入stdoutQ
    def consume_stdout(self):
        while 1:
            try:
                line=self.process.stdout.readline().decode("utf-8")
                if line:
                    #print('stdout:[[[',line,']]]]')
                    self.stdout_queue.put(line)
                else:
                    #print("leaving consume_stdout thread")
                    return
            except (Exception) as e:
                print("leaving consume_stdout thread due to exception",e)
                return

    #向围棋AI写入GTP指令
    def write(self,txt):
        try:
            self.process.stdin.write(txt+"\r\n")
            #print txt
            self.process.stdin.flush()
        except (Exception) as e:
            print("Error while writting to stdin:",e)

    #如果围棋AI刚启动时报错退出，则取得系统报错信息
    def readAns_nowait(self):
        try:
            answer=self.stdout_queue.get_nowait()
            #print('readAns_nowait.1[', answer, ']')
            return answer
        except:
            return None

    #执行围棋AI运算，获取下一招落子
    #或 取得GTP指令返回的信息
    def readAns(self):
        #因为这个是阻塞式读取，所以先判断process还是否存活
        if self.process.poll() == None:
            answer=self.stdout_queue.get()
        else:
            return None
        #print('readAns.1[', answer, ']')
        while answer in ("\n","\r\n","\r"):
            answer=self.stdout_queue.get()
            #print('readAns.2[', answer, ']')
        return answer

    #围棋AI进程刚开始启动时，获取启动进程信息，必须使用非阻塞方式
    #clearErrQ使用
    def readErr_nowait(self):
        try:
            answer=self.stderr_queue.get_nowait()
            while answer in ("\n","\r\n","\r"):
                answer=self.stderr_queue.get_nowait()
            return answer
        except:
            return None

    #暂时没有使用
    def readErr(self):
        try:
            #因为这个是阻塞式读取，所以先判断process还是否存活
            if self.process.poll() == None:
                answer=self.stderr_queue.get()
                return answer
            else:
                return None
        except:
            return None

    #读取errQ并返回信息
    def clearErrQ(self):
        returnStr = ''
        try:
            gotErrStr = self.readErr_nowait()
            while gotErrStr != None:
                #print '<',gotErrStr[:-2],'>'
                returnStr += gotErrStr
                gotErrStr = self.readErr_nowait()
            return returnStr
        except:
            return None

    def quit(self):
        #print("<in quit thread...>")
        self.write("quit")

    def terminate(self):
        t=10
        while 1:
            #print("<in terminate thread...>")
            self.quitting_thread.join(0.0)
            if not self.quitting_thread.is_alive():
                #print("The threading has quitted properly")
                break
            elif t==0:
                print("The threading is still running...")
                print("Forcefully closing it now!")
                break
            t-=1
            print("Waiting for the threading to close",t,"s")
            sleep(1)
        
        try: self.process.kill()
        except: pass
        try: self.process.stdin.close()
        except: pass
            
    def close(self):
        #print("Now closing")
        self.quitting_thread=Thread(target=self.quit)
        self.quitting_thread.start()
        #print("<quit thread started>")
        Thread(target=self.terminate).start()
        #print("<terminate thread started>")

#围棋落子坐标转换 -> GTP棋谱格式坐标
def a2num(s):
    try:
        return (a2n[s[0].upper()],int(s[1:])-1)
    except:
        print '----Unkown error:',s
        return (a2n[s[0].upper()],int(s[1:])-1)

#取得下一手相关信息：落子点、胜率、后几步走法、playouts
def getStepInfo(infotxt,gotAns):
    iLines = infotxt.split('\r\n')
    step,winrate,lcbrate,mightMoves,povalue = None,None,None,None,None
    # Old:    G14 ->       2 (V: 92.34%) (N:  9.63%) PV: G14 H14
    # LZ0.17: D17 ->     102 (V: 45.56%) (LCB: 42.97%) (N:  5.52%) PV: D17 R17 D4 Q3 D14 Q5 C6 C12 K3\r\n
    for eachline in iLines:
        #print eachline
        if eachline.startswith(' ') and eachline.count('%')>=2:
            step = eachline[1:eachline.find(' ->')].strip()
            steplist = eachline.split(')')
            # D17 ->     102 (V: 45.56%
            # (LCB: 42.97%
            # (N:  5.52%
            # PV: D17 R17 D4 Q3 D14 Q5 C6 C12 K3
            for i in range(len(steplist)):
                if steplist[i].find('V:') != -1 and winrate is None:
                    winrate = steplist[i][steplist[i].find('V:')+3:steplist[i].find('%')]
                if steplist[i].find('LCB:') != -1:
                    lcbrate = steplist[i][steplist[i].find('LCB:')+5:steplist[i].find('%')]
                if steplist[i].find('PV:') != -1:
                    mightMoves = steplist[i][steplist[i].find('PV:')+4:-2]
            if step == gotAns:
                #print(step,winrate,lcbrate,mightMoves,'gotAns:',gotAns,step == gotAns)
                break
            else:
                if gotAns!='resign':
                    print(step,winrate,lcbrate,mightMoves,'gotAns:',gotAns,step == gotAns)
                step,winrate,lcbrate,mightMoves = None,None,None,None
                continue
    for eachline in iLines:     #4 visits, 1056 nodes, 3 playouts, 3 n/s
        if eachline.count('visits')==1 and eachline.count('playouts')==1:
            povalue = eachline[eachline.find('nodes,')+7:eachline.find('playouts')-1]
            #print povalue
            break
    return step,winrate,lcbrate,mightMoves,povalue

def startPK(num,weightb,weightw,spendTime):
    g = sgf.Sgf_game(size=19)
    g.root.set("KM",'7.5')
    g.root.set("PB",weightb)
    g.root.set("PW",weightw)
    
    #pbscmd = 'D:\\Go\\leela-zero-0.16-win64\\leelaz.exe -g --noponder -t 2 -wD:\\Go\\weights\\' \
    pbscmd = 'E:\\Go\\20190219GCPNext\\leelaz.exe -g --noponder --precision half -wE:\\Go\\Ana_1.26\\weight\\' \
             +weightb+' --gpu 0 -p 100000'
    pbcwdstr = 'E:\\Go\\20190219GCPNext'
    #print pbscmd
    pbcommand = pbscmd.split(' ')
    try:
        pb = goEngin(pbcommand, pbcwdstr)
    except (Exception) as e:
        print("Error found:",e)
        return None
    
    processTest = True
    while processTest:
        #print 'test pb alive',pb.process.poll()
        if pb.process.poll() is None:
            pass
        else:
            gotStdStr = pb.readAns_nowait()
            while gotStdStr != None:
                print gotStdStr
                gotStdStr = pb.readAns_nowait()
            print "process start failed"
            return None
        sleep(0.001)
        gotErrStr = pb.readErr_nowait()
        if gotErrStr!=None:
            while gotErrStr!=None:
                if gotErrStr[:24] == 'Setting max tree size to':
                    print 'pb.1',gotErrStr[:-2]
                    print 'Black is ready.'
                    processTest = False
                else:
                    #print 'pb.1',gotErrStr[:-2]
                    pass
                if pb.process.poll() is None:
                    pass
                else:
                    print "process start failed"
                    return None
                gotErrStr = pb.readErr_nowait()

    #pwscmd = 'D:\\Go\\leela-zero-0.16-win64\\leelaz.exe -g --noponder -t 2 -wD:\\Go\\weights\\' \
    pwscmd = 'E:\\Go\\1130fastexit-tensor-accum\\leelaz.exe -g --noponder -t 1 --precision half --batchsize 4 -wE:\\Go\\Ana_1.26\\weight\\' \
             +weightw+' --gpu 0 -p 100000'
    pwcwdstr = 'E:\\Go\\1130fastexit-tensor-accum'
    #print pwscmd
    pwcommand = pwscmd.split(' ')
    try:
        pw = goEngin(pwcommand, pwcwdstr)
    except (Exception) as e:
        print("Error found:",e)
        return None

    processTest = True
    while processTest:
        #print 'test pw alive',pw.process.poll()
        if pw.process.poll() is None:
            pass
        else:
            gotStdStr = pw.readAns_nowait()
            while gotStdStr != None:
                print gotStdStr
                gotStdStr = pw.readAns_nowait()
            print "process start failed"
            return None
        sleep(0.001)
        gotErrStr = pw.readErr_nowait()
        if gotErrStr!=None:
            while gotErrStr!=None:
                if gotErrStr[:24] == 'Setting max tree size to':
                    print 'pw.1',gotErrStr[:-2]
                    print 'White is ready.'
                    processTest = False
                else:
                    #print 'pw.1',gotErrStr[:-2]
                    pass
                if pw.process.poll() is None:
                    pass
                else:
                    print "process start failed"
                    return None
                gotErrStr = pw.readErr_nowait()

    initCmds = ['version','boardsize 19','komi 7.5','time_settings 0 '+str(spendTime+1)+' 1']

    for cmd in initCmds:
        print 'Sending pb[',cmd,']',
        try:
            pb.write(cmd)
        except (Exception) as e:
            print("Error found:",e)
            return None
        gotAns = pb.readAns()
        print 'pb Answer is :', gotAns[:-2]
        pb.clearErrQ()

    for cmd in initCmds:
        print 'Sending pw[',cmd,']',
        try:
            pw.write(cmd)
        except (Exception) as e:
            print("Error found:",e)
            return None            
        gotAns = pw.readAns()
        print 'pw Answer is :', gotAns[:-2]
        pw.clearErrQ()

    #开始对战
    stepTime1 = datetime.datetime.now()
    startTime = stepTime1
    resigned = False
    black_po = 0    #黑棋po总值
    white_po = 0    #白棋po总值
    cmdStr = 'genmove b'
    pb.write(cmdStr)
    gotAns = pb.readAns()
    #print 'Black First Move is :', gotAns
    sleep(0.01)
    #取得对局下一手相关信息：落子点、胜率、预测后几步走法、playouts
    errQTime1 = datetime.datetime.now() #记录读取errQ的时长
    strInfo = pb.clearErrQ()
    errQTime2 = datetime.datetime.now() #记录读取errQ的时长
    firstStep,stepWinrate,lcbrate,mightMoves,povalue = getStepInfo(strInfo,gotAns[2:-2])
    if (stepWinrate == None or povalue == None) and gotAns[2:-2]!='resign':
        print repr(strInfo)

    cmdStr = 'play b ' + gotAns[2:-2]
    sgfStr=gotAns[2:-2]    #去除末尾的\r\n
    node = g.extend_main_sequence()
    node.set_move('b', a2num(sgfStr))
    if stepWinrate!=None and povalue!=None:
        if lcbrate!=None:
            node.set("C",stepWinrate+'% lcb:'+lcbrate+'% po:'+povalue)
        else:
            node.set("C",stepWinrate+'% po:'+povalue)
        black_po += int(povalue)

    steps = 1
    whowins = ''

    while not resigned:
        pw.write(cmdStr)
        stepTime2 = datetime.datetime.now()
        print steps,cmdStr,'WinRate:(',stepWinrate,'%)(lcb:',lcbrate,'%)(po:',povalue,')', \
              (stepTime2-stepTime1).total_seconds(),'s',(errQTime2-errQTime1).total_seconds(),'s'
        steps += 1
        gotAns = pw.readAns()
        #print 'White answer is :', gotAns
        cmdStr = 'genmove w'
        pw.write(cmdStr)
        gotAns = pw.readAns()
        #print 'White answer is :', gotAns
        sleep(0.01)
        #取得对局下一手相关信息：落子点、胜率、预测后几步走法
        errQTime1 = datetime.datetime.now() #记录读取errQ的时长
        strInfo = pw.clearErrQ()
        errQTime2 = datetime.datetime.now() #记录读取errQ的时长
        firstStep,stepWinrate,lcbrate,mightMoves,povalue = getStepInfo(strInfo,gotAns[2:-2])
        if (stepWinrate == None or povalue == None) and gotAns[2:-2]!='resign':
            print repr(strInfo)
            
        if gotAns[2:] == u'pass\r\n':
            sgfStr += ','+gotAns[2:-2]
            node = g.extend_main_sequence()
            node.set_move('w', None)
            cmdStr = 'play w ' + gotAns[2:-2]
        elif gotAns[2:] != u'resign\r\n':
            sgfStr += ','+gotAns[2:-2]
            node = g.extend_main_sequence()
            node.set_move('w', a2num(gotAns[2:-2]))
            if stepWinrate!=None and povalue!=None:
                if lcbrate!=None:
                    node.set("C",stepWinrate+'% lcb:'+lcbrate+'% po:'+povalue)
                else:
                    node.set("C",stepWinrate+'% po:'+povalue)
                white_po += int(povalue)
            cmdStr = 'play w ' + gotAns[2:-2]
        else:
            print 'White resigned!'
            node = g.extend_main_sequence()
            node.set_move('w', None)
            node.set("C", "White resigned!")
            g.root.set('RE','B+')
            resigned = True
            whowins = 'b'
            endTime = datetime.datetime.now()
            continue

        pb.write(cmdStr)
        stepTime1 = datetime.datetime.now()
        print steps,cmdStr,'WinRate:(',stepWinrate,'%)(lcb:',lcbrate,'%)(po:',povalue,')', \
              (stepTime1-stepTime2).total_seconds(),'s',(errQTime2-errQTime1).total_seconds(),'s'
        steps += 1
        gotAns = pb.readAns()
        #print 'Black answer is :', gotAns
        cmdStr = 'genmove b'
        pb.write(cmdStr)
        gotAns = pb.readAns()
        #print 'Black answer is :', gotAns
        sleep(0.01)
        #取得对局下一手相关信息：落子点、胜率、预测后几步走法
        errQTime1 = datetime.datetime.now() #记录读取errQ的时长
        strInfo = pb.clearErrQ()
        errQTime2 = datetime.datetime.now() #记录读取errQ的时长
        firstStep,stepWinrate,lcbrate,mightMoves,povalue = getStepInfo(strInfo,gotAns[2:-2])
        if (stepWinrate == None or povalue == None) and gotAns[2:-2]!='resign':
            print repr(strInfo)
            
        if gotAns[2:] == u'pass\r\n':
            sgfStr += ','+gotAns[2:-2]
            node = g.extend_main_sequence()
            node.set_move('b', None)
            cmdStr = 'play b ' + gotAns[2:-2]
        elif gotAns[2:] != u'resign\r\n':
            sgfStr += ','+gotAns[2:-2]
            node = g.extend_main_sequence()
            node.set_move('b', a2num(gotAns[2:-2]))
            if stepWinrate!=None and povalue!=None:
                if lcbrate!=None:
                    node.set("C",stepWinrate+'% lcb:'+lcbrate+'% po:'+povalue)
                else:
                    node.set("C",stepWinrate+'% po:'+povalue)
                black_po += int(povalue)
            cmdStr = 'play b ' + gotAns[2:-2]
        else:
            print 'Black resigned!'
            node = g.extend_main_sequence()
            node.set_move('b', None)
            node.set("C", "Black resigned!")
            g.root.set('RE','W+')
            resigned = True
            whowins = 'w'
            endTime = datetime.datetime.now()
            continue

        if steps >= 500:
            print 'Too many Moves!'
            node.set("C", "Too many Moves!")
            resigned = True
            whowins = 'x'
            endTime = datetime.datetime.now()
            continue            

    #计算黑白平均po值
    if steps % 2 == 0:  #偶数说明是白投降了
        avgBlackPo = black_po/(steps/2)
        avgWhitePo = white_po/(steps/2-1)
    else:
        avgBlackPo = black_po/((steps-1)/2)
        avgWhitePo = white_po/((steps-1)/2)

    print '本局共耗时：',(endTime-startTime).total_seconds(),'s','avgBpo:',avgBlackPo,'avgWpo:',avgWhitePo
    #print sgfStr
    sgffile = open(weightb+' B'+str(avgBlackPo)+'po vs '+weightw+' W'+str(avgWhitePo)+'po-'+str(spendTime)+'s-'+str(num)+'-'+whowins+'+.sgf','w')
    sgffile.write(g.serialise())
    sgffile.close()        
    pb.close()
    pw.close()
    return whowins

if __name__ == "__main__":

    spendTime = 3 #可修改：设定pk时间
    weightb='197.gz' #可修改：执黑权重
    weightw='LeelaMaster_GX5B.gz' #可修改：执白权重
    while spendTime <= 3: #可修改：设定pk上限时间
        t0 = datetime.datetime.now()
        blackW = 0
        whiteW = 0
        for i in range(100): #可修改：每一轮测试的对局数
            try:
                whoWin = startPK(i,weightb,weightw,spendTime)
            except KeyboardInterrupt:
                break
            if whoWin == 'b':
                blackW += 1
            elif whoWin == 'w':
                whiteW += 1
            elif whoWin == 'x':
                print 'Too many moves Found:', whoWin
            else:
                print 'Error Found:', whoWin
            print weightb+' B vs '+weightw+' W'+str(spendTime)+'s', blackW,':', whiteW
            
            #每一局结束保存临时结果到~autopk_temp.txt文件中,防止意外退出
            t1 = datetime.datetime.now()
            tempfile = open('~autopk_temp.txt','w')
            tempfile.write('From:'+t0.strftime('%b-%d-%y %H:%M:%S')+' to '+ \
                          t1.strftime('%b-%d-%y %H:%M:%S')+ \
                          '. Spend '+str((t1-t0).total_seconds())+'s\n')
            tempfile.write(weightb+' B vs '+weightw+' W'+str(spendTime)+'s '+str(blackW)+":"+str(whiteW)+'\n')
            tempfile.close()
            
        t1 = datetime.datetime.now()
        resfile = open('PKResult.txt','a')
        resfile.write('From:'+t0.strftime('%b-%d-%y %H:%M:%S')+' to '+ \
                      t1.strftime('%b-%d-%y %H:%M:%S')+ \
                      '. Spend '+str((t1-t0).total_seconds())+'s\n')
        resfile.write(weightb+' B-nextEngine vs '+weightw+' W-1130Engine'+str(spendTime)+'s '+str(blackW)+":"+str(whiteW)+'\n')
        #resfile.write(weightb+' B-t2 vs '+weightw+' W-t4 '+str(blackW)+":"+str(whiteW)+'\n')
        resfile.close()
        spendTime = spendTime*2 #可修改：设定每一轮pk时间的增量
        #引擎及引擎参数的修改要到201行和242行，注意行数可能随着程序被修改而变化，搜索pbscmd、pwscmd变量比较准确
