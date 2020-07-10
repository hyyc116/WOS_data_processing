#coding:utf-8
'''
对wos数据库中的数据进行一系列的基本处理，以便于其他项目使用。

包括：
    
    ---基础数据

    每篇论文的年份: pid_pubyear.json
    
    每篇论文每年的被引次数： pid_year_citnum.json

    每篇论文对应的作者数量： pid_teamsize.json
    
    --- subject相关

    每篇论文对应的subjects: pid_subjects.json pid_topsubjs.json
    
    --- 用于计算学科之间的相似度
    topsubject以及subject的参考文献数量，以及相互之间的引用数量： subj_refnum.json subj_subj_refnum.json  topsubj_refnum.json topsubj_topsubj_refnum.json

    每个学科非本地引用的数量： subj_outrefnum.json

    ---统计数据
    论文总数量，引用关系总数量，及在六个学科中的总数量

    随着时间论文总数量的变化以及六个顶级学科的论文数量变化
    
    六个顶级学科相互之间的引用矩阵

    六个学科的引用次数分布 CCDF以及使用powlaw进行拟合的系数

'''

from basic_config import *

from basic_attr_stats import *

def stat_basic_attr():
    fetch_subjects()
    fetch_pubyear()
    fetch_doctype()
    fetch_teamsize()


def load_basic_data(isStat=False):

    logging.info('======== LOADING BASIC DATA =============')
    logging.info('======== ================== =============')


    logging.info('loading paper pubyear ...')
    pid_pubyear = json.loads(open('data/pid_pubyear.json').read())
    logging.info('{} papers has year label.'.format(len(pid_pubyear.keys())))

    logging.info('loading paper subjects ...')
    pid_subjects = json.loads(open('data/pid_subjects.json').read())
    logging.info('{} papers has subject label.'.format(len(pid_subjects.keys())))

    logging.info('loading paper top subjects ...')
    pid_topsubjs = json.loads(open('data/pid_topsubjs.json').read())
    logging.info('{} papers has top subject label.'.format(len(pid_topsubjs.keys())))

    logging.info('loading paper teamsize ...')
    pid_teamsize = json.loads(open('data/pid_teamsize.json').read())
    logging.info('{} papers has teamsize label.'.format(len(pid_teamsize.keys())))

    if isStat:
        interset = set(pid_pubyear.keys())&set(pid_teamsize.keys())&set(pid_topsubjs.keys())&set(pid_topsubjs.keys())
        logging.info('{} papers has both four attrs.'.format(len(interset)))

    logging.info('======== LOADING BASIC DATA DONE =============')
    logging.info('======== ======================= =============')

    return pid_pubyear,pid_subjects,pid_topsubjs,pid_teamsize

def stats_from_pid_cits():
    
    ##基础数据统计
    pid_pubyear,pid_subjects,pid_topsubjs,pid_teamsize = load_basic_data()

    ## 学科间的相互引用
    subj_refnum = defaultdict(int)
    subj_subj_refnum = defaultdict(lambda:defaultdict(int))

    topsubj_refnum = defaultdict(int)
    topsubj_topsubj_refnum = defaultdict(lambda:defaultdict(int))

    ## 非本地引文数量
    subj_year_outrefnum = defaultdict(lambda:defaultdict(int))
    topsubj_year_outrefnum = defaultdict(lambda:defaultdict(int))

    subj_year_refnum = defaultdict(lambda:defaultdict(int))
    topsubj_year_refnum = defaultdict(lambda:defaultdict(int))

    ## 每篇论文随着时间的引用次数
    pid_year_citnum = defaultdict(lambda:defaultdict(int))

    progress = 0
    lines = []
    for line in open('data/pid_cits_ALL.txt'):

        progress+=1
        if progress%100000000==0:
            logging.info('reading %d citation relations....' % progress)

        line = line.strip()

        pid,citing_id = line.split("\t")

        cited_year = pid_pubyear.get(pid,None)

        cited_subjs = pid_subjects.get(pid,None)

        cited_topsubjs = pid_topsubjs.get(pid,None)

        citing_year = pid_pubyear.get(citing_id,None)

        citing_subjs = pid_subjects.get(citing_id,None)

        citing_topsubjs = pid_topsubjs.get(citing_id,None)

        ##如果引证文献没有数据 则略过
        if citing_year is None or citing_subjs is None or citing_topsubjs is None:
            continue

        ## 被引论文可能是不再本地数据库中的论文
        if cited_year is None or cited_subjs is None or cited_topsubjs is None:

            for subj in citing_subjs:
                subj_year_outrefnum[subj][citing_year]+=1

            for topsubj in citing_topsubjs:
                topsubj_year_outrefnum[topsubj][citing_year]+=1

            continue

        for subj in citing_subjs:
            subj_year_refnum[subj][citing_year]+=1

            subj_refnum[subj]+=1

            for cited_subj in cited_subjs:
                subj_subj_refnum[subj][cited_subj]+=1

        for topsubj in citing_topsubjs:
            topsubj_year_refnum[topsubj][citing_year]+=1

            topsubj_refnum[topsubj]+=1

            for cited_topsubj in cited_topsubjs:
                topsubj_topsubj_refnum[topsubj][cited_topsubj]+=1

        pid_year_citnum[pid][citing_year]+=1

    open("data/pid_year_citnum.json",'w').write(json.dumps(pid_year_citnum))
    logging.info('data saved to data/pid_year_citnum.json')

    open("data/subj_refnum.json",'w').write(json.dumps(subj_refnum))
    logging.info('data saved to data/subj_refnum.json')

    open("data/subj_year_refnum.json",'w').write(json.dumps(subj_year_refnum))
    logging.info('data saved to data/subj_year_refnum.json')

    open("data/subj_year_outrefnum.json",'w').write(json.dumps(subj_year_outrefnum))
    logging.info('data saved to data/subj_year_outrefnum.json')

    open("data/topsubj_refnum.json",'w').write(json.dumps(topsubj_refnum))
    logging.info('data saved to data/topsubj_refnum.json')

    open("data/topsubj_year_refnum.json",'w').write(json.dumps(topsubj_year_refnum))
    logging.info('data saved to data/topsubj_year_refnum.json')

    open("data/topsubj_year_outrefnum.json",'w').write(json.dumps(topsubj_year_outrefnum))
    logging.info('data saved to data/topsubj_year_outrefnum.json')

    open("data/subj_subj_refnum.json",'w').write(json.dumps(subj_subj_refnum))
    logging.info('data saved to data/subj_subj_refnum.json')

    open("data/topsubj_topsubj_refnum.json",'w').write(json.dumps(topsubj_topsubj_refnum))
    logging.info('data saved to data/topsubj_topsubj_refnum.json')


##对一些数据进行统计和可视化
def stat_and_visualize_data():

    ## 各领域的论文数量及随时间的变化曲线
    pid_pubyear,pid_subjects,pid_topsubjs,pid_teamsize = load_basic_data()

    subj_year_num = defaultdict(lambda:defaultdict(int))

    subj_totalnum = defaultdict(int)

    years = set([])
    allsubjs = set([])

    for pid in pid_pubyear:

        subjs = pid_topsubjs.get(pid,None)

        pubyear = pid_pubyear[pid]

        years.add(pubyear)

        if subjs is None:
            continue

        for subj in subjs:

            allsubjs.add(subj)

            subj_year_num[subj][pubyear]+=1

            subj_totalnum[subj]+=1

    tableLines = ['|year|{}|'.format('|'.join(sorted(list(allsubjs))))]
    tableLines.append('|:---:|{}|'.format('|'.join([':---:']*len(allsubjs))))

    for year in sorted(years,key=lambda x:int(x)):
        line = []
        line.append(year)
        for subj in sorted(subj_year_num.keys()):

            line.append('{:,}'.format(subj_year_num[subj][year]))

        tableLines.append('|{}|'.format('|'.join(line)))

    totalline = ['total']

    for subj in sorted(subj_totalnum.keys()):
        totalline.append('{:,}'.format(subj_totalnum[subj]))

    tableLines.append('|{}|'.format('|'.join(totalline)))


    open("subj_paper_num.md",'w').write('\n'.join(tableLines))

    logging.info('paper num saved to subj_paper_num.md')


    plt.figure(figsize=(7,5))

    for subj in sorted(subj_year_num.keys()):

        year_num = subj_year_num[subj]

        xs = []
        ys = []

        for year in sorted(year_num.keys(),key=lambda x:int(x)):

            xs.append(int(year))
            ys.append(year_num[year])

        plt.plot(xs,ys,label=subj)


    plt.yscale('log')

    plt.xlabel('year')

    plt.ylabel('number of publications')

    plt.tight_layout()

    plt.savefig('fig/subj_year_num.png',dpi=400)

    logging.info('fig saved to fig/subj_year_num.png.')


def subj_sim_cal(data_path,out_path):

    subj_subj_refnum = json.loads(open(data_path).read())

    subj_refT = defaultdict(int)
    subj_citT = defaultdict(int) 

    for subj in subj_subj_refnum.keys():

        for cited_subj in subj_subj_refnum[subj].keys():

            refnum = subj_subj_refnum[subj][cited_subj]

            subj_refT[subj]+=refnum
            subj_citT[cited_subj]+=refnum

    subjs = subj_refT.keys()

    print(subjs)

    subj_subj_sim = defaultdict(dict)

    for i in range(len(subjs)):
        subj1 = subjs[i]
        for j in range(len(subjs)):

            subj2 = subjs[j]

            R_ij = subj_subj_refnum[subj1].get(subj2,0)
            R_ji = subj_subj_refnum[subj2].get(subj1,0)

            TR_i = subj_refT[subj1]
            TR_j = subj_refT[subj2]

            TC_i = subj_citT[subj1]
            TC_j = subj_citT[subj2]

            sim = (R_ji+R_ij)/(np.sqrt((TC_i+TR_i)*(TC_j+TR_j)))

            subj_subj_sim[subj1][subj2] = sim

    open(out_path,'w').write(json.dumps(subj_subj_sim))

    logging.info('data saved to {}.'.format(out_path))


def plot_subj_sim_matrix():

    subj_subj_sim = json.loads(open('data/subj_subj_sim.json').read())

    tableLines = []
    header = '|subj|{}|'.format('|'.join(subj_subj_sim.keys()))
    header2 = '|:---:|{}|'.format('|'.join([':---:']*len(subj_subj_sim.keys())))

    tableLines.append(header)
    tableLines.append(header2)

    for subj1 in sorted(subj_subj_sim.keys()):

        line = [subj1]
        for subj2 in sorted(subj_subj_sim.keys()):
            line.append(str(subj_subj_sim[subj1][subj2]))

        tableLines.append('|{}|'.format('|'.join(line)))


    open('sim_matrix.md','w').write('\n'.join(tableLines))

    logging.info('data saved to sim_matrix.md')





if __name__ == '__main__':
    # stat_basic_num()

    # stats_from_pid_cits()

    # stat_and_visualize_data()

    # subj_sim_cal('data/subj_subj_refnum.json','data/subj_subj_sim.json')
    # subj_sim_cal('data/topsubj_topsubj_refnum.json','data/topsubj_topsubj_sim.json')

    plot_subj_sim_matrix()



