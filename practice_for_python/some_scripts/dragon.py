import csv
import matplotlib.pyplot as plt
import numpy as np
DEBUG = False
class Arena():
    def __init__(self):

        def loadData(fname):
            '''
            内置函数：从文件中读取队名，胜率区间
            :param fname: filename
            :return: 队名，胜率区间
            '''
            teamsName = list()
            teamsWinRate = list()
            #打开文件
            with open(fname) as f:
                f_csv = csv.reader(f)
                headers = next(f_csv)
                #逐行读取数据
                for r in f_csv:
                    teamsName.append(r[0])
                    teamsWinRate.append(r[1:])
            return teamsName, np.array(teamsWinRate,dtype=np.float32)
        #利用上面的内置函数读取数据
        self.teamsName, self.teamsWinRange = loadData('data.csv')
        # 生成候选名单
        self.candidates = np.arange(0, 8)
        #随机匹配，相邻者比赛
        np.random.shuffle(self.candidates)

        if DEBUG:
            self.candidates = np.array([0,5,7,3,1,2,6,4])
            print(self.teamsName)
            print(self.teamsWinRange)
            print(self.candidates)

    def game(self, _teamsKillDragonRate):
        '''
        8支淘汰赛：最后一支队伍胜出
        :param teamsKillDragonRate: 每个队伍的胜率（杀龙概率）
        :return: 比赛后的队伍的胜率
        '''
        teamsKillDragonRate = _teamsKillDragonRate.copy()
        #比赛队伍数量
        n = self.candidates.shape[0]
        while(n!=1):
            #获取比赛双方胜率
            KillDragonRate = teamsKillDragonRate[self.candidates].reshape(-1, 2)
            for i in range(n//2): #晋级比赛
                for j in range(3): # 最大比赛次数
                    p1,p2 = KillDragonRate[i]
                    flag = 0 # 获胜标签
                    while(flag == 0):
                        #随机生成2个概率和2个时间
                        r1,r2,t1,t2 = np.random.random(4)
                        t1 = t1 * 60
                        t2 = t2 * 60
                        #如果时间小于10分钟重新比赛
                        if ((t1 < 10) or (t2 < 10)):
                            continue
                        #如果player1 杀死了小龙
                        if (r1 < p1):
                            flag = flag | 1 #player1 win
                        # 如果player2 杀死了小龙
                        if (r2 < p2):
                            flag = flag | 2
                    # 如果player1 player2 都杀死了小龙
                    if flag ==3 :
                        #时间短的获胜
                        if t1 < t2:
                            flag = 1
                        else:
                            flag = 2
                    #杀死小龙的队伍胜率加 5%
                    p2 += 0.05* (flag & 1) if p2 <=0.95 else 0
                    p1 += 0.05*((flag & 2)>>1) if p1 <=0.95 else 0
                    #修改胜率
                    KillDragonRate[i] =[p1, p2 ]
                    #如果双方胜率差值大于 10% 结束比赛
                    if(abs(p1-p2)>0.1):
                        break
                # 修改胜率
                idx1 = self.candidates[i * 2]
                idx2 = self.candidates[i * 2 + 1]
                teamsKillDragonRate[idx1] = p1
                teamsKillDragonRate[idx2] = p2
                # 如果player1 获胜
                if flag == 1:
                    # player1 晋级
                    self.candidates[i] = self.candidates[i * 2 + 0]
                    #如果根据杀小龙时间修改胜率
                    rate = p1 + (0.05 if t1<25 else 0.02)
                    rate = rate if rate <1 else 1
                    #尝试杀大龙
                    flag = np.random.random() < rate #结果
                    time = np.random.random() * 60   #时间
                    if flag:
                        #杀死大龙且时间在（30，40），胜率 +10%
                        if 30 < time and time <40:
                            teamsKillDragonRate[i * 2 + 0] += 0.1 if teamsKillDragonRate[i * 2 + 0] < 0.9 else 0
                # 如果player2 获胜
                else:
                    # player2 晋级
                    self.candidates[i] = self.candidates[i * 2 + 1]
                    # 如果根据杀小龙时间修改胜率
                    rate = p2 + (0.05 if t2<25 else 0.02)
                    rate = rate if rate < 1 else 1
                    # 尝试杀大龙
                    flag = np.random.random() < rate#结果
                    time = np.random.random() * 60  #时间
                    if flag:
                        # 杀死大龙且时间在（30，40），胜率 +10%
                        if 30 < time and time <40:
                            teamsKillDragonRate[i * 2 + 1] += 0.1 if teamsKillDragonRate[i * 2 + 1] < 0.9 else 0
            #晋级名单
            self.candidates = self.candidates[: n//2]
            #随机匹配
            np.random.shuffle(self.candidates)
            #输出
            print("Promotion List")
            for no, prob in zip(self.candidates, teamsKillDragonRate[self.candidates]):
                print('%d %s rate = %.2f'%(no,self.teamsName[no],prob))
            n = self.candidates.shape[0]
        return teamsKillDragonRate



if __name__ == '__main__':
    #实例化 Arena 类
    a = Arena()
    #根据胜率范围随机产生各个队伍胜率
    teamsKillDragonRate = (a.teamsWinRange[:,0] + np.random.random(8) * (a.teamsWinRange[:,1] - a.teamsWinRange[:,0])) / 100.
    #根据胜率开始比赛
    teamsKillDragonRate_new = a.game(teamsKillDragonRate)
    #前后胜率集合
    plt_data = np.stack([teamsKillDragonRate,teamsKillDragonRate_new])
    #画图
    axis_x = np.arange(8)
    plt.bar(left=axis_x, height=teamsKillDragonRate,facecolor='#9999ff', edgecolor='white')
    plt.bar(left=axis_x, height=-teamsKillDragonRate_new,facecolor='#ff9999', edgecolor='white')
    for x, y in zip(axis_x, teamsKillDragonRate):
        # ha: horizontal alignment
        # va: vertical alignment
        plt.text(x , y + 0.05, '%.2f' % y, ha='center', va='bottom')
    for x, y in zip(axis_x, teamsKillDragonRate_new):
        # ha: horizontal alignment
        # va: vertical alignment
        plt.text(x , -y - 0.05, '%.2f' % y, ha='center', va='top')
    plt.show()