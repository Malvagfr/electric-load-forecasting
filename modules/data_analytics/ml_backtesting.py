
#############################################################################################################################
#                                                                                                                           #                       
#                                     Electric load forecasting - ML backtesting                                            #     
#                                                                                                                           #
#                                        Ironhack Data Part Time --> Nov-2021                                               #
#                                                                                                                           #
#############################################################################################################################

####################################################### Import libraries #####################################################
# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Libraries Imports
import pandas as pd
import numpy as np

from datetime import datetime, date,timedelta
from dateutil import tz

# train test split
from sklearn.model_selection import train_test_split

# ML model
from xgboost import XGBRegressor

# error
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error

######################################################## Auxilary function definition ##########################################
# Read csv
def read_csv(path):
    return pd.read_csv(path)

# Change date format
def date_format(column,date_format):
    return pd.to_datetime(column,format=date_format)

# Drop columns
def drop_columns(df,columns):
    return df.drop(columns, 1) 

# Row filter
def row_filter_limits(df, column,low_limit,high_limit):
    return df[(df[column]>=low_limit)&(df[column]<=high_limit)]

# Change Timezone
def change_timezone(datetime,from_zone,to_zone):
    from_zone=tz.gettz(from_zone)
    to_zone=tz.gettz(to_zone)
    return datetime.replace(tzinfo=from_zone).astimezone(to_zone).replace(tzinfo=None)

# Join data
def join_data(df_left,df_right,link_fields,link_type):
    return pd.merge(df_left,df_right,on=link_fields,how=link_type)


########################################################### Data Import #########################################################
def import_data():
    # Import data 
    df_electricity_demand=read_csv("./data/intermediate_data/electricity_demand.csv")

    # Drop not needed columns
    df_electricity_demand=drop_columns(df_electricity_demand,'Unnamed: 0')

    # Change time format
    df_electricity_demand['Time']=date_format(df_electricity_demand['Time'],"%Y-%m-%d %H:%M:%S")
    return df_electricity_demand

########################################################### Feature engineering ###################################################

def craft_features(df,calendar_features=True,laglead_calendar_features=True,laglead_temperature=True,
                  roll_temperature=True,daily_temp_features=True):
    # Calendar features
    if calendar_features:
        df["Week_day"]=df.Time.dt.day_name().astype('category').cat.codes
        df['Week_day_category']=np.where(df["Time"].dt.dayofweek>4,'Weekend','Week')
        df['Week_day_category']=df['Week_day_category'].astype('category').cat.codes
        df["Bank_Holiday_Weight"]=df["Country_Bank_Holiday"]+df["Partial_Bank_Holiday_Weight"]

        # Laglead calendar features
        if laglead_calendar_features:
            df["Bank_Holiday_Weight_p24"]=df["Bank_Holiday_Weight"].shift(24)
            df["Bank_Holiday_Weight_n24"]=df["Bank_Holiday_Weight"].shift(-24)
            df["Bank_Holiday_Weight_p168"]=df["Bank_Holiday_Weight"].shift(168)
            df["Week_day_category_p24"]=df["Week_day_category"].shift(24)
            df["Week_day_category_n24"]=df["Week_day_category"].shift(-24)

    # Laglead Temperature 
    if laglead_temperature:
            df["Temp_K_p1"]=df["Temp_K"].shift(1)     
            df["Temp_K_p2"]=df["Temp_K"].shift(2)  

            df["Temp_K_n1"]=df["Temp_K"].shift(-1)     
            df["Temp_K_n2"]=df["Temp_K"].shift(-2)  

            df["Temp_K_p24"]=df["Temp_K"].shift(24)       
            df["Temp_K_p48"]=df["Temp_K"].shift(48)        
            df["Temp_K_p72"]=df["Temp_K"].shift(72)               
            df["Temp_K_p96"]=df["Temp_K"].shift(96)
            df["Temp_K_p120"]=df["Temp_K"].shift(120)
            df["Temp_K_p144"]=df["Temp_K"].shift(144)
            df["Temp_K_p168"]=df["Temp_K"].shift(168)

    # Rolling Statistical values
    if roll_temperature:
        df['Temp_K_SMA3']=df['Temp_K'].rolling(3,center=True).mean()
        df['Temp_K_SMA5']=df['Temp_K'].rolling(5,center=True).mean()
        df['Temp_K_SMA12']=df['Temp_K'].rolling(12,center=True).mean()

        df['Temp_K_SD3']=df['Temp_K'].rolling(3,center=True).std()
        df['Temp_K_SD5']=df['Temp_K'].rolling(5,center=True).std()
        df['Temp_K_SD12']=df['Temp_K'].rolling(12,center=True).std()

    # Statistical values by day
    if daily_temp_features:
        df_daily_temp=df.groupby(['Date'],as_index=False)\
        .agg(Daily_Temp_K_mean=('Temp_K', 'mean'),
             Daily_Temp_K_std=('Temp_K','std'),
             Daily_Temp_K_min=('Temp_K','min'),
             Daily_Temp_K_max=('Temp_K','min')
            )
        df=join_data(df,df_daily_temp,'Date','left')

        if laglead_temperature:
            df_dailylag_temp=df.groupby(['Date'],as_index=False)\
            .agg(Daily_Temp_K_p24_mean=('Temp_K_p24', 'mean'),
                 Daily_Temp_K_p24_std=('Temp_K_p24','std'),
                 Daily_Temp_K_p24_min=('Temp_K_p24','min'),
                 Daily_Temp_K_p24_max=('Temp_K_p24','min'),
                 Daily_Temp_K_p168_mean=('Temp_K_p168', 'mean'),
                 Daily_Temp_K_p168_std=('Temp_K_p168','std'),
                 Daily_Temp_K_p168_min=('Temp_K_p168','min'),
                 Daily_Temp_K_p168_max=('Temp_K_p168','min')
            )
            df=join_data(df,df_dailylag_temp,'Date','left')        

    df=drop_columns(df,['Country_Bank_Holiday','Partial_Bank_Holiday','Partial_Bank_Holiday_Weight','Date',
                       'Year','Day'])
    df=df.dropna()
    return df


########################################################### Model definition ###################################################

def get_xgb_model(df,section,target='Demand_MWh'):
    df=drop_columns(df,'Time')
    if section=='train':
        X=drop_columns(df,target)
        y=df[target]
        # Split train and test
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        # Model
        model_xgb=XGBRegressor(n_estimators=500,colsample_bylevel=1,colsample_bynode=1,
                         colsample_bytree=0.8,reg_alpha=1, reg_lambda=1,
                               gamma=0,learning_rate=0.1, random_state=42)
        model_xgb.fit(X, y)
        model_xgb.save_model("./data/final_results/models/XGB_model.json")

    elif section=='predict':
        model_xgb = XGBRegressor()
        model_xgb.load_model("./data/final_results/models/XGB_model.json")
        X_test=df
        predictions=model_xgb.predict(X_test)
        return predictions.tolist()


################################################### Backtest calculation #############################################################
def ml_backtest():
    print('----------------------- 22. starting ML -----------------------')  
    # Parameters definition

    # Historical data starts in 2015 in UTC
    begin_training=datetime.strptime('2015-01-01 00:00:00', '%Y-%m-%d %H:%M:%S') 

    # First forecast is set at the end of 2015 (so there is an historical year)
    # Forecast is launch each day at 11:00 o'clock in local time
    begin_forecast=datetime.strptime('2015-12-31 11:00:00', '%Y-%m-%d %H:%M:%S')
    end_forecast=datetime.strptime('2021-12-29 11:00:00', '%Y-%m-%d %H:%M:%S')
    end_forecast=datetime.strptime('2016-05-16 11:00:00', '%Y-%m-%d %H:%M:%S') #TO DELETE for testing purposes

    # Data is predicted everyday (24 hours)
    step=24 

    # Model is trained each month (30 days)
    training_frequency=30 

    # Timezone
    market_tz="Europe/Madrid"
    data_tz='UTC'

    # Feature Engineerging params

    # Define lags
    max_X_lag=168
    max_X_lead=24

    calendar_features=True
    laglead_calendar_features=True
    laglead_temperature=True
    roll_temperature=True
    daily_temp_features=True
    predict_with_feedback=False

    
    # Imort Data
    df_electricity_demand=import_data()

    # Backtest calculation

    # define empty dataframe
    final_preds=pd.DataFrame()

    # Define predict times (each day at 11:00 during forecast period)
    pred_dates = pd.DataFrame({"Pred_Date": pd.date_range(begin_forecast, end_forecast)})

    # loop for predict everyday and train everymonth
    for index, row in pred_dates.iterrows():
        
        index=index+1
        
        # train section
        if index % training_frequency == 0 or index==1:
            section='train'
            # end training is 23h of previous day (local time)
            end_training=row['Pred_Date'].floor('d')-timedelta(hours = 1)

            df_training=row_filter_limits(df_electricity_demand,'Time',begin_training,
                                        change_timezone(end_training,market_tz,data_tz))
            
            df_training=craft_features(df_training,calendar_features,laglead_calendar_features,laglead_temperature,
                                    roll_temperature,daily_temp_features)
            
            # Log
            print('training model from: ',begin_training,' - to: ',end_training)
            get_xgb_model(df_training,section)
            
        # Predict section
        
        section='predict'
        
        # Predit dates
        begin_pred=row['Pred_Date'].ceil('d')
        end_pred=begin_pred+timedelta(days = 1)-timedelta(hours = 1)
        
        # Request dates: padding (including more times so lags/leads NA match with prediction)
        begin=begin_pred-timedelta(hours = max_X_lag)
        end=end_pred+timedelta(hours = max_X_lead)
        
        if predict_with_feedback:
            # TODO: recursive predition
            print(row['Pred_Date'],begin_pred,end_pred)
        else:
            df_predict=df_electricity_demand.drop(columns=['Demand_MWh'])
            
            df_predict=row_filter_limits(df_electricity_demand,'Time',change_timezone(begin,market_tz,data_tz),
                                        change_timezone(end,market_tz,data_tz))
            # Feature engineering
            df_predict=craft_features(df_predict,calendar_features,laglead_calendar_features,laglead_temperature,
                                    roll_temperature,daily_temp_features)
            
            # Filtering data
            df_predict=row_filter_limits(df_predict,'Time',change_timezone(begin_pred,market_tz,data_tz),
                                        change_timezone(end_pred,market_tz,data_tz))
            # Prediction
            df_predict=drop_columns(df_predict,'Demand_MWh') #removing the target in backtest
            preds=get_xgb_model(df_predict,section)
            
            test_preds=pd.concat([pd.DataFrame(df_predict['Time'].tolist()),pd.DataFrame(preds)],axis=1,ignore_index=True)
            test_preds.columns = ['Time', 'Forecast']
            
        final_preds=final_preds.append(test_preds)
        
    # Assessing (evaluation)
    final_results=pd.merge(final_preds,df_electricity_demand[['Time','Demand_MWh']],on="Time",how="left")
    final_results.to_csv("./data/final_results/final_predictions.csv")
    rmse_val = mean_squared_error(final_results['Demand_MWh'], final_results['Forecast'])**0.5
    mae_val=mean_absolute_error(final_results['Demand_MWh'], final_results['Forecast'])
    mae_normalized=mae_val/final_results['Demand_MWh'].mean()*100

    print('----------------------- 23. finish ML -----------------------')  
    print('preditions: ',final_results)
    print('rmse: ',rmse_val)
    print('mae: ',mae_val)
    print('mae normalized: ',mae_normalized, ' %')




