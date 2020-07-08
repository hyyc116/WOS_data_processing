#coding:utf-8
'''
对wos数据库中的数据进行一系列的基本处理，以便于其他项目使用。

包括：
    
    ---基础数据

    每篇论文的年份: paper_pubyear.json
    
    每篇论文每年的被引次数： paper_year_citnum.json

    每篇论文对应的作者数量： paper_authornum.json
    
    --- subject相关

    每篇论文对应的subjects: paper_subjects.json paper_topsubjects.json
    
    --- 用于计算学科之间的相似度
    topsubject以及subject的参考文献数量，以及相互之间的引用数量： subj_refnum.json subj_subj_refnum.json  topsubj_refnum.json topsubj_topsubj_refnum.json

    每个学科非本地引用的数量： subj_outrefnum.json

    ---统计数据
    论文总数量，引用关系总数量，及在六个学科中的总数量

    随着时间论文总数量的变化以及六个顶级学科的论文数量变化
    
    六个顶级学科相互之间的引用矩阵

    六个学科的引用次数分布 CCDF以及使用powlaw进行拟合的系数

'''

def stat_data_from_pid_cits():

    pass


