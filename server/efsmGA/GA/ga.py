#encoding:UTF-8
from __future__ import division
from datetime import datetime
import initial_population
import cal_chrofitness
import selection
import crossover
import mutation
import update_population
import feasibility
import delete_repeat
import pop_diversity
import du_cover
import copy
import obtain_efsm_info
from collections import Counter


import random
popsize=10
pc=0.9
pm=0.3
ind_history=[]
history=[]
def pop_history(pop,flag):  #精英策略
    ind_flag = 0
    if flag==1:
        for ind in pop:
            for tran in ind:
                if tran not in history:
                    history.append(tran)
                    ind_flag = 1
            if ind_flag:
                ind_history.append(ind)
    elif flag==2:
        traninfolist = obtain_efsm_info.obtain_tran_info()
        for ind in pop:
            ind_flag=0
            for tran in ind:
                tran = tran.strip('T')
                index = int(tran) - int('0') - 1
                if traninfolist[index].tgt.name not in history:
                    history.append(traninfolist[index].tgt.name)
                    ind_flag=1
                if traninfolist[index].src.name not in history:
                    history.append(traninfolist[index].src.name)
                    ind_flag=1
            if ind_flag:
                ind_history.append(ind)
def GA(pop,pc,pm,popsize,flag):
    print 'parent pop:', pop
    temp = copy.deepcopy(pop)
    covlist = cal_chrofitness.pop_fitlist_cov(pop,flag)#flag=1,全歉意覆盖，=2，全状态覆盖
    selectedpop = selection.RouletteSelection(pop, flag)# 验证 select功能
    crossedpop = crossover.crossover(selectedpop, pc)# 验证crossover功能
    mutantedpop = mutation.mutantion(crossedpop, pm)# 验证mutant功能
    childpop_repeat=delete_repeat.delete_repeat_chrom(mutantedpop)
    newpop = update_population.update_deleteSim(temp,childpop_repeat,popsize)  ## 验证update功能
    print 'update result:', newpop
    list=feasibility.is_feasible_list(newpop)
    if len(list)<popsize:
        for i in range(len(list)):
            if list[i]==False:
                newpop[i]=pop[i]
    return newpop



startTime = datetime.now()   # 记录开始时间
pop=initial_population.initalpop_new(popsize)
count=0
flag=2
end_need_num=9
while 1:
    pop_history(pop,flag)
    print history
    print len(history)
    if (len(history)>=end_need_num) or (count==400):
        print '================================================'
        print 'geneneration:', count
        break
    pop = GA(pop, pc, pm, popsize, flag)
    count=count+1
endTime = datetime.now()
during=endTime - startTime
print 'endTime - startTime:\t', during
print '======================================================='
path = ''
name = 'fullState.txt'
with open(path+name, 'w') as f:
    for i in ind_history:
        print i
        f.write(str(i)+'\n')