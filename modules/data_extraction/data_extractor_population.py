
#############################################################################################################################
#                                                                                                                           #                       
#                            Electric load forecasting - Population data extraction                                         #     
#                                                                                                                           #
#                                             Ironhack Data Part Time --> Nov-2021                                          #
# Information coming from INE (https://www.ine.es/jaxiT3/Datos.htm?t=2915)                                                  #
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
def read_csv(path,sep_value,encoding_value):
    return pd.read_csv(path,sep=sep_value,encoding=encoding_value)

# Send data to csv
def send_to_csv(df,path):
    return df.to_csv(path)

# Row filter
def row_filter_limits(df, column,low_limit,high_limit):
    return df[(df[column]>=low_limit)&(df[column]<=high_limit)]

# Drop columns
def drop_columns(df,columns):
    return df.drop(columns, 1) 

# Replace values
def replace_values(df,column,old_value,new_value):
    return df[column].replace([old_value],[new_value])  

# Exclude 
def exclude(df,column,to_exclude):
    return df[~df[column].isin(to_exclude)]

########################################################### Data import ##########################################################

def extract_population():
    print('----------------------- 5. starting population load -----------------------')
    # Import dataframe
    df_population=read_csv('./data/SOTs/population/population.csv',';','latin-1')

    # Filter period
    df_population=row_filter_limits(df_population, 'Periodo',2015,2021)

    # Simplify names
    df_population['Comunidades y Ciudades Autónomas']=df_population['Comunidades y Ciudades Autónomas'].str[3:]

    df_population['Comunidades y Ciudades Autónomas'] = \
    replace_values(df_population,'Comunidades y Ciudades Autónomas','al','Total')
    df_population['Comunidades y Ciudades Autónomas'] = \
    replace_values(df_population,'Comunidades y Ciudades Autónomas','Asturias, Principado de','Asturias')
    df_population['Comunidades y Ciudades Autónomas'] = \
    replace_values(df_population,'Comunidades y Ciudades Autónomas','Castilla - La Mancha','Castilla-La Mancha')
    df_population['Comunidades y Ciudades Autónomas'] = \
    replace_values(df_population,'Comunidades y Ciudades Autónomas','Comunitat Valenciana','Comunidad Valenciana')
    df_population['Comunidades y Ciudades Autónomas'] = \
    replace_values(df_population,'Comunidades y Ciudades Autónomas','Madrid, Comunidad de','Madrid')
    df_population['Comunidades y Ciudades Autónomas'] = \
    replace_values(df_population,'Comunidades y Ciudades Autónomas','Murcia, Región de','Murcia')
    df_population['Comunidades y Ciudades Autónomas'] = \
    replace_values(df_population,'Comunidades y Ciudades Autónomas','Navarra, Comunidad Foral de','Navarra')
    df_population['Comunidades y Ciudades Autónomas'] = \
    replace_values(df_population,'Comunidades y Ciudades Autónomas','Rioja, La','La Rioja')

    # Exclude not needed regions
    df_population=exclude(df_population,'Comunidades y Ciudades Autónomas',
                        ['Total','Balears, Illes','Canarias','Ceuta','Melilla'])

    # Rename columns
    df_population.rename(columns={'Comunidades y Ciudades Autónomas': 'Region', 
                                'Periodo': 'Year', 'Total': 'Population'}, inplace=True)

    # Remove columns
    df_population=drop_columns(df_population,'Tamaño de los municipios')

    # Change data types
    df_population['Population']=df_population['Population'].str.replace('.', '').astype(float)

    # Send data to csv
    send_to_csv(df_population,"./data/raw_data/population.csv")

    # Print info
    print('----------------------- 6. finish population load -----------------------')
    print(df_population)
