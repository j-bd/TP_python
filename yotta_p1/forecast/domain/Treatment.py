from forecast.infrastructure.Load import Load
import numpy as np
import forecast.settings.base as sg
import pandas as pd
from datetime import datetime as dt
import datetime

class Treatment:

    nb_month = 12

    def __init__(self, data):
        self.data = data

    def run_preprocessing(self):
        self.data = self.treat_NaN_RESULT_LAST_CAMPAIGN() # OK effet
        #self.data = self.treat_BALANCE() # USELESS effet
        #self.data = self.add_PRECARITY() # OK effet
        self.data = self.add_AT_DEBIT() # OK effet
        self.data = self.drop_DURATION_CONTACT() # OK effet
        self.data = self.add_CAT_CONTACT_LAST_CAMPAIGN()
        self.data = self.add_CAT_CONTACT()
        #self.data = self.time_last_contact()
        #self.data = self.treat_NB_DAY_LAST_CONTACT() # USELESS effet
        #self.data = self.treat_NB_CONTACT() # USELESS effet
        #self.data = self.treat_NB_CONTACT_LAST_CAMPAIGN() # USELESS effet
        return self.data

    def treat_NaN_RESULT_LAST_CAMPAIGN(self):
        not_contacted = self.data.query('{} == -1'.format(sg.NB_DAY_LAST_CONTACT)).copy()
        not_contacted[sg.RESULT_LAST_CAMPAIGN] = not_contacted[sg.RESULT_LAST_CAMPAIGN].fillna("Not contacted")
        INDEX = list(not_contacted.index)
        self.data.loc[INDEX] = not_contacted
        contacted = self.data.query('{} != -1'.format(sg.NB_DAY_LAST_CONTACT)).copy()
        contacted[sg.RESULT_LAST_CAMPAIGN] = contacted[sg.RESULT_LAST_CAMPAIGN].fillna("Autre")
        INDEX = list(contacted.index)
        self.data.loc[INDEX] = contacted
        return self.data

    def add_AT_DEBIT(self):
        self.data['AT_DEBIT'] = 'No'
        AT_DEBIT_TRUE = self.data.query('{} < 0'.format(sg.BALANCE))\
                                .assign(AT_DEBIT=lambda x: 'Yes').copy()
        INDEX = list(self.data.query('{} < 0'.format(sg.BALANCE)).index)
        self.data.loc[INDEX] = AT_DEBIT_TRUE
        return self.data

    def add_PRECARITY(self):
        self.data['PRECARITY'] = 'No' 
        PRECARITY_TRUE = self.data.query('{} ==0 '.format(sg.BALANCE))\
                                    .assign(PRECARITY=lambda x: 'Yes').copy()
        INDEX = list(self.data.query('{} ==0 '.format(sg.BALANCE)).index)
        self.data.loc[INDEX] = PRECARITY_TRUE
        return self.data

    def treat_BALANCE(self):
        self.data = self.add_AT_DEBIT()
        self.data[sg.BALANCE] = self.data[sg.BALANCE].apply(lambda x: np.absolute(x)).copy()
        INDEX_DEBIT = list(self.data.query('{} >= 0 and {} < 1'.format(sg.BALANCE,sg.BALANCE)).index)
        self.data.loc[INDEX_DEBIT,sg.BALANCE] = 1
        self.data[sg.BALANCE] = self.data.BALANCE.apply(lambda x: np.log(x)).copy()

        self.data = self.add_PRECARITY()
        #MEAN_BALANCE = self.data[sg.BALANCE].mean()
        #treat_data = self.data.query('{} == 0'.format(sg.BALANCE)).copy()
        #INDEX_PRECARITY = list(self.data.query('{} == 0'.format(sg.BALANCE)).index)
        #treat_data[sg.BALANCE] = MEAN_BALANCE
        #self.data.loc[INDEX_PRECARITY] = treat_data
        return self.data

    def drop_DURATION_CONTACT(self):
        self.data = self.data.drop(sg.DURATION_CONTACT, axis=1)
        return self.data 

    def treat_NB_DAY_LAST_CONTACT(self):
        col = sg.NB_DAY_LAST_CONTACT
        restriction_data = self.data.query('{} > -1'.format(col)).copy()
        INDEX_PRINCIPAL = list(self.data.query('{} > -1'.format(col)).index)

        restriction_data[col].describe()
        MEAN_NB_DAY_LAST_CONTACT = round(restriction_data[col].mean(),0)
        THRESHOLD_MEAN = np.abs(restriction_data[col] - MEAN_NB_DAY_LAST_CONTACT)
        STD_DEV_ACCEPTED = 3 * np.std(restriction_data[col])

        treat_data = restriction_data[THRESHOLD_MEAN >= STD_DEV_ACCEPTED].copy()
        treat_data[col] = MEAN_NB_DAY_LAST_CONTACT
        INDEX_EXTREM = list(treat_data.index)
        restriction_data.loc[INDEX_EXTREM] = treat_data
        self.data.loc[INDEX_PRINCIPAL] = restriction_data

        MEAN_NB_DAY_LAST_CONTACT = round(restriction_data[col].mean(),0)
        treat_NaN = self.data.query('{} == -1'.format(col)).copy()
        treat_NaN[col] = MEAN_NB_DAY_LAST_CONTACT
        INDEX_NaN = list(treat_NaN.index)
        self.data.loc[INDEX_NaN] = treat_NaN
        return self.data

    def treat_NB_CONTACT_LAST_CAMPAIGN(self):
        col = sg.NB_CONTACT_LAST_CAMPAIGN
        restriction_data = self.data.query('{} > 0'.format(col)).copy()

        MEAN = round(self.data[col].mean(),0)
        THRESHOLD_MEAN = np.abs(self.data[col] - MEAN)
        STD_DEV_ACCEPTED = 6 * self.data[col].std()

        treat_data = self.data[THRESHOLD_MEAN >= STD_DEV_ACCEPTED].copy()
        treat_data[col] = MEAN

        INDEX = list(treat_data.index)
        self.data.loc[INDEX] = treat_data
        return self.data

    def treat_NB_CONTACT(self):
        col = sg.NB_CONTACT
        restriction_data = self.data.query('{} > 1'.format(col)).copy()
        MEAN = round(self.data[col].mean(),0)
        THRESHOLD_MEAN = np.abs(self.data[col] - MEAN)
        STD_DEV_ACCEPTED = 6 * self.data[col].std()
        treat_data = self.data[THRESHOLD_MEAN >= STD_DEV_ACCEPTED].copy()
        treat_data[col] = MEAN
        INDEX = list(treat_data.index)
        self.data.loc[INDEX] = treat_data
        return self.data

    def discretisation_NB_CONTACT_LAST_CAMPAIGN(self, row):
        if row == 0:
            return 'Not contacted'
        elif row > 0 and row < 5:
            return 'Between 1 and 4 call'
        elif row >= 5 and row < 11:
            return 'Between 5 and 10 call'
        elif row >= 11 and row < 15:
            return 'Between 11 and 14 call'
        elif row >= 15:
            return 'More than 15 call'
        else:
            return np.NaN

    def add_CAT_CONTACT_LAST_CAMPAIGN(self):
        self.data['CAT_CONTACT_LAST_CAMPAIGN'] = self.data[sg.NB_CONTACT_LAST_CAMPAIGN].apply(lambda row: self.discretisation_NB_CONTACT_LAST_CAMPAIGN(row))
        self.data = self.data.drop(sg.NB_CONTACT_LAST_CAMPAIGN,axis=1)
        return self.data

    def discretisation_NB_CONTACT(self, row):
        if row == 1:
            return '1 call'
        elif row > 1 and row < 4:
            return '2 or 3 call'
        elif row >= 4 and row < 7:
            return 'Between 4 and 6 call'
        elif row >= 11 and row < 15:
            return 'Between 7 and 11 call'
        elif row >= 11:
            return 'More than 1 call'
        else:
            return np.NaN

    def add_CAT_CONTACT(self):
        self.data['CAT_CONTACT'] = self.data[sg.NB_CONTACT].apply(lambda row: self.discretisation_NB_CONTACT(row))
        self.data = self.data.drop(sg.NB_CONTACT,axis=1)
        return self.data

    def month_last_contact(self, row):
        if row[sg.NB_DAY_LAST_CONTACT] == -1:
            return 0
        else:
            date = row[sg.DATE]
            gap_days = datetime.timedelta(days = int(row.NB_DAY_LAST_CONTACT))
            return (date - gap_days).month

    def week_of_the_year_last_contact(self, row):
        if row[sg.NB_DAY_LAST_CONTACT] == -1:
            return 0
        else:
            date = row[sg.DATE]
            gap_days = datetime.timedelta(days = int(row.NB_DAY_LAST_CONTACT))
            return (date - gap_days).isocalendar()[1]

    def gap_last_contact_month(self, row):
        if row[sg.NB_DAY_LAST_CONTACT] == -1:
            return 0
        else:
            date = row[sg.DATE]
            gap_days = datetime.timedelta(days = int(row.NB_DAY_LAST_CONTACT))
            date_before = date - gap_days
            return (date.year - date_before.year) * self.nb_month + (date.month - date_before.month)

    def time_last_contact(self):
        self.data = self.data[sg.DATE].astype('datetime64[ns]')
        self.data['month_last_contact'] = self.data.apply(lambda x: self.month_last_contact(x))
        self.data['week_of_the_year_last_contact'] = self.data.apply(lambda x: self.week_of_the_year_last_contact(x))
        self.data['gap_last_contact_month'] = self.data.apply(lambda x: self.gap_last_contact_month(x))
        self.data = self.data[sg.DATE].astype('object') 
        return self.data


    #def LabelEncoding_adapted(self):
    #    columns_quali = self.data.select_dtypes(include=['object']).columns
    #    le = LabelEncoder()
    #    le.fit_transform(self.data)


# NB_CONTACT,	NB_DAY_LAST_CONTACT,	NB_CONTACT_LAST_CAMPAIGN	
if __name__ == "__main__": 
    df, df_soc_eco = Load().Download()
    df_treat = Treatment(df).run_preprocessing()
    df_treat.head()
    
    df_treat.CAT_CONTACT
    df.DATE = df.DATE.astype('datetime64[ns]')
    df.DATE[41065]
    df.NB_DAY_LAST_CONTACT[41065]
    y = df.DATE[41065] - datetime.timedelta(days = int(df.NB_DAY_LAST_CONTACT[41065]))
    y
    z = (df.DATE[41065].year - y.year) * 12 + (df.DATE[41065].month - y.month)
    z
    abs(df.DATE[41065] -y)
    y.isocalendar()[1]

    format_date = '%Y-%m-%d'
    df.dtypes
    
# Teste de répartition pour NB_CONTACT
if __name__ == "__main__": 
    
    x1 = df.query('NB_CONTACT > 1 and NB_CONTACT < 4')
    x2 = df.query('NB_CONTACT >= 4 and NB_CONTACT < 7')
    x3 = df.query('NB_CONTACT >= 7 and NB_CONTACT < 11')
    x4 = df.query('NB_CONTACT >= 11')
    x5 = df.query('NB_CONTACT == 1')

    x1y = x1[x1['SUBSCRIPTION'] == 'Yes']
    x1n = x1[x1['SUBSCRIPTION'] == 'No']

    x2y = x2[x2['SUBSCRIPTION'] == 'Yes']
    x2n = x2[x2['SUBSCRIPTION'] == 'No']

    x3y = x3[x3['SUBSCRIPTION'] == 'Yes']
    x3n = x3[x3['SUBSCRIPTION'] == 'No']

    x4y = x4[x4['SUBSCRIPTION'] == 'Yes']
    x4n = x4[x4['SUBSCRIPTION'] == 'No']

    x5y = x5[x5['SUBSCRIPTION'] == 'Yes']
    x5n = x5[x5['SUBSCRIPTION'] == 'No']

    print('condition1')
    print(x1.shape[0])
    x1y.shape[0]/(x1n.shape[0]+x1y.shape[0])
    x1n.shape[0]/(x1n.shape[0]+x1y.shape[0])

    print('condition2')
    print(x2.shape[0])
    x2y.shape[0]/(x2n.shape[0]+x2y.shape[0])
    x2n.shape[0]/(x2n.shape[0]+x2y.shape[0])
    
    print('condition3')
    print(x3.shape[0])
    x3y.shape[0]/(x3n.shape[0]+x3y.shape[0])
    x3n.shape[0]/(x3n.shape[0]+x3y.shape[0])

    print('condition4')
    print(x4.shape[0])
    x4y.shape[0]/(x4n.shape[0]+x4y.shape[0])
    x4n.shape[0]/(x4n.shape[0]+x4y.shape[0])

    print('condition5')
    print(x5.shape[0])
    x5y.shape[0]/(x5n.shape[0]+x5y.shape[0])
    x5n.shape[0]/(x5n.shape[0]+x5y.shape[0])

    df_treat = Treatment(df).run_preprocessing()
    df_treat.head()

    perc_by_value = []
    value = []
    perc_no = []
    perc_yes = []
    taille_ech =[]
    for i in range(max(df.NB_CONTACT)):
        if i in list(df.NB_CONTACT):
            x = df.query('NB_CONTACT == {}'.format(i))
            taille = x.shape[0]
            taille_ech.append(taille)
            xy = x[x['SUBSCRIPTION']=='Yes']
            xn = x[x['SUBSCRIPTION']=='No']
            if xy.shape[0]>0 and xn.shape[0]>0:
                perc_by_value.append(x.shape[0]/df.shape[0]*100)
                value.append(i)
                perc_yes.append(xy.shape[0]/ (xy.shape[0]+xn.shape[0])*100)
                perc_no.append(xn.shape[0]/ (xy.shape[0]+xn.shape[0])*100)
            else:
                perc_by_value.append(x.shape[0]/df.shape[0]*100)
                value.append(i)
                perc_yes.append('just one value')
                perc_no.append('just one value')


    t = pd.DataFrame(taille_ech,columns=["taille"])
    val = pd.DataFrame(value,columns=["value"])
    pdf = pd.DataFrame(perc_by_value,columns=['percentage of df'])
    pn = pd.DataFrame(perc_no,columns=['percentage of no'])
    py = pd.DataFrame(perc_yes,columns=['percentage of yes'])
    data = pd.concat([val,pdf,t,pn,py], axis=1)

    data


# Teste de répartition pour NB_CONTACT_LAST_CAMPAIGN
if __name__ == "__main__": 
    
    x1 = df.query('NB_CONTACT_LAST_CAMPAIGN > 0 and NB_CONTACT_LAST_CAMPAIGN < 5')
    x2 = df.query('NB_CONTACT_LAST_CAMPAIGN >= 5 and NB_CONTACT_LAST_CAMPAIGN < 11')
    x3 = df.query('NB_CONTACT_LAST_CAMPAIGN > 11 and NB_CONTACT_LAST_CAMPAIGN < 15')
    x4 = df.query('NB_CONTACT_LAST_CAMPAIGN >= 15')
    x5 = df.query('NB_CONTACT_LAST_CAMPAIGN == 0')

    x1y = x1[x1['SUBSCRIPTION'] == 'Yes']
    x1n = x1[x1['SUBSCRIPTION'] == 'No']

    x2y = x2[x2['SUBSCRIPTION'] == 'Yes']
    x2n = x2[x2['SUBSCRIPTION'] == 'No']

    x3y = x3[x3['SUBSCRIPTION'] == 'Yes']
    x3n = x3[x3['SUBSCRIPTION'] == 'No']

    x4y = x4[x4['SUBSCRIPTION'] == 'Yes']
    x4n = x4[x4['SUBSCRIPTION'] == 'No']

    x5y = x5[x5['SUBSCRIPTION'] == 'Yes']
    x5n = x5[x5['SUBSCRIPTION'] == 'No']

    print('condition1')
    print(x1.shape[0])
    x1y.shape[0]/(x1n.shape[0]+x1y.shape[0])
    x1n.shape[0]/(x1n.shape[0]+x1y.shape[0])

    print('condition2')
    print(x2.shape[0])
    x2y.shape[0]/(x2n.shape[0]+x2y.shape[0])
    x2n.shape[0]/(x2n.shape[0]+x2y.shape[0])
    
    print('condition3')
    print(x3.shape[0])
    x3y.shape[0]/(x3n.shape[0]+x3y.shape[0])
    x3n.shape[0]/(x3n.shape[0]+x3y.shape[0])

    print('condition4')
    print(x4.shape[0])
    x4y.shape[0]/(x4n.shape[0]+x4y.shape[0])
    x4n.shape[0]/(x4n.shape[0]+x4y.shape[0])

    print('condition5')
    print(x5.shape[0])
    x5y.shape[0]/(x5n.shape[0]+x5y.shape[0])
    x5n.shape[0]/(x5n.shape[0]+x5y.shape[0])

    df_treat = Treatment(df).run_preprocessing()
    df_treat.head()

    perc_by_value = []
    value = []
    perc_no = []
    perc_yes = []
    taille_ech =[]
    for i in range(max(df.NB_CONTACT_LAST_CAMPAIGN)):
        if i in list(df.NB_CONTACT_LAST_CAMPAIGN):
            x = df.query('NB_CONTACT_LAST_CAMPAIGN == {}'.format(i))
            taille = x.shape[0]
            taille_ech.append(taille)
            xy = x[x['SUBSCRIPTION']=='Yes']
            xn = x[x['SUBSCRIPTION']=='No']
            if xy.shape[0]>0 and xn.shape[0]>0:
                perc_by_value.append(x.shape[0]/df.shape[0]*100)
                value.append(i)
                perc_yes.append(xy.shape[0]/ (xy.shape[0]+xn.shape[0])*100)
                perc_no.append(xn.shape[0]/ (xy.shape[0]+xn.shape[0])*100)
            else:
                perc_by_value.append(x.shape[0]/df.shape[0]*100)
                value.append(i)
                perc_yes.append('just one value')
                perc_no.append('just one value')


    t = pd.DataFrame(taille_ech,columns=["taille"])
    val = pd.DataFrame(value,columns=["value"])
    pdf = pd.DataFrame(perc_by_value,columns=['percentage of df'])
    pn = pd.DataFrame(perc_no,columns=['percentage of no'])
    py = pd.DataFrame(perc_yes,columns=['percentage of yes'])
    data = pd.concat([val,pdf,t,pn,py], axis=1)

    data
