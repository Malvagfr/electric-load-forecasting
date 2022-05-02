
#############################################################################################################################
#                                                                                                                           #                       
#                            Electric load forecasting - Temperature data extraction                                        #     
#                                                                                                                           #
#                                             Ironhack Data Part Time --> Nov-2021                                          #
# - Information exported from ERA5                                                                                          #
# (https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview)                         #
# - 2m dewpoint temperature	(K)                                                                                             #
#                                                                                                                           #
# - This parameter is the temperature to which the air, at 2 metres above the surface of the Earth, would have to be cooled #
# for saturation to occur. It is a measure of the humidity of the air. Combined with temperature and pressure, it can be    #
# used to calculate the relative humidity. 2m dew point temperature is calculated by interpolating between the lowest model #
# level and the Earth's surface, taking account of the atmospheric conditions. This parameter has units of kelvin (K).      #
# Temperature measured in kelvin can be converted to degrees Celsius (°C) by subtracting 273.15.                            #
# - UTC (Coordinated Universal Time)                                                                                        #
#                                                                                                                           #
#############################################################################################################################

####################################################### Import libraries #####################################################

# Ignore warnings ignore
import warnings
warnings.filterwarnings('ignore')

# Import libraries
import pandas as pd
import numpy as np
import cdsapi
import netCDF4

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

# Row filter
def row_filter_limits(df, column,low_limit,high_limit):
    return df[(df[column]>=low_limit)&(df[column]<=high_limit)]

######################################################## List of cities definition #################################################

# Main cities: Latitud, longitud:
# - Asturias - Oviedo: North 43.4°, West -5.8°, South 43.3°, East -5.7°
# - Madrid - Madrid: North 40.4°, West -3.7°, South 40.3°, East -3.6°
# - Cataluña - Barcelona: North 41.4°, West 2.1°, South 41.3°, East 2.2°
# - Comunidad Valenciana - Valencia: North 39.5°, West -0.37°, South 39.4°, East -0.38°
# - Andalucia - Sevilla: North 37.4°, West -6.0°, South 37.3°, East -5.9°
# - Aragón - Zaragoza: North 41.7°, West -0.8°, South 41.6°, East -0.9°
# - Murcia - Murcia: North 38.0°, West -1.1°, South 37.9°, East -1.2°
# - País Vasco - Bilbao: North 43.3°, West -2.8°, South 43.2°, East -2.9° 
# - Galicia - Vigo: North 42.2°, West -8.6°, South 42.1°, East -8.7°
# - Castilla y León - Valladolid: North 41.7°, West -4.6°, South 41.6°, East -4.7°
# - Cantabria - Santander: North 43.5°, West -3.7°, South 43.4°, East -3.8°
# - La Rioja - Logroño: North 42.5°, West -2.4°, South 42.4°, East -2.5°
# - Navarra - Pamplona: North 42.9°, West -1.6°, South 42.8°, East -1.7°
# - Castilla la mancha - Albacete: North 39.0°, West -1.8°, South 38.9°, East -1.9°
# - Extremadura - Badajoz: North 38.9°, West -6.9°, South 38.8°, East -7.0° 

# For each city a file is exported with 4 geographical points
file_list=['Oviedo','Madrid','Barcelona','Valencia','Sevilla','Zaragoza','Bilbao','Vigo','Santander',
           'Pamplona','Albacete','Badajoz','Murcia','Valladolid','Logroño']

########################################################### Data import ##########################################################

# Export data from nc format to csv
def temperature_extraction():
    print('----------------------- 7. starting temperature load -----------------------')
    df_temperatures = []
    for file in file_list:
        # Define paths
        path="./Data/SOTs/hourly_temperature/cities/"+file+".nc"

        # Define empty dataframes (each dataframe is a coordinate point)
        df_point_1=pd.DataFrame()
        df_point_2=pd.DataFrame()
        df_point_3=pd.DataFrame()
        df_point_4=pd.DataFrame() 
        df_time=pd.DataFrame() 
        
        # Define nc object
        nc=netCDF4.Dataset(path,'r')
        
        # Extract time
        time=nc.variables['time']
        dtime=netCDF4.num2date(time[:],time.units)
        df_time['Time']=np.array(dtime,dtype=type(dtime))
        
        # Extract temperatures
        temp_p1=np.array(nc.variables['d2m'][:,0,0],dtype=type(nc.variables['d2m'][:,0,0]))
        temp_p2=np.array(nc.variables['d2m'][:,0,1],dtype=type(nc.variables['d2m'][:,0,1]))
        temp_p3=np.array(nc.variables['d2m'][:,1,0],dtype=type(nc.variables['d2m'][:,1,0]))
        temp_p4=np.array(nc.variables['d2m'][:,1,1],dtype=type(nc.variables['d2m'][:,1,1]))
        
        df_point_1['Temp']=temp_p1
        df_point_2['Temp']=temp_p2
        df_point_3['Temp']=temp_p3
        df_point_4['Temp']=temp_p4
        
        # Concatenation of 4 points     
        df_city=pd.concat([df_point_1,df_point_2,df_point_3,df_point_4])
        
        # Merge time dimension
        df_city=pd.merge(df_city, df_time,left_index=True, right_index=True)
        
        # Include city values
        df_city['City']=file
        
        # Stort each city values
        df_temperatures.append(df_city)

        # Concatenate all cities 
        df_temperatures = pd.concat(df_temperatures)

        # Send data to csv
        send_to_csv(df_temperatures,"./data/SOTs/hourly_temperature/raw_temperatures.csv")

        # Print result
        print('----------------------- 8. starting temperature load -----------------------')
        print(df_temperatures)


def temperature_data_cleaning():

    print('----------------------- 9. starting data claning and aggregation -----------------------')
    # Import Dataframe
    df_raw_temperatures=read_csv("./data/SOTs/hourly_temperature/raw_temperatures.csv")

    # Drop not needed columns
    df_raw_temperatures=drop_columns(df_raw_temperatures,'Unnamed: 0')

    # Split time columns
    df_raw_temperatures['Time']=pd.to_datetime(df_raw_temperatures['Time'], format="%Y-%m-%d %H:%M:%S")
    df_raw_temperatures['Year']=df_raw_temperatures['Time'].dt.year
    df_raw_temperatures['Month']=df_raw_temperatures['Time'].dt.month
    df_raw_temperatures['Day']=df_raw_temperatures['Time'].dt.day
    df_raw_temperatures['Hour']=df_raw_temperatures['Time'].dt.hour
    df_raw_temperatures['Date']=df_raw_temperatures['Time'].dt.date

    # Sort columns
    df_raw_temperatures = df_raw_temperatures[['City', 'Time','Date', 'Year', 'Month','Day','Hour','Temp']]

    # Filter time 
    df_raw_temperatures=row_filter_limits(df_raw_temperatures, 'Year',2015,2021)

    # Remove outliers
    df_raw_temperatures=df_raw_temperatures[df_raw_temperatures['Temp']!=-32767.0]

    # Calculate temperature mean by city
    df_temperatures=df_raw_temperatures.groupby(['Time','Date','Year','Month',
                                             'Day','Hour','City'], as_index=False).agg({'Temp':'mean'})

    # Send data to csv
    send_to_csv(df_temperatures,"./data/raw_data/temperatures.csv")

    # Send results
    print('----------------------- 10. finish data claning and aggregation -----------------------')
    print(df_temperatures)



def extract_temperature():
    # Extract info
    temperature_extraction()
    temperature_data_cleaning()


