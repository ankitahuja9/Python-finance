import pandas as pd
import numpy as np
from warnings import filterwarnings
filterwarnings("ignore")
# Main class score
class score:
    # This class will give the scores to the benchmarks, so you can choose the best benchmark per category. Usage of similarity algorithm
    # for the time series of the prices of the benchmarke has been made which is used in the object: simi_1 and then final score object uses
    # this output along with nb_funds and AUM to give the final score of each benchmark, the maximum is the score the more representative
    # is the benchmark of the all other benchmarks in that category.

    def score_representative(df):

        ## This module contains the way to calculate the score of the similarity between the time series, the method used in extended jaccard method
        ## cosine method and Tanimoto method of similarity. This module will take the input of the matrix containing the data series and will apply 
        ## all these method to calculate the score, along with the correlation, weighted average will be taken of all these score to give the final similarity score
        ## Advantage of using these method over and along the correlation is that they will incorporate the non linear property of the prices, which 
        ## is not the case in correlation but instead of replacing the correlation, the weighted average of 3 scores and correlation will be used to give the
        ## score of the similarity, higher the score more similar is the given time series to all others and can be replaced with others. 

        def simi_1(df): ## This function is calculating the score on the basis of Jaccard method
            a=pd.DataFrame()
            k=[]
            for i in range(0,len(df.columns)-1):
                first=pd.DataFrame(df.iloc[:,i])
                for j in range(1,len(df.columns)):
                    if i == j:
                        pass
                    else:
                        d=pd.DataFrame(df.iloc[:,j])
                        f=pd.concat([first,d],axis=1)
                        name=f.iloc[:,0].name + str('-')+  f.iloc[:,1].name
                        num=(f.iloc[:,0]*f.iloc[:,1]).sum()
                        deno=(f**2).sum()
                        deno_1=deno.sum()
                        sim=pd.Series(num/(deno_1-num))
                        a=a.append(sim,ignore_index=True)
                        k.append(name)
            a.index=k
            a=a.reset_index()
            q=[]
            for k in df.columns:
                m1=a[a['index'].str.contains(k)]
                simi=((m1.iloc[:,1]/m1.iloc[:,1].sum())*m1.iloc[:,1]).sum()
                q.append(simi)
            similarity_1=pd.DataFrame(data=q,index=df.columns,columns=['similarity_1'])
            return similarity_1

        def simi_2(df): #this method is using Cosine method
            a=pd.DataFrame()
            k=[]
            for i in range(0,len(df.columns)-1):
                first=pd.DataFrame(df.iloc[:,i])
                for j in range(1,len(df.columns)):
                    if i == j:
                        pass
                    else:
                        d=pd.DataFrame(df.iloc[:,j])
                        f=pd.concat([first,d],axis=1)
                        name=f.iloc[:,0].name + str('-')+  f.iloc[:,1].name
                        num=(f.iloc[:,0]*f.iloc[:,1]).sum()
                        deno=(f**2)
                        k1=(deno).sum()
                        deno_1=np.sqrt(k1[0]*k1[1])
                        sim=pd.Series(num/(deno_1))
                        a=a.append(sim,ignore_index=True)
                        k.append(name)
            a.index=k
            a=a.reset_index()
            q=[]
            for k in df.columns:
                m1=a[a['index'].str.contains(k)]
                simi=((m1.iloc[:,1]/m1.iloc[:,1].sum())*m1.iloc[:,1]).sum()
                q.append(simi)
            similarity_2=pd.DataFrame(data=q,index=df.columns,columns=['similarity_2'])
            return similarity_2
        
        def simi_3(df): # this method is using Tanimoto method of similarity 
            a=pd.DataFrame()
            k=[]
            for i in range(0,len(df.columns)-1):
                first=pd.DataFrame(df.iloc[:,i])
                for j in range(1,len(df.columns)):
                    if i == j:
                        pass
                    else:
                        d=pd.DataFrame(df.iloc[:,j])
                        f=pd.concat([first,d],axis=1)
                        name=f.iloc[:,0].name + str('-')+  f.iloc[:,1].name
                        num=2*(f.iloc[:,0]*f.iloc[:,1]).sum()
                        deno=(f**2).sum().sum()
                        sim=pd.Series(num/(deno))
                        a=a.append(sim,ignore_index=True)
                        k.append(name)
            a.index=k
            a=a.reset_index()
            q=[]
            for k in df.columns:
                m1=a[a['index'].str.contains(k)]
                simi=((m1.iloc[:,1]/m1.iloc[:,1].sum())*m1.iloc[:,1]).sum()
                q.append(simi)
            similarity_3=pd.DataFrame(data=q,index=df.columns,columns=['similarity_2'])
            return similarity_3

        s0=pd.DataFrame(df.corr().mean(),columns=['Corr-Score']) # traditional correlation score
        s1=simi_1(df=df) # Score1
        s2=simi_2(df=df) # Score2
        s3=simi_3(df=df) # Score3

        table=pd.concat([s1,s2,s3,s0],axis=1)
        w=table/pd.DataFrame((table.sum(axis=1)).values).values  # Weighted average of all the scores
        represent=pd.DataFrame((w * table).sum(axis=1),columns=['Score of Similarity in %'])
        return round(represent*100,2)
    

    # This module wil give you final score of the matirx, taking into consideration the Nb 0f Funds represented, AUM, and the similarity we 
    # calculated in the above module.
    #df1=== Prices of the benchmarks
    #df2=== Information matrix of Nb of funds and AUM
    def final_score(df1,df2):
        m1=score.score_representative(df1)
        d_f=pd.concat([m1,df2],axis=1)
        s=pd.DataFrame(((d_f/d_f.max())*0.33).sum(axis=1),columns=['Score'])
        s=s.sort_values(by='Score',ascending=False)
        return round(s,2) #########     Final output of the score class, giving the score to each bench and ranking from best to worst.

class test:
    def test():
        data_1=pd.DataFrame(data=[[2,3,1,3],[4,5,2,0],[2,7,7,1],[6,1,9,10],[8,9,3,20],[2,1,5,3],[2,4,5,11]],columns=['T1','T2','T3','T4'])
        data_2=pd.DataFrame(data=[[2,3],[4,2],[3,8],[6,8]],index=['T1','T2','T3','T4'],columns=['Nbfunds','AUM'])
        result=pd.DataFrame(data=[[0.95],[0.77],[0.59],[0.56]],index=['T1','T2','T3','T4'],columns=['Score'])
        a=score.final_score(data_1,data_2)
        if (a - result).sum()[0] ==0:
            print('The code has passed the test \nReading the input files and making the computation with respect to the benchmarks')
            data_1=pd.read_csv("/home/ankit/workspace/AOI_Predictor_Optimizer/indicators_changes/Bench_finder/fair_price.csv",index_col=0,header=0,parse_dates=True)
            data_2=pd.read_excel("/home/ankit/workspace/AOI_Predictor_Optimizer/indicators_changes/Bench_finder/test_data_input_2.xlsx",index_col=0,header=0,parse_dates=True)
            s=score.final_score(data_1,data_2)
            print(s)
        else:
            print('The code has not passed the test')
test.test()