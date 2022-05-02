
#############################################################################################################################
#                                                                                                                           #                       
#                            Electric load forecasting - Data transformation                                                #     
#                                                                                                                           #
#                                             Ironhack Data Part Time --> Nov-2021                                          #
#                                                                                                                           #
#############################################################################################################################

####################################################### Import libraries #####################################################

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Libraries Imports
import pandas as pd
import numpy as np

######################################################## Function definition ################################################### 

# Read csv
def read_csv(path):
    return pd.read_csv(path)

# Send data to csv
def send_to_csv(df,path):
    return df.to_csv(path)

# Drop columns
def drop_columns(df,columns):
    return df.drop(columns, 1) 

# Aggregate data
def agg_data(df, dimensions, agg_var,agg_opp):
    return df.groupby(dimensions, as_index=False).agg({agg_var:agg_opp})

# Join data
def join_data(df_left,df_right,link_fields,link_type):
    return pd.merge(df_left,df_right,on=link_fields,how=link_type)

########################################################### Data Transformation #################################################

def data_transformation():
    # Import raw data 
    df_temperatures=read_csv('./data/raw_data/temperatures.csv')
    df_bank_holidays=read_csv('.data/raw_data/bank_holidays.csv')
    df_electricity_demand=read_csv('.data/raw_data/electricity_demand.csv')
    df_population=read_csv('.data/raw_data/population.csv')

    # Drop not needed columns
    df_temperatures=drop_columns(df_temperatures,['Unnamed: 0'])
    df_bank_holidays=drop_columns(df_bank_holidays,['Unnamed: 0'])
    df_electricity_demand=drop_columns(df_electricity_demand,['Unnamed: 0'])
    df_population=drop_columns(df_population,['Unnamed: 0'])

    # Regions: Define region master table so cities and regions can be related

    # Define region master table
    print('----------------------- 11. starting region master definition -----------------------')
    df_regions=pd.DataFrame()

    df_regions['Region']=[x for x in df_population['Region'].unique()]

    df_regions['City']=['Sevilla','Zaragoza','Oviedo','Santander','Valladolid','Albacete',
                    'Barcelona','Valencia','Badajoz','Vigo','Madrid','Murcia','Pamplona',
                    'Bilbao','Logroño']

    # Save table
    send_to_csv(df_regions,".data/intermediate_data/regions.csv")

    # Print info
    print('----------------------- 12. finish region master definition -----------------------')
    print(df_regions)


    # Population: Calculate population ratio for each region
    print('----------------------- 13. starting Calculate population ratio for each region -----------------------')
    # Calculate country population over the years and ratio by region
    df_county_population=agg_data(df_population,['Year'],'Population','sum')

    df_county_population=df_county_population.rename(columns={'Population':'Total_Population'})

    df_population=join_data(df_population,df_county_population,'Year','left')
    df_population['Population_Ratio']=df_population['Population']/\
    df_population['Total_Population']

    # Print info
    print('----------------------- 14. finish Calculate population ratio for each region -----------------------')
    print(df_population)

    # Temperature: ponderation by region population
    print('----------------------- 15. starting Temperature: ponderation by region population -----------------------')

    # Add region to temperatures
    df_temperatures_region=join_data(df_temperatures,df_regions,'City','left')

    # Add population to temperatures and ponderate temperature by region
    df_temperatures_population=join_data(df_temperatures_region,df_population,['Region','Year'],'left')

    df_temperatures_population['Temp_Ponderation']= df_temperatures_population['Temp']\
    *df_temperatures_population['Population_Ratio']

    # Print info
    print('----------------------- 16. finish Temperature: ponderation by region population -----------------------')
    print(df_temperatures_population)

    # Bank holidays: ponderation by region
    print('----------------------- 17. starting Bank holidays: ponderation by region -----------------------')    
    # Add city to bank holidays
    df_bank_holidays_city=join_data(df_bank_holidays,df_regions,['Region'],'left')

    df_bank_holidays_city['City']=df_bank_holidays_city['City'].fillna('Nacional')

    def national_holiday(row):
        if row=='Nacional':
            return 1
        else:
            return 0
    
    df_bank_holidays_city['Country_Bank_Holiday']=df_bank_holidays_city['Region']\
    .apply(lambda row: national_holiday(row))

    # Take population and calculate bank holiday ratio
    df_bank_holidays_population=\
    join_data(df_bank_holidays_city,df_population,['Region','Year'],'left')

    df_bank_holidays_population['Population_Ratio']=\
    df_bank_holidays_population['Population_Ratio'].fillna(1)

    df_bank_holidays_population = \
    drop_columns(df_bank_holidays_population,['Population','Total_Population'])

    df_bank_holidays_population['Partial_Bank_Holiday'] = \
    np.where(df_bank_holidays_population['City']!='Nacional',1,0)

    df_bank_holidays_population['Partial_Bank_Holiday_Weight']=\
    df_bank_holidays_population['Partial_Bank_Holiday']*\
    df_bank_holidays_population['Population_Ratio']

    # Aggregate data by day
    df_bank_holidays_agg=df_bank_holidays_population.groupby(['Date','Year','Month','Day'], \
    as_index=False).agg(Country_Bank_Holiday=('Country_Bank_Holiday', 'mean'), \
    Partial_Bank_Holiday=('Partial_Bank_Holiday', 'mean'),\
    Partial_Bank_Holiday_Weight=('Partial_Bank_Holiday_Weight','sum'))

    # Save table
    send_to_csv(df_bank_holidays_agg,"./data/intermediate_data/bank_holidays_agg.csv")

    # Print info
    print('----------------------- 18. finish Bank holidays: ponderation by region -----------------------') 
    print(df_bank_holidays_agg)

    # Temperature: aggregation by country
    print('----------------------- 19. starting Temperature: aggregation by country -----------------------')     
    # Temperature aggregation for the whole country
    df_county_temp=agg_data(df_temperatures_population, 
                            ['Time','Date','Year','Month','Day','Hour'],'Temp_Ponderation','sum')

    # save table
    send_to_csv(df_county_temp,'./data/intermediate_data/county_temp.csv')

    # Temperature: Add bank holidays
    # Add bank holidays to temperature table
    df_county_temp_holidays=join_data(df_county_temp,df_bank_holidays_agg,
                                    ['Date','Year','Month','Day'],'left')

    df_county_temp_holidays['Country_Bank_Holiday']=\
    df_county_temp_holidays['Country_Bank_Holiday'].fillna(0)

    df_county_temp_holidays['Partial_Bank_Holiday']=\
    df_county_temp_holidays['Partial_Bank_Holiday'].fillna(0)

    df_county_temp_holidays['Partial_Bank_Holiday_Weight']=\
    df_county_temp_holidays['Partial_Bank_Holiday_Weight'].fillna(0)

    # save table
    send_to_csv(df_county_temp_holidays,'./data/intermediate_data/county_temp_holidays.csv')

    # Print info
    print('----------------------- 19. finish Temperature: aggregation by country -----------------------')  
    print(df_county_temp_holidays)

    # Final table: Merge demand and temperature
    # Merge demand and temperatute
    print('----------------------- 20. starting Final table: Merge demand and temperature -----------------------')  
    df_county_temp_demand=join_data(df_electricity_demand,df_county_temp_holidays,
            ['Time','Date','Year','Month','Day','Hour'],'inner')
    df_county_temp_demand=drop_columns(df_county_temp_demand,['utcDateTime'])

    # Add population
    df_country_population=agg_data(df_population, ['Year'], 'Population','sum')

    df_electricity_demand=join_data(df_county_temp_demand,df_country_population,'Year','left')

    # Change data types
    df_electricity_demand['DemandaElect_ES_MWh']=\
    df_electricity_demand['DemandaElect_ES_MWh'].str.replace(',', '.').astype(float)

    # Rename columns
    df_electricity_demand.rename(columns=\
    {'DemandaElect_ES_MWh': 'Demand_MWh', 'Temp_Ponderation': 'Temp_K'},inplace=True)

    # Save table
    send_to_csv(df_electricity_demand,'./data/intermediate_data/electricity_demand.csv')

    # Print info
    print('----------------------- 20. finish Final table: Merge demand and temperature -----------------------')  
    print(df_electricity_demand)

            


