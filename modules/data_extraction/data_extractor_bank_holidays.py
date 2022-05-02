
#############################################################################################################################
#                                                                                                                           #                       
#                            Electric load forecasting - Bank holidays data extraction                                      #     
#                                                                                                                           #
#                                             Ironhack Data Part Time --> Nov-2021                                          #
# Information coming from public source:                                                                                    #
# https://administracion.gob.es/pag_Home/atencionCiudadana/calendarios/diasInhabiles.html#-b95725c1af8d                     #
#                                                                                                                           #
############################################################################################################################# 


####################################################### Import libraries #####################################################
# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# import libraries
import pandas as pd

######################################################## Function definition ################################################### 
# Read csv
def read_csv(path,sep_value,encoding_value):
    return pd.read_csv(path,sep=sep_value,encoding=encoding_value)

# Row filter
def row_filter_limits(df, column,low_limit,high_limit):
    return df[(df[column]>=low_limit)&(df[column]<=high_limit)]

# Send data to csv
def send_to_csv(df,path):
    return df.to_csv(path)

########################################################### Data import ##########################################################

def extract_bank_holidays():
    print('----------------------- 1. starting bank holidays load -----------------------')

    # Import dataframe
    df_bank_holidays=read_csv('./data/SOTs/bank_holidays/bank_holidays.csv',',','utf-8')

    # Split time
    df_bank_holidays['Date']=pd.to_datetime(df_bank_holidays['Day'], format="%d/%m/%Y")
    df_bank_holidays['Month']=df_bank_holidays['Date'].dt.month
    df_bank_holidays['Day']=df_bank_holidays['Date'].dt.day

    # Sort columns
    df_bank_holidays = df_bank_holidays[['Date', 'Year','Month', 'Day', 'Region']]

    # Time filter
    df_bank_holidays=row_filter_limits(df_bank_holidays, 'Year',2015,2021)

    # Remove not needed regions
    df_bank_holidays=df_bank_holidays[df_bank_holidays['Region']!='Baleares']

    # Send data to csv
    send_to_csv(df_bank_holidays,"./data/raw_data/bank_holidays.csv")

    # Print info
    print('----------------------- 2. finished bank holidays load ----------------------- ')
    print(df_bank_holidays)