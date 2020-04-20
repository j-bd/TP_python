import forecast.settings.base as sg
import pandas as pd

class Load:
    '''
    Download the database.

    Attributes
    ----------
    format: the choice is between CSV

    Methods
    -------
    Download()
    '''
    
    def Download(self):
        ''' Download the database '''
        try:
            data_principal = pd.read_csv('data/raw/' + sg.name_file_data, encoding='utf-8')
            data_socio_eco = pd.read_csv('data/raw/' + sg.name_file_socio_eco, encoding='utf-8')
            return data_principal, data_socio_eco
           
        except TypeError:
            print("You can only load CSV!")


