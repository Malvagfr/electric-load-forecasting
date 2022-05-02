
#############################################################################################################################
#                                                                                                                           #                       
#                            Electric load forecasting - Electric Demand data extraction                                    #     
#                                                                                                                           #
#                                             Ironhack Data Part Time --> Nov-2021                                          #
# Information coming from public source: UTC (Coordinated Universal Time)                                                   #
#                                                                                                                           #
# https://www.ree.es/es/apidatos                                                                                            #
#                                                                                                                           #
#############################################################################################################################

####################################################### Import libraries #####################################################

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Imports
import pandas as pd

######################################################## Function definition ################################################### 
# Read csv
def read_csv(path,sep_value):
    return pd.read_csv(path,sep=sep_value)

# Send data to csv
def send_to_csv(df,path):
    return df.to_csv(path)

# Row filter
def row_filter_limits(df, column,low_limit,high_limit):
    return df[(df[column]>=low_limit)&(df[column]<=high_limit)]

########################################################### Data import ##########################################################

def extract_electric_demand():
    print('----------------------- 3. starting electric demand load -----------------------')
    # Import dataframe
    df_electricity_demand=read_csv('./data/SOTs/electricity_demand/demanda_ES.csv',';')

    # Split time
    df_electricity_demand['Time']=pd.to_datetime(df_electricity_demand['utcDateTime'], format="%d/%m/%Y %H:%M")
    df_electricity_demand['Year']=df_electricity_demand['Time'].dt.year
    df_electricity_demand['Month']=df_electricity_demand['Time'].dt.month
    df_electricity_demand['Day']=df_electricity_demand['Time'].dt.day
    df_electricity_demand['Hour']=df_electricity_demand['Time'].dt.hour
    df_electricity_demand['Date']=df_electricity_demand['Time'].dt.date

    # Sort columns
    df_electricity_demand = df_electricity_demand[['utcDateTime', 'Time','Date', 'Year', 'Month',
                                                'Day','Hour','DemandaElect_ES_MWh']]

    # Filter period
    df_electricity_demand=row_filter_limits(df_electricity_demand, 'Year',2015,2021)

    # Send data to csv
    send_to_csv(df_electricity_demand,"./data/raw_data/electricity_demand.csv")

    # Print info
    print('----------------------- 4. finish electric demand load -----------------------')
    print(df_electricity_demand)