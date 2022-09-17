import pandas as pd
from sklearn.linear_model import LogisticRegression
from pandas.core.frame import DataFrame
from sklearn.model_selection import train_test_split
import numpy as np
import time

#module for dataprocessing and prediction
def Modelpredict(tpl):
    
    #reading dataset
    df = pd.read_csv("C:\\Users\\keshav\\Documents\\SE_project\\CODE\\heart.csv")

    #data processing
    '''
    Converting string values into numerical values
    '''
    Sex = {'M':1,'F':0}
    df.Sex = [Sex[item] for item in df.Sex]

    ChestPainType = {'TA':1,'ATA':2,'NAP':3,'ASY':4}
    df.ChestPainType = [ChestPainType[item] for item in df.ChestPainType]

    RestingECG = {'Normal':0,'ST':1,'LVH':2}
    df.RestingECG = [RestingECG[item] for item in df.RestingECG]

    ExerciseAngina = {'N':0,'Y':1}
    df.ExerciseAngina = [ExerciseAngina[item] for item in df.ExerciseAngina]

    ST_Slope = {'Flat':0,'Up':1,'Down':-1}
    df.ST_Slope = [ST_Slope[item] for item in df.ST_Slope]


    train_set , test_set = train_test_split(df,test_size = 0.1,random_state=42)
    final_train_set = train_set.drop('HeartDisease',axis=1)
    train_setLabel = train_set['HeartDisease'].copy()

    #using LogisticRegression model
    model = LogisticRegression(max_iter = 1000)
    model.fit(final_train_set,train_setLabel)

    #creating a data frame for the values taken from database
    cpt = 0
    sex =0
    recg = 0
    exag = 0
    slp = 0

    if tpl[1] == 'TA':
        cpt = 1
    elif tpl[1] == 'ATA': 
        cpt = 2
    elif tpl[1] == 'NAP':
        cpt = 3
    elif tpl[1] == 'ASY':
        cpt = 4      

    if tpl[11] == 'M':
        sex = 1
    elif tpl[11] == 'F':
        sex = 0    
        
    if tpl[5]=='Normal':
        recg = 0
    elif tpl[5]=='ST':
        recg = 1 
    elif tpl[5]=='LVH':
        recg = 2       

    if tpl[7] == 'N':
        exag = 0
    elif tpl[7] == 'Y':
        exag = 1    

    if tpl[9]=='Flat':
        slp = 0
    elif tpl[9]=='Up':
        slp = 1
    elif tpl[9]=='Down':
        slp = -1        

    #dataframe creation
    data = {'AGE':[tpl[10]],'Sex':[sex],'ChestPainType':[cpt],'RestingBP':[tpl[2]],'Cholesterol':[tpl[3]],'FastingBS':[eval(tpl[4])],'RestingECG':[recg],'MaxHR':[tpl[6]],'ExerciseAngina':[exag],'Oldpeak':[tpl[8]],'ST_Slope':[slp]}
    dt = pd.DataFrame(data)
    p = model.predict(dt) #passing patient lab test info in model for prediction
    return p[0]       #returning the predicted result