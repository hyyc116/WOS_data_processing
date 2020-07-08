#coding:utf-8
'''
对wos数据库中的数据进行一系列的基本处理，以便于其他项目使用。

包括：
    
    ---基础数据

    每篇论文的年份: pid_pubyear.json
    
    每篇论文每年的被引次数： pid_year_citnum.json

    每篇论文对应的作者数量： pid_authornum.json
    
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

def fetch_subjects():
    pid_subjects = defaultdict(list)
    ## query database wos_summary
    query_op = dbop()
    num_with_subject = 0
    sql = 'select id,subject from wos_core.wos_subjects'
    progress=0
    for pid,subject in query_op.query_database(sql):
        progress+=1
        if progress%1000000==0:
            logging.info('progress {:}, {:} papers within subjects ...'.format(progress,num_with_subject))

        # if subject.strip().lower() in subjects:
        #     num_with_subject+=1
        pid_subjects[pid].append(subject)

    query_op.close_db()
    logging.info('{:}  papers have subject'.format(len(pid_subjects.keys())))
    open('data/pid_subjects.json','w').write(json.dumps(pid_subjects))

    ##加载所有论文的subject对应的最高级的subject
    logging.info('loading mapping relations to top subject ...')
    top_subject = None
    subject_2_top = {}

    for line in open('subjects.txt'):

        line = line.strip()

        if line=='' or line is None:
            continue

        if line.startswith('====='):

            top_subject = line[5:]
        else:
            subject_2_top[line.lower()] = top_subject

            if ',' in line.lower():

                for subj in line.split(','):

                    subject_2_top[subj.lower()] = top_subject
            if '&' in line.lower():

                subject_2_top[line.replace('&','')] = top_subject

    logging.info('%d subjects are loaded ..' % len(subject_2_top.keys()))

    ## 所有论文的顶级subject
    logging.info('paper top subjs ....')
    nums_top_subjs  = []
    _ids_top_subjs = {}
    progress = 0
    error_subjs = []

    topsubj_num = defaultdict(int)
    for _id in pid_subjects.keys():

        progress+=1

        if progress%1000000==0:

            logging.info('progress %d/%d ...' %(progress,total_paper_num))

        top_subjs = []
        for subj in pid_subjects[_id]:

            top_subj = subject_2_top.get(subj.strip().lower(),None)

            if top_subj is None:
                error_subjs.append(subj)
                logging.info('error subj %s' % subj)
            else:
                top_subjs.append(top_subj)

                topsubj_num[top_subj]+=1


        top_subjs = list(set(top_subjs))

        nums_top_subjs.append(len(top_subjs))

        _ids_top_subjs[_id] = top_subjs
    open('data/missing_subjects.txt','w').write('\n'.join(list(set(error_subjs))))

    open('data/pid_topsubjs.json','w').write(json.dumps(_ids_top_subjs))
    logging.info('pid_topsubjs.json saved')

def fetch_pubyear():
    pid_pubyear = {}
    ## query database wos_summary
    query_op = dbop()
    sql = 'select id,pubyear from wos_core.wos_summary'
    progress=0
    for pid,pubyear in query_op.query_database(sql):
        progress+=1
        if progress%1000000==0:
            logging.info('progress {:} ...'.format(progress))

        pid_pubyear[pid] = pubyear

    query_op.close_db()
    logging.info('{:} cited ids have year'.format(len(pid_pubyear.keys())))

    open('data/pid_pubyear.json','w').write(json.dumps(pid_pubyear))

def fetch_doctype():
    pid_doctype = {}
    ## query database wos_summary
    query_op = dbop()
    sql = 'select id,doctype from wos_core.wos_doctypes'
    progress=0
    for pid,doctype in query_op.query_database(sql):
        progress+=1
        if progress%1000000==0:
            logging.info('progress {:} ...'.format(progress))

        pid_doctype[pid] = doctype

    query_op.close_db()
    saved_path = 'data/pid_doctype.json'
    open(saved_path,'w').write(json.dumps(pid_doctype))


def get_paper_teamsize():

    sql = 'select id,name_id,addr_id from wos_core.wos_address_names'

    pid_names = defaultdict(set)

    query_op = dbop()
    progress = 0
    for _id,name_id,addr_id in query_op.query_database(sql):
        progress+=1

        if progress%1000000==0:
            logging.info('progress {} ...'.format(progress))

        pid_names[_id].add(name_id)

        pid_ts = {}
        for pid in pid_names:

            pid_ts[pid] = len(pid_names)

    open('data/pid_teamsize.json','w').write(json.dumps(pid_ts))
    logging.info('{} data saved to data/pid_teamsize.json'.format(len(pid_ts)))



def stat_basic_num():

    logging.info('loading paper pubyear ...')
    pid_pubyear = json.loads(open('data/pid_pubyear.json').read())
    logging.info('{} papers has year label.'.format(len(pid_pubyear.keys())))

    logging.info('loading paper subjects ...')
    pid_subjects = json.loads(open('data/pid_subjects.json').read())
    logging.info('{} papers has year label.'.format(len(pid_subjects.keys())))

    logging.info('loading paper top subjects ...')
    pid_topsubjs = json.loads(open('data/pid_topsubjs.json').read())
    logging.info('{} papers has year label.'.format(len(pid_topsubjs.keys())))

    logging.info('loading paper teamsize ...')
    pid_teamsize = json.loads(open('data/pid_teamsize.json').read())
    logging.info('{} papers has year label.'.format(len(pid_teamsize.keys())))

    interset = set(pid_pubyear.keys())&set(pid_teamsize.keys())&set(pid_topsubjs.keys())&set(pid_topsubjs.keys())

    logging.info('{} papers has both four attrs.'.format(len(interset)))



if __name__ == '__main__':
    stat_basic_num()

