import os
os.environ["KMP_DUPLICATE_LIB_OK"]  =  "TRUE"
import pandas as pd
import numpy as np 
import Cal_Resilience_fun as CRF
import multiprocessing
import warnings
warnings.filterwarnings("ignore")
# import construct_networkx_fun as cnf
# import networkx as nx
# mmbsG=cnf.creat_networkx()
# # 
# nodes=nx.get_node_attributes(mmbsG,'name')
# nodes=pd.DataFrame(nodes.items())
nodes=pd.read_csv('networkx for BRTN.csv',encoding='gbk')
nodes.columns=[0,1]
import datetime

# def resilience_assess(object):
#     # ICD node
#     node_i=object.node_i
#     ftime=object.ftime
#     tbpath = object.tbpath
#     xypath8 = object.xypath8
#     nodes=object.nodes
#     wi=object.wi
#     newod=object.newod
#     Q0=object.Q0
def resilience_assess(newod,xypath8,node_i,ftime,tbpath,nodes,wi,num_i,Q0):
    try:
        # 1.1 ICD node Qr
        aff_path, upt = CRF.disturbance_path.ICD_node_aff_path(node_i, ftime, tbpath, xypath8, nodes, wi, newod)
        # 1.2  ICD node
        tv = upt
        Qv = CRF.cal_Q.calculate_Q1(wi, aff_path, newod)
        tr = 1.5 * tv
        expR_ICD = CRF.fun_R.cal_exp_R(Q0, Qv, tv, tr)
        cosR_ICD = CRF.fun_R.cal_cos_R(Q0, Qv, tv, tr)
        # %%%%%%%%% 2 %%%%%%%%%%%%%
        # FOD node
        aff_path1, upt1 = CRF.disturbance_path.FOD_node_aff_path(node_i, tbpath, xypath8, nodes, wi, newod)
        tv1 = upt1
        Qv1 = CRF.cal_Q.calculate_Q1(wi, aff_path1, newod)
        tr1 = 1.5 * tv1
        expR_FOD = CRF.fun_R.cal_exp_R(Q0, Qv1, tv1, tr1)
        cosR_FOD = CRF.fun_R.cal_cos_R(Q0, Qv1, tv1, tr1)
        # print([object.num_i,node_i])
        filename = 'node_resilence' + '\\' + node_i + '.txt'
        f = open(filename, 'w+')
        f.write(str([node_i,expR_ICD,cosR_ICD,expR_FOD,cosR_FOD]))
        f.close()
        return node_i,expR_ICD,cosR_ICD,expR_FOD,cosR_FOD
    except:
        print('erro')
        return -1
class A:
    def __init__(self,newod,xypath8,node_i,ftime,tbpath,nodes,wi,num_i,Q0):
        self.newod=newod
        self.xypath8=xypath8
        self.node_i=node_i
        self.ftime=ftime
        self.tbpath=tbpath
        self.nodes= nodes
        self.wi = wi
        self.num_i=num_i
        self.Q0=Q0
if __name__=='__main__':
    # pool = multiprocessing.Pool(processes=2)
    # 
    newod=pd.read_csv('bus-metro_flow.csv',encoding='gbk')
    xypath8=pd.read_feather('ETP in BRTNs(final).feather')
    # 
    wi=pd.read_csv('importance of each station.csv',encoding='gbk')
    print(sum(np.array(wi['com_im'])))
    # 
    subs=pd.read_csv('subnetwork_classification.csv',encoding='gbk')
    #
    tbpath=pd.read_csv('ETPs in taxi and sharing bikes.csv',encoding='gbk')

    Q0 = CRF.cal_Q.calculate_Q(wi, xypath8, newod)
    
    # params = []
    file_dir = "node_resilence\\"
    files = os.listdir(file_dir)
    df = pd.DataFrame(files)
    df = pd.DataFrame(files)
    df['name'] = df[0].str.replace('.txt', '')
    yy = list(df['name'])



    sts=list(set(list(newod['org'])))
    for i in sts:
        # newod,xypath8,node_i,ftime,tbpath,nodes,wi):
        node_i=i
        ftime = 100000000
        num_i=sts.index(i)
        if i not in yy and num_i<1000:
            resilience_assess(newod, xypath8, node_i, ftime, tbpath, nodes, wi, num_i, Q0)
        print(num_i)
        # params.append(A(newod,xypath8,node_i,ftime,tbpath,nodes,wi,num_i,Q0))
    #assess_nodes = pool.map(resilience_assess, params)
    '''
    # ICD subs
    failuer_nodes=subs[(subs['label']==0)&(subs['modularity_class']==0)]['station'].to_list()  
    failuer_nodes_ind=subs[(subs['label']==0)&(subs['modularity_class']==0)]['index'].to_list() # 
    ftime=10000000000
    aff_path,upt=CRF.disturbance_path.ICD_subs_aff_path(failuer_nodes,failuer_nodes_ind,ftime,tbpath,xypath8,wi,newod)
    '''

    '''
    # FOD subs
    failuer_nodes=subs[(subs['label']==0)&(subs['modularity_class']==0)]['station'].to_list()  # 
    failuer_nodes_ind=subs[(subs['label']==0)&(subs['modularity_class']==0)]['index'].to_list() # 
    aff_path,upt=CRF.disturbance_path.FOD_subs_aff_path(failuer_nodes,failuer_nodes_ind,tbpath,xypath8,wi,newod)
    '''