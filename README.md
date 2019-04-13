# Curves
![Screen-shot of 40b-elo-playouts Curves](https://github.com/guitanj/AutoPK/blob/master/curves/40b-elo-playoutsCurve-updateTo220-192.jpg "Screen-shot of 40b-elo-playouts Curves")
![Screen-shot of 15b-elo-playouts Curves](https://github.com/guitanj/AutoPK/blob/master/curves/15b-elo-playoutsCurve-update157-990.jpg "Screen-shot of 15b-elo-playouts Curves")
![权重playouts值对应elo分对照表-基于各自100局对战测试（设定ELFV0 2po为2000）](https://github.com/guitanj/AutoPK/blob/master/elo/playoutsVSEloList-update220-192.jpg "playouts vs elo list")

# AutoPK
Try to draw the elo-playouts curve of those leelazero networks.

Based on the elfv0, auto self-fight with the gradual growth of playouts(100 games per fight), 10 vs 2,50 vs 10,100 vs 50 and so on...now max 25600 vs 12800, Define elfv0 2 playouts with 2000 elo, generate baseline elo data.

then use other weights to fight with elfv0 with same playouts(100 games per fight),use the winning percentage to calculate Elo values of the corresponding playouts, Eventually draw the elo-playouts curve.

这个程序的目标是画leelaZero权重的棋力曲线(elo-playouts)。

以ELFV0为基础，使用其逐步增长的playouts自动自我对战（每轮对战100局），根据胜率计算出对应playouts的elo值，进一步画出棋力曲线来。

然后用其他权重同po对战ELFV0（每轮对战100局），用胜率计算出对应的elo值，画出测试权重的棋力曲线。以ELFV0权重2po为2000elo值。

# Advantage
Automatically save versus, and to save the winrate/playouts of every step.

Same playouts pk:save score, time spending.

Same time pk:save the average playouts.

Parameter adjustment of freedom, the engine can also be freely adjusted.

Going to Python programming, you can change the program whatever you like.

自动保存对战棋谱，并且保存每一步的胜率、playouts情况

保存对战比分、对战时长，同时间对战保存平均playouts数据

参数自由调整，引擎也可以自由调整

# To do list
GUI interface, animate the progress while fighting

Versus breakpoints saved and restored

图形配置界面，动态显示下棋对战进展

对战断点保存以及恢复

# Requirements
This program requires python2.X(with gomill) or python3.X(with sgfmill) environment, thanks to Matthew woodcraft's gomill & sgfmill module, also thanks to goreviewpartner project,I am learning a lot of knowledge.

本程序需要python2.x(with gomill) or python3.X(with sgfmill)环境，感谢Matthew Woodcraft的gomill & sgfmill模块。同时感谢goreviewpartner项目，我一直从中学习了许多知识。

# How to use
Modify the program, mainly the last paragraph.I noted some detailed description. 

Attention:Path to the engine and weights needs to be modified.

Results are automatically saved in PKResult.txt（for same playouts） or PKResult-ST.txt（for same time） file.

Program with same playouts:autoPK.py for python 3.X

Program with same time:autoPK-SameTime.py for python 3.X

生成的对战结果会自动保存在PKResult.txt（同po）或者PKResult-ST.txt(同时间)文件中

同playouts的对战程序为：autoPK.py for python 3.X

同时间的对战程序为：autoPK-SameTime.py for python 3.X

See " # " note to modify config.ini（for same playouts） or config-ST.ini(for same time)

参见“#”注释，修改config.ini（同po） 或者 config-ST.ini(同时间)
