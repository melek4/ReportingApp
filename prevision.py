import pymysql

import pandas as pd
import datetime

conn=pymysql.connect(host='localhost',port=int(3306),user='root',passwd='',db='hr')
personnel1=pd.read_sql_query("SELECT * FROM personnel ",conn)
personnel1 = personnel1.loc[personnel1['PERS_CET_9']==0]
personnel = personnel1.drop(columns=['PERS_DATE_REC','PERS_DATE_NAIS', 'PERS_AFFECT_92', 'PERS_NATURAGENT_93', 'PERS_QUALIF_X45', 'PERS_CATPERS_9', 'PERS_NATPERS_9', 'PERS_SEXE_X', 'PERS_CET_9'])
absence = pd.read_sql_query("SELECT * FROM absence ",conn)
pers_abs = personnel.merge(absence,left_on='PERS_MAT_95',right_on='ABS_MAT_95', how='left')
pers_abs = pers_abs.drop(columns=['ABS_MAT_95', 'ABS_PERDEB_X', 'ABS_DATE_FIN', 'ABS_PERFIN_X', 'ABS_CUMULE_9', 'INDEX_PK'])
retard = pd.read_sql_query("SELECT * FROM retard ",conn)
pers_ret = personnel.merge(retard,left_on='PERS_MAT_95',right_on='PERS_MAT_95', how='left')
pers_ret = pers_ret.drop(columns=['TRIM', 'RECAP', 'INDEX_PK'])

def absence_condition(mat, year, data):
    pers = pers_abs[pers_abs.PERS_MAT_95==mat]
    
    not_justified = False
    y=pd.DatetimeIndex(pers['ABS_DATE_DEB']).year
    year1data = pers[y==year-2]
    year2data = pers[y==year-1]
    year1_abs = year1data['ABS_NBRJOUR_93'].sum() # set the value of the selected rows' new 'year1' 
                                                                        # column to the number of his abs in the first year
    year2_abs = year2data['ABS_NBRJOUR_93'].sum()
    if (9 in year1data['ABS_NAT_9'].unique()) or (9 in year2data['ABS_NAT_9'].unique()):
        not_justified = True
    
    data['year1_abs'].append(year1_abs)
    data['year2_abs'].append(year2_abs)
    data['not_justified'].append(not_justified)


def retard_condition(mat, year, data):
    pers = pers_ret[pers_ret.PERS_MAT_95==mat]
    
    y=pers['ANNE']
    year1data = pers[y==year-2]
    year2data = pers[y==year-1]
    year1_ret = year1data['NB_RETARD'].sum()
    year2_ret = year2data['NB_RETARD'].sum()
    
    data['year1_ret'].append(year1_ret)
    data['year2_ret'].append(year2_ret)


fonction = pd.read_sql_query("SELECT * FROM fonction ",conn)
pers_fonction = personnel.merge(fonction,left_on='PERS_MAT_95',right_on='HFONC_MAT_95', how='left')

def fonction_condition(mat, data):
    current_year = pd.to_datetime(datetime.date.today())
    if mat in pers_fonction.HFONC_MAT_95.unique():
        pers = pers_fonction[pers_fonction.PERS_MAT_95==mat]
        

        y=pd.to_datetime(pd.DatetimeIndex(pers['HFONC_DATE1']))

        ancienneté = current_year-y
        ancienneté = (ancienneté[0].days)/365
        data['ancienneté'].append(ancienneté)
    else : 
        pers = personnel1[personnel1.PERS_MAT_95==mat]
        anc = pd.to_datetime(pd.DatetimeIndex(pers['PERS_DATE_REC']))
        ancienneté = current_year-anc
        ancienneté = (ancienneté[0].days)/365
        data['ancienneté'].append(ancienneté)


note = pd.read_sql_query("SELECT * FROM note ",conn)
pers_note = personnel.merge(note,left_on='PERS_MAT_95',right_on='NOTE_MAT_95', how='left')


def note_condition(mat, year, data):
    pers = pers_note[pers_note.PERS_MAT_95==mat]
    
    y=pers['NOTE_ANNEE_94']
    year1data = pers[y==year-2]
    year2data = pers[y==year-1]
    year1_note = year1data['NOTE_NOTETRIMES_92'].sum()/4
    year2_note = year2data['NOTE_NOTETRIMES_92'].sum()/4
    
    data['year1_note'].append(year1_note)
    data['year2_note'].append(year2_note)


personnel = personnel.set_index('PERS_MAT_95')

current_year = datetime.date.today().year
data = dict()
data = {'mat':[],'year':[], 'year1_abs':[], 'year2_abs':[], 'not_justified':[], 'year1_ret':[], 'year2_ret':[] , 'year1_note':[], 'year2_note':[], 'ancienneté':[]}
for index, row in personnel.iterrows():
    data['mat'].append(index)
    data['year'].append(current_year)
    absence_condition(index, current_year, data) # after setting the index to PERS_MAT_95, each rows' index is the PERS_MAT_95 of the personnel
    retard_condition(index, current_year, data)
    note_condition(index, current_year, data)
    fonction_condition(index, data)
    
df_for_ml = pd.DataFrame(data)
for index, row in df_for_ml.iterrows(): 
    if row['year1_abs']<15 and row['year2_abs']<15 and row['not_justified']==False and (row['ancienneté']>=3 or row['ancienneté']==-3) and row['year1_ret']<15 and row['year2_ret']<15 and row['year1_note']>=18 and row['year2_note']>=18 :
        val = True
    else:
        val = False
    df_for_ml.at[index,'promotion'] = val


feature_cols = ['year1_abs', 'year2_abs', 'not_justified', 'year1_ret', 'year2_ret', 'year1_note', 'year2_note', 'ancienneté']
X = df_for_ml[feature_cols]
y = df_for_ml.promotion
y=y.astype('int')
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=0)

from sklearn.ensemble import RandomForestClassifier
ml_model = RandomForestClassifier()
ml_model.fit(X_train, y_train)

import pickle

pickle.dump(ml_model, open("random_forest.sav","wb"))