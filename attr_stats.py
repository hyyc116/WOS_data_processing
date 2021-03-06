#coding:utf-8

from basic_config import *

from WOS_data_processing import load_basic_data

import seaborn as sns


def citation_distribution():

    logging.info('loading attrs ...')
    pid_pubyear, pid_subjects, pid_topsubjs, pid_teamsize = load_basic_data()

    logging.info('loading pid cn ...')
    pid_cn = json.loads(open('data/pid_cn.json').read())

    logging.info('{} paper citations loaded.'.format(len(pid_cn.keys())))

    subj_cit_dis = defaultdict(lambda: defaultdict(int))

    subj_year_cits = defaultdict(lambda: defaultdict(list))

    for pid in pid_cn.keys():

        pubyear = int(pid_pubyear[pid])

        cn = pid_cn[pid]

        for subj in pid_topsubjs[pid]:

            subj_cit_dis[subj][cn] += 1
            subj_year_cits[subj][pubyear].append(cn)

    ##画出各个学科的ccdf分布

    plt.figure(figsize=(5.5, 4))
    for subj in sorted(subj_cit_dis.keys()):

        xs = []
        ys = []
        for cit in sorted(subj_cit_dis[subj].keys()):
            xs.append(cit)
            ys.append(subj_cit_dis[subj][cit])

        ys = [np.sum(ys[i:]) / float(np.sum(ys)) for i in range(len(ys))]

        plt.plot(xs, ys, label=subj)

    plt.xlabel('number of citations')

    plt.ylabel('percentage')

    plt.xscale('log')

    plt.yscale('log')

    plt.legend()

    plt.tight_layout()

    plt.savefig('fig/subj_cit_dis.png', dpi=400)
    logging.info('fig saved to fig/subj_cit_dis.png.')

    ### 画出各学科平均引用次数随时间的变化

    plt.figure(figsize=(5.5, 4))

    for subj in sorted(subj_year_cits.keys()):

        xs = []
        ys = []

        for year in sorted(subj_year_cits[subj].keys()):

            avgC = np.mean(subj_year_cits[subj][year])

            xs.append(year)
            ys.append(avgC)

        plt.plot(xs, ys, label=subj)

    plt.plot([2004] * 10, np.linspace(1, 42, 10), '--', label='$x=2004$')

    plt.xlabel('year')

    plt.ylabel('average number of citations')

    plt.legend()
    # plt.yscale('l)

    plt.tight_layout()

    plt.savefig('fig/subj_year_averagecn.png', dpi=400)

    logging.info('fig saved to fig/subj_year_averagecn.png.')


def reference_distribution():

    logging.info('loading paper subjects ...')
    pid_topsubjs = json.loads(open('data/pid_topsubjs.json').read())
    logging.info('{} papers has subject label.'.format(len(
        pid_topsubjs.keys())))

    pid_refnum = json.loads(open('data/pid_refnum.json').read())

    ## 统计每一个学科 数据集内的引用次数分布
    subj_refnum_dis = defaultdict(lambda: defaultdict(int))
    for pid in pid_refnum.keys():

        if pid_topsubjs.get(pid, None) is None:
            continue

        for subj in pid_topsubjs[pid]:
            subj_refnum_dis[subj][pid_refnum[pid]] += 1

    sns.set_theme(style='ticks')
    plt.figure(figsize=(5.5, 4))
    ##将每一个学科的ref_dis画出来
    for subj in sorted(subj_refnum_dis.keys()):

        xs = []
        ys = []

        for refnum in sorted(subj_refnum_dis[subj].keys()):

            xs.append(refnum)
            ys.append(subj_refnum_dis[subj][refnum])

        ys = np.array(ys) / float(np.sum(ys))

        plt.plot(xs, ys, label=subj)

    sns.despine()

    plt.xscale('log')
    # plt.yscale('log')

    plt.xlabel('number of references')

    plt.xlim(0.9, 200)
    # plt.ylim()
    plt.ylabel('percentage')

    plt.legend()

    plt.tight_layout()
    plt.savefig('fig/subj_all_refnum_dis.png', dpi=400)
    logging.info('fig saved to fig/subj_all_refnum_dis.png')

    pid_refs = {}

    for line in open('data/pid_refs.txt'):

        line = line.strip()
        pid_refs.update(json.loads(line))

    ## 统计每一个学科 数据集内的引用次数分布
    subj_refnum_dis = defaultdict(lambda: defaultdict(int))
    for pid in pid_refs.keys():
        for subj in pid_topsubjs[pid]:
            subj_refnum_dis[subj][len(pid_refs[pid])] += 1

    plt.figure(figsize=(5.5, 4))
    ##将每一个学科的ref_dis画出来
    for subj in sorted(subj_refnum_dis.keys()):

        xs = []
        ys = []

        for refnum in sorted(subj_refnum_dis[subj].keys()):

            xs.append(refnum)
            ys.append(subj_refnum_dis[subj][refnum])

        ys = np.array(ys) / float(np.sum(ys))

        plt.plot(xs, ys, label=subj)

    plt.xscale('log')
    # plt.yscale('log')

    plt.xlabel('number of references')

    plt.xlim(0.9, 200)
    # plt.ylim()
    plt.ylabel('percentage')

    plt.legend()

    sns.despine()

    plt.tight_layout()
    plt.savefig('fig/subj_refnum_dis.png', dpi=400)
    logging.info('fig saved to fig/subj_refnum_dis.png')


if __name__ == '__main__':
    # citation_distribution()

    reference_distribution()
