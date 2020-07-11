#coding:utf-8

from basic_config import *

def reference_distribution():

    logging.info('loading paper subjects ...')
    pid_topsubjs = json.loads(open('data/pid_topsubjs.json').read())
    logging.info('{} papers has subject label.'.format(len(pid_topsubjs.keys())))

    pid_refs = {}

    for line in open('data/pid_refs.txt'):

        line = line.strip()
        pid_refs.update(json.loads(line))

    ## 统计每一个学科 数据集内的引用次数分布
    subj_refnum_dis = defaultdict(lambda:defaultdict(int))
    for pid in pid_refs.keys():
        for subj in pid_topsubjs[pid]:
            subj_refnum_dis[subj][len(pid_refs[pid])]+=1

    plt.figure(figsize=(6,5))
    ##将每一个学科的ref_dis画出来
    for subj in sorted(subj_refnum_dis.keys()):

        xs = []
        ys = []

        for refnum in sorted(subj_refnum_dis[subj].keys()):

            xs.append(refnum)
            ys.append(subj_refnum_dis[subj][refnum])

        ys = np.array(ys)/float(np.sum(ys))

        plt.plot(xs,ys,label=subj)


    plt.xscale('log')
    plt.xlabel('number of citations')
    plt.ylabel('percentage')

    plt.tight_layout()
    plt.savefig('fig/subj_refnum_dis.png',dpi=400)




if __name__ == '__main__':
    reference_distribution()


