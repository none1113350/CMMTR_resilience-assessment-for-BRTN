import os
os.environ["KMP_DUPLICATE_LIB_OK"]  =  "TRUE"
import pandas as pd
import numpy as np 
import copy
from scipy import integrate


class cal_Q():
    def calculate_Q(wi,xypath8,newod):
       
        # logit
        newod=newod.reset_index()
        xypath9=xypath8.merge(newod,on=['org','dst'],how='inner')
        xypath9['etime']=np.exp(-np.array(xypath9['time']))
        xy1=xypath9.groupby(['org','dst']).sum('etime')
        xy2=xy1.reset_index()
        xy2=xy2.rename(columns={'etime':'setime'})
        xy2=xy2[['org','dst','setime']]
        xy3=xypath9.merge(xy2,on=['org','dst'],how='inner')
        xy3=xy3.fillna(0)
        xy3['pr']=np.array(xy3['etime'])/np.array(xy3['setime'])
        xy3=xy3.fillna(0)
        xy3['pflow']=np.array(xy3['pr'])*np.array(xy3['flow'])
        cols=['org','dst','path','time','index','flow','pr','pflow']
        xypath9=xy3[cols]
        # 
        # w_ij
        # org
        wi1=copy.deepcopy(wi)
        wi1=wi1.rename(columns={'station':'org','com_im':'im_i'})
        wi1=wi1[['org','im_i']]
        xypath10=xypath9.merge(wi1,on=['org'],how='inner')
        # print(xypath10.shape)
        # dst
        wi2=copy.deepcopy(wi)
        wi2=wi2.rename(columns={'station':'dst','com_im':'im_j'})
        wi2=wi2[['dst','im_j']]
        xypath11=xypath10.merge(wi2,on=['dst'],how='inner')
        # print(xypath11.shape)
        xypath11.head(1)
        # 
        xypath11['Qijk']=(np.sqrt(np.array(xypath11['im_i'])*np.array(xypath11['im_j']))
                      *np.array(xypath11['flow'])*np.array(xypath11['pr']))/np.array(xypath11['time'])
        # 
        # print('nan检验：{}'.format(xypath11[xypath11['Qijk'].isna()].shape[0]))
        if 'index' in list(newod.columns):
            newod=newod.drop(columns='index')
        newod=newod.reset_index()
        xypath12=xypath11[['org','dst','Qijk']]
        xypath13=xypath12.merge(newod,on=['org','dst'],how='inner')
        xypath13.head(1)
        ## 计算Qij
        new1=xypath13.groupby(['org','dst']).sum('Qijk').reset_index()
        new2=newod.merge(new1,on=['org','dst'],how='inner')
        # print(new2.shape[0]==newod.shape[0])
        ## 
        new3=new2.groupby(['org']).sum('Qijk').reset_index()
        #
        Q0=(1/new3.shape[0]*(new3.shape[0]-1))*sum(np.array(new3['Qijk']))
        return Q0
    # 迭代Q1
    def calculate_Q1(wi,xypath8,newod):

        # logit
        newod=newod.reset_index()
        xypath9=xypath8.merge(newod,on=['org','dst'],how='inner')
        xypath9['etime']=np.exp(-np.array(xypath9['time']))
        xy1=xypath9.groupby(['org','dst']).sum('etime')
        xy2=xy1.reset_index()
        xy2=xy2.rename(columns={'etime':'setime'})
        xy2=xy2[['org','dst','setime']]
        xy3=xypath9.merge(xy2,on=['org','dst'],how='inner')
        xy3=xy3.fillna(0)
        xy3['pr']=np.array(xy3['etime'])/np.array(xy3['setime'])
        xy3=xy3.fillna(0)
        xy3['pflow']=np.array(xy3['pr'])*np.array(xy3['flow'])
        xy3=xy3[xy3['bool']==1]
        # print(['%%',xy3.shape])
        cols=['org','dst','path','time','index','flow','pr','pflow']
        xypath9=xy3[cols]
        # print(['%%_sum',sum(xy3['pflow'])])
        # 
        # 计算w_ij
        # org
        wi1=copy.deepcopy(wi)
        wi1=wi1.rename(columns={'station':'org','com_im':'im_i'})
        wi1=wi1[['org','im_i']]
        xypath10=xypath9.merge(wi1,on=['org'],how='inner')
        print(xypath10.shape)
        # dst
        wi2=copy.deepcopy(wi)
        wi2=wi2.rename(columns={'station':'dst','com_im':'im_j'})
        wi2=wi2[['dst','im_j']]
        xypath11=xypath10.merge(wi2,on=['dst'],how='inner')
        # print(xypath11.shape)
        xypath11.head(1)
        # 计算Q值内层
        xypath11['Qijk']=(np.sqrt(np.array(xypath11['im_i'])*np.array(xypath11['im_j']))
                      *np.array(xypath11['flow'])*np.array(xypath11['pr']))/np.array(xypath11['time'])
        # 检验是否出现nan
        # print('nan检验：{}'.format(xypath11[xypath11['Qijk'].isna()].shape[0]))
        if 'index' in list(newod.columns):
            newod=newod.drop(columns='index')
        newod=newod.reset_index()
        xypath12=xypath11[['org','dst','Qijk']]
        xypath13=xypath12.merge(newod,on=['org','dst'],how='inner')
        xypath13.head(1)
        ## 计算Qij
        new1=xypath13.groupby(['org','dst']).sum('Qijk').reset_index()
        new2=newod.merge(new1,on=['org','dst'],how='inner')
        # print(new2.shape[0]==newod.shape[0])
        ## 计算Qi
        new3=new2.groupby(['org']).sum('Qijk').reset_index()
        # 计算Q_0
        Q0=(1/new3.shape[0]*(new3.shape[0]-1))*sum(np.array(new3['Qijk']))
        return Q0
class disturbance_path():
    # 
    def ICD_node_aff_path(node_i,ftime,tbpath,xypath8,nodes,wi,newod):

        id_dafnode=nodes[nodes[1]==node_i][0].to_list()[0]
        dafnode=node_i 
        nwi=wi[wi['station']==dafnode]['com_im'].to_list()[0]*100 # NI计算值
        upt=max(xypath8[xypath8['org']==dafnode].groupby(['org','dst']).min('time')['time'].to_list())*nwi #
       
        affect_nodes=xypath8[(xypath8['org']==dafnode)&(xypath8['time']<=upt)]['dst'].to_list()
        #
        ods1=newod[newod['org']==dafnode][['org','dst']]  
        ods2=newod[newod['dst']==dafnode][['org','dst']]  
        xy=copy.deepcopy(xypath8)
        xy['path1']=xy['path'].apply(lambda x:str(x))
        xyp9=pd.concat([xy, xy['path1'].str.replace('[','').str.replace(']','').str.split(' ', expand=True)], axis=1)
        cols1=xyp9.columns
        xyp10=xyp9[cols1[6::]]
        arp=xyp10.values
        xyp9=xyp9.reset_index()
        dfw=pd.DataFrame(np.argwhere(arp==str(id_dafnode)))
        dfw.columns=['index','index1']
        dfw=dfw[['index']]
        ods3=xyp9.merge(dfw,on='index',how='inner')[['org','dst']]
       
        od1=pd.DataFrame(affect_nodes,columns=['org'])
        ods4=newod.merge(od1,on='org',how='inner')[['org','dst']]
     
        odall=pd.DataFrame()
        odall=pd.concat([odall,ods1])
        odall=pd.concat([odall,ods2])
        odall=pd.concat([odall,ods3])
        odall=pd.concat([odall,ods4])

        axyp=odall.merge(xypath8,on=['org','dst'],how='inner')
        #2.1 
        axyp1=copy.deepcopy(axyp)
        axyp1['ntime']=np.array(axyp['time'])+ftime
        #2.2 
        axyp2=copy.deepcopy(axyp)
        axyp2['path1']=axyp2['path'].apply(lambda x:str(x))
        ap1=pd.concat([axyp2, axyp2['path1'].str.replace('[','').str.replace(']','').str.split(' ', expand=True)], axis=1)
        cols1=ap1.columns
        apa=ap1[cols1[6::]].values
        dfapa=pd.DataFrame(np.argwhere(apa==str(id_dafnode)))
        dfapa.columns=['index','index1']
        axyp2=axyp2.reset_index()
        axyp3=axyp2.merge(dfapa,on='index',how='outer')
        axyp3.head()
        axyp3=axyp3.fillna(-1)
        axyp2=axyp3[axyp3['index1']==-1][['org','dst','path','time']]
        # 2.3 
        axypp=tbpath.merge(odall,on=['org','dst'],how='inner')
        axyp3=axypp[['org','dst','path','bike_time']]
        axyp4=axypp[['org','dst','path','taxi_time']]
        # 2.4 
        axyp1=axyp1[['org','dst','path','ntime']]
        axyp1=axyp1.rename(columns={'ntime':'time'})
        axyp1['bool']=1
        axyp2['bool']=1
        axyp3=axyp3.rename(columns={'bike_time':'time'})
        axyp3['bool']=0
        axyp4=axyp4.rename(columns={'taxi_time':'time'})
        axyp4['bool']=0
        aff_path=pd.DataFrame()
        aff_path=pd.concat([aff_path,axyp1])
        aff_path=pd.concat([aff_path,axyp2])
        aff_path=pd.concat([aff_path,axyp3])
        aff_path=pd.concat([aff_path,axyp4])

        # 3 
        odall1=copy.deepcopy(odall)
        odall1=odall1.reset_index()
        p8=xypath8.merge(odall1,on=['org','dst'],how='outer')
        p8=p8.fillna(-1)
        p8=p8[p8['index']==-1][['org','dst','path','time']]
        p8['bool']=0
        aff_path=pd.concat([aff_path,p8])
        return aff_path,upt

    def FOD_node_aff_path(node_i,tbpath,xypath8,nodes,wi,newod):

        id_dafnode=nodes[nodes[1]==node_i][0].to_list()[0]
        dafnode=node_i 
        nwi=wi[wi['station']==dafnode]['com_im'].to_list()[0]*100 # NI
        upt=max(xypath8[xypath8['org']==dafnode].groupby(['org','dst']).min('time')['time'].to_list())*nwi #
        ftime=upt #
        affect_nodes=xypath8[(xypath8['org']==dafnode)&(xypath8['time']<=upt)]['dst'].to_list()
        
        ods1=newod[newod['org']==dafnode][['org','dst']]  
        ods2=newod[newod['dst']==dafnode][['org','dst']]  
        od1=pd.DataFrame(affect_nodes,columns=['org'])
        ods3=newod.merge(od1,on='org',how='inner')[['org','dst']]
    
        odall=pd.DataFrame()
        odall=pd.concat([odall,ods1])
        odall=pd.concat([odall,ods2])
        odall=pd.concat([odall,ods3])
        #2  
        axyp=odall.merge(xypath8,on=['org','dst'],how='inner')
        #2.1 
        axyp1=copy.deepcopy(axyp)
        axyp1['ntime']=np.array(axyp['time'])+ftime
        #2.2 
        axyp2=copy.deepcopy(axyp)
        axyp2['path1']=axyp2['path'].apply(lambda x:str(x))
        ap1=pd.concat([axyp2, axyp2['path1'].str.replace('[','').str.replace(']','').str.split(' ', expand=True)], axis=1)
        cols1=ap1.columns
        apa=ap1[cols1[6::]].values
        dfapa=pd.DataFrame(np.argwhere(apa==str(id_dafnode)))
        dfapa.columns=['index','index1']
        axyp2=axyp2.reset_index()
        axyp3=axyp2.merge(dfapa,on='index',how='outer')
        axyp3.head()
        axyp3=axyp3.fillna(-1)
        axyp2=axyp3[axyp3['index1']==-1][['org','dst','path','time']]
         # 2.3 
        axypp=tbpath.merge(odall,on=['org','dst'],how='inner')
        axyp3=axypp[['org','dst','path','bike_time']]
        axyp4=axypp[['org','dst','path','taxi_time']]
        # 2.4 
        axyp1=axyp1[['org','dst','path','ntime']]
        axyp1=axyp1.rename(columns={'ntime':'time'})
        axyp1['bool']=1
        axyp2['bool']=1
        axyp3=axyp3.rename(columns={'bike_time':'time'})
        axyp3['bool']=0
        axyp4=axyp4.rename(columns={'taxi_time':'time'})
        axyp4['bool']=0
        aff_path=pd.DataFrame()
        aff_path=pd.concat([aff_path,axyp1])
        aff_path=pd.concat([aff_path,axyp2])
        aff_path=pd.concat([aff_path,axyp3])
        aff_path=pd.concat([aff_path,axyp4])
        
        odall1=copy.deepcopy(odall)
        odall1=odall1.reset_index()
        p8=xypath8.merge(odall1,on=['org','dst'],how='outer')
        p8=p8.fillna(-1)
        p8=p8[p8['index']==-1][['org','dst','path','time']]
        p8['bool']=1
        aff_path=pd.concat([aff_path,p8])
        return aff_path,upt
    
    def ICD_subs_aff_path(failuer_nodes,failuer_nodes_ind,ftime,tbpath,xypath8,wi,newod):
        
        df_failuer_node=pd.DataFrame(failuer_nodes)
        df_failuer_node.columns=['station']
        nwis=df_failuer_node.merge(wi,on='station',how='inner')[['station','com_im']]
        df_failuer_node.columns=['org']
        mt=df_failuer_node.merge(xypath8,on=['org'],
                              how='inner').groupby(['org','dst']).min(
            'time').reset_index().sort_values(by='time',ascending=False).head(1)
        mt=mt.reset_index().drop(columns='index')
        mt=mt.rename(columns={'org':'station'})
        mt=mt.merge(nwis,on='station',how='inner')
        upt=mt.iloc[0,2]*mt.iloc[0,3]*100 
        affect_nodes=list(set(df_failuer_node.merge(xypath8,on='org',how='inner')[
            df_failuer_node.merge(xypath8,on='org',how='inner')['time']<=upt]['dst'].to_list()))
        #
        ods1=newod.merge(df_failuer_node,on='org',how='inner')[['org','dst']] 
        df_failuer_node.columns=['dst']
        ods2=newod.merge(df_failuer_node,on='dst',how='inner')[['org','dst']] 
        
        xy=copy.deepcopy(xypath8)
        xy['path1']=xy['path'].apply(lambda x:str(x))
        xyp9=pd.concat([xy, xy['path1'].str.replace('[','').str.replace(']','').str.split(' ', expand=True)], axis=1)
        cols1=xyp9.columns
        xyp10=xyp9[cols1[6::]]
        arp=xyp10.values
        dfind=pd.DataFrame()
        for i in range(len(failuer_nodes_ind)):
            dfind=pd.concat([dfind,pd.DataFrame(np.argwhere(arp==str(failuer_nodes_ind[i])))])
        ods3=dfind.drop_duplicates([0,1]).reset_index().drop(columns='index')
        # 1.3
        od1=pd.DataFrame(affect_nodes,columns=['org'])
        ods4=newod.merge(od1,on='org',how='inner')[['org','dst']]
        #1.4 
        odall=pd.DataFrame()
        odall=pd.concat([odall,ods1])
        odall=pd.concat([odall,ods2])
        odall=pd.concat([odall,ods3])
        odall=pd.concat([odall,ods4])
        odall=odall.reset_index().drop(columns='index')
        #2  
        axyp=odall.merge(xypath8,on=['org','dst'],how='inner')
        #2.1 
        axyp1=copy.deepcopy(axyp)
        axyp1['ntime']=np.array(axyp['time'])+ftime
        #2.2 
        axyp2=copy.deepcopy(axyp)
        axyp2['path1']=axyp2['path'].apply(lambda x:str(x))
        ap1=pd.concat([axyp2, axyp2['path1'].str.replace('[','').str.replace(']','').str.split(' ', expand=True)], axis=1)
        cols1=ap1.columns
        apa=ap1[cols1[6::]].values
        axy=pd.DataFrame()
        for i in range(len(failuer_nodes_ind)):
            id_dafnode=failuer_nodes_ind[i]
            dfapa=pd.DataFrame(np.argwhere(apa==str(id_dafnode)))
            dfapa.columns=['index','index1']
            axyp2=axyp2.reset_index()
            axyp3=axyp2.merge(dfapa,on='index',how='outer')
            axyp3.head()
            axyp3=axyp3.fillna(-1)
            axyp2=axyp3[axyp3['index1']==-1][['org','dst','path','time']]
            axy=pd.concat([axy,axyp2])
        axyp2=axy
        # 2.3 
        axypp=tbpath.merge(odall,on=['org','dst'],how='inner')
        axyp3=axypp[['org','dst','path','bike_time']]
        axyp4=axypp[['org','dst','path','taxi_time']]
        # 2.4 
        axyp1=axyp1[['org','dst','path','ntime']]
        axyp1=axyp1.rename(columns={'ntime':'time'})
        axyp1['bool']=1
        axyp2['bool']=1
        axyp3=axyp3.rename(columns={'bike_time':'time'})
        axyp3['bool']=0
        axyp4=axyp4.rename(columns={'taxi_time':'time'})
        axyp4['bool']=0
        aff_path=pd.DataFrame()
        aff_path=pd.concat([aff_path,axyp1])
        aff_path=pd.concat([aff_path,axyp2])
        aff_path=pd.concat([aff_path,axyp3])
        aff_path=pd.concat([aff_path,axyp4])
       
        odall1=copy.deepcopy(odall)
        odall1=odall1.reset_index()
        p8=xypath8.merge(odall1,on=['org','dst'],how='outer')
        p8=p8.fillna(-1)
        p8=p8[p8['index']==-1][['org','dst','path','time']]
        p8['bool']=1
        aff_path=pd.concat([aff_path,p8])
        return aff_path,upt
    
    
    def FOD_subs_aff_path(failuer_nodes,failuer_nodes_ind,tbpath,xypath8,wi,newod):
        
        df_failuer_node=pd.DataFrame(failuer_nodes)
        df_failuer_node.columns=['station']
        nwis=df_failuer_node.merge(wi,on='station',how='inner')[['station','com_im']]
        df_failuer_node.columns=['org']
        mt=df_failuer_node.merge(xypath8,on=['org'],
                              how='inner').groupby(['org','dst']).min(
            'time').reset_index().sort_values(by='time',ascending=False).head(1)
        mt=mt.reset_index().drop(columns='index')
        mt=mt.rename(columns={'org':'station'})
        mt=mt.merge(nwis,on='station',how='inner')
        upt=mt.iloc[0,2]*mt.iloc[0,3]*100 
        ftime=upt
       
        affect_nodes=list(set(df_failuer_node.merge(xypath8,on='org',how='inner')[
            df_failuer_node.merge(xypath8,on='org',how='inner')['time']<=upt]['dst'].to_list()))
        
        ods1=newod.merge(df_failuer_node,on='org',how='inner')[['org','dst']] 
        df_failuer_node.columns=['dst']
        ods2=newod.merge(df_failuer_node,on='dst',how='inner')[['org','dst']] 
        
        od1=pd.DataFrame(affect_nodes,columns=['org'])
        ods3=newod.merge(od1,on='org',how='inner')[['org','dst']]
        
        odall=pd.DataFrame()
        odall=pd.concat([odall,ods1])
        odall=pd.concat([odall,ods2])
        odall=pd.concat([odall,ods3])
        odall=odall.reset_index().drop(columns='index')
        
        axyp=odall.merge(xypath8,on=['org','dst'],how='inner')
       
        axyp1=copy.deepcopy(axyp)
        axyp1['ntime']=np.array(axyp['time'])+ftime
        
        axyp2=copy.deepcopy(axyp)
        axyp2['path1']=axyp2['path'].apply(lambda x:str(x))
        ap1=pd.concat([axyp2, axyp2['path1'].str.replace('[','').str.replace(']','').str.split(' ', expand=True)], axis=1)
        cols1=ap1.columns
        apa=ap1[cols1[6::]].values
        axy=pd.DataFrame()
        for i in range(len(failuer_nodes_ind)):
            id_dafnode=failuer_nodes_ind[i]
            dfapa=pd.DataFrame(np.argwhere(apa==str(id_dafnode)))
            dfapa.columns=['index','index1']
            axyp2=axyp2.reset_index()
            axyp3=axyp2.merge(dfapa,on='index',how='outer')
            axyp3.head()
            axyp3=axyp3.fillna(-1)
            axyp2=axyp3[axyp3['index1']==-1][['org','dst','path','time']]
            axy=pd.concat([axy,axyp2])
        axyp2=axy
        
        axypp=tbpath.merge(odall,on=['org','dst'],how='inner')
        axyp3=axypp[['org','dst','path','bike_time']]
        axyp4=axypp[['org','dst','path','taxi_time']]

        axyp1=axyp1[['org','dst','path','ntime']]
        axyp1=axyp1.rename(columns={'ntime':'time'})
        axyp1['bool']=1
        axyp2['bool']=1
        axyp3=axyp3.rename(columns={'bike_time':'time'})
        axyp3['bool']=0
        axyp4=axyp4.rename(columns={'taxi_time':'time'})
        axyp4['bool']=0
        aff_path=pd.DataFrame()
        aff_path=pd.concat([aff_path,axyp1])
        aff_path=pd.concat([aff_path,axyp2])
        aff_path=pd.concat([aff_path,axyp3])
        aff_path=pd.concat([aff_path,axyp4])
        
        odall1=copy.deepcopy(odall)
        odall1=odall1.reset_index()
        p8=xypath8.merge(odall1,on=['org','dst'],how='outer')
        p8=p8.fillna(-1)
        p8=p8[p8['index']==-1][['org','dst','path','time']]
        p8['bool']=1
        aff_path=pd.concat([aff_path,p8])
        return aff_path,upt
class fun_R():
    def cal_exp_R(Q0,Qv,tv,tr):
        a=Q0
        b=-np.log(Qv/a)
        a1=Qv
        b1=-((tr-0)/(tr-tv))*np.log(Q0/a1)
        def func1(t):
            return a*np.exp(b*t/(tv))
        def func2(t):
            return a1*np.exp(b1*(t-tv)/(tr-tv))
        fArea1,err1 = integrate.quad(func1,0,tv)
        fArea2,err2 = integrate.quad(func2,tv,tr)
        return fArea1+fArea2
    # 三角函数
    def cal_cos_R(Q0,Qv,tv,tr):
        # 过程1：
        #1.1 t=0时：
        a=2*Q0
        b=np.arccos(1-2*Qv/a)
        # 过程2
        a1=2*Qv
        b1=np.pi*2
        def func1(t):
            return (a/2)*(1+np.cos(b*t/tv))
        def func2(t):
            return (a1/2)*(1+np.cos(b1*(t-tv)/(tr-tv)))
        fArea1,err1 = integrate.quad(func1,0,tv)
        fArea2,err2 = integrate.quad(func2,tv,tr)
        return fArea1+fArea2