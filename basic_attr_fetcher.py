#coding:utf-8

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


def fetch_teamsize():

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
        pid_ts[pid] = len(pid_names[pid])

    open('data/pid_teamsize.json','w').write(json.dumps(pid_ts))
    logging.info('{} data saved to data/pid_teamsize.json'.format(len(pid_ts)))

if __name__ == '__main__':
    fetch_teamsize()

